# case_generator.py
"""
把 Jira 需求單轉成：
  1) 測試大綱 (給 PM/QA 確認用的重點清單)
  2) 完整測試案例 (title / preconditions / steps+expected)

輸出的 steps 欄位是 [{"content": ..., "expected": ...}, ...]，
剛好對應 TestRail 的 custom_steps_separated 格式，可直接餵給
testrail_write.create_test_case()。

支援兩種 AI 供應商，用 GEN_PROVIDER 切換：
  - "gemini"    (預設，先用 Google 的免費額度測試)：需要 GEMINI_API_KEY
  - "anthropic" (之後想換回 Claude 再切)：需要 ANTHROPIC_API_KEY

設定方式 (.streamlit/secrets.toml)：
    GEN_PROVIDER = "gemini"
    GEMINI_API_KEY = "AIza..."
    # 之後想換回 Claude，改成：
    # GEN_PROVIDER = "anthropic"
    # ANTHROPIC_API_KEY = "sk-ant-..."

也可以用環境變數設定同名的值，效果一樣。
"""

import json
import os
import re
from typing import Any, Dict, List, Optional

import requests

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-sonnet-5"  # 依你的 API 方案調整，例如 claude-opus-4-8

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_MODEL = "gemini-2.5-flash"  # 免費額度目前涵蓋 Flash 系列；Google 偶爾會調整免費模型清單，
                                    # 若這個模型不再免費，去 https://ai.google.dev 查目前的免費模型名稱替換即可


class CaseGenError(Exception):
    pass


def _get_setting(name: str, explicit: Optional[str] = None) -> str:
    """依序從：明確傳入 > 環境變數 > st.secrets 取值。"""
    if explicit:
        return explicit
    value = os.environ.get(name, "")
    if value:
        return value
    try:
        import streamlit as st
        value = st.secrets.get(name, "")
    except Exception:
        pass
    return value or ""


def _get_provider(explicit: Optional[str] = None) -> str:
    provider = _get_setting("GEN_PROVIDER", explicit).strip().lower()
    return provider or "gemini"  # 預設用 Gemini，方便先用免費額度測試


def _get_api_key(provider: str, explicit_key: Optional[str] = None) -> str:
    key_name = "GEMINI_API_KEY" if provider == "gemini" else "ANTHROPIC_API_KEY"
    key = _get_setting(key_name, explicit_key)
    if not key:
        raise CaseGenError(
            f"找不到 {key_name}，請在 .streamlit/secrets.toml 或環境變數中設定。"
        )
    return key


def _call_gemini(prompt: str, api_key: str, max_tokens: int) -> str:
    url = GEMINI_API_URL.format(model=GEMINI_MODEL)
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens},
    }
    try:
        resp = requests.post(url, headers=headers, params=params, json=body, timeout=60)
    except requests.RequestException as e:
        raise CaseGenError(f"呼叫 Gemini API 失敗：{e}") from e

    if resp.status_code == 429:
        raise CaseGenError("Gemini 免費額度的速率限制被打到了（429），請稍等一下再試一次。")
    if not resp.ok:
        raise CaseGenError(f"Gemini API 回傳錯誤 ({resp.status_code})：{resp.text[:300]}")

    data = resp.json()
    candidates = data.get("candidates", [])
    if not candidates:
        finish_reason = data.get("promptFeedback", {})
        raise CaseGenError(f"Gemini 沒有回傳任何內容，可能被安全過濾擋下：{finish_reason}")

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "\n".join(p.get("text", "") for p in parts).strip()
    if not text:
        raise CaseGenError("Gemini 回傳了空白內容，請重新產生一次。")
    return text


def _call_claude(prompt: str, api_key: str, max_tokens: int) -> str:
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        resp = requests.post(ANTHROPIC_API_URL, headers=headers, json=body, timeout=60)
    except requests.RequestException as e:
        raise CaseGenError(f"呼叫 Claude API 失敗：{e}") from e

    if not resp.ok:
        raise CaseGenError(f"Claude API 回傳錯誤 ({resp.status_code})：{resp.text[:300]}")

    data = resp.json()
    text_parts = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
    return "\n".join(text_parts).strip()


def _call_llm(
    prompt: str,
    max_tokens: int = 4000,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
) -> str:
    resolved_provider = _get_provider(provider)
    key = _get_api_key(resolved_provider, api_key)

    if resolved_provider == "gemini":
        return _call_gemini(prompt, key, max_tokens)
    elif resolved_provider == "anthropic":
        return _call_claude(prompt, key, max_tokens)
    else:
        raise CaseGenError(f"不支援的 GEN_PROVIDER：{resolved_provider}（請用 'gemini' 或 'anthropic'）")


def _extract_json(raw_text: str) -> Any:
    """去除模型有時會加的 ```json 包裝，再解析。"""
    cleaned = re.sub(r"^```(json)?", "", raw_text.strip())
    cleaned = re.sub(r"```$", "", cleaned.strip())
    try:
        return json.loads(cleaned.strip())
    except json.JSONDecodeError as e:
        raise CaseGenError(f"AI 回傳格式無法解析為 JSON：{e}\n原始內容：{raw_text[:500]}") from e


def generate_test_outline(
    summary: str,
    description: str,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
) -> str:
    """
    第一步：只產生「測試重點大綱」給人工確認，不直接生完整案例。
    回傳純文字（條列式），方便在 st.text_area 中編輯。
    """
    prompt = f"""你是資深 QA 工程師。以下是 PM 開的 Jira 需求單，請你分析後列出「測試重點大綱」，
不要寫詳細步驟，只要條列出這個需求應該涵蓋哪些測試面向/情境(正常流程、邊界值、異常流程、權限相關等)。

需求標題：{summary}

需求描述：
{description or "(無描述)"}

請用繁體中文，以條列的方式輸出，例如：
1. 驗證 XXX 情境下 YYY 是否正確
2. 驗證權限不足時是否正確阻擋
...

只輸出條列大綱本身，不要加任何前言或結語。"""

    return _call_llm(prompt, max_tokens=1500, api_key=api_key, provider=provider)


def generate_test_cases(
    summary: str,
    description: str,
    confirmed_outline: str,
    path_hint: Optional[str] = None,
    format_example: Optional[str] = None,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    第二步：依據「已確認的大綱」產生完整測試案例，格式對齊 TestRail 欄位。

    回傳格式：
    [
      {
        "title": "...",
        "path": "父層 > 子層" 或 None,
        "preconditions": ["...", "..."],
        "steps": [
            {"content": "1. 路徑：... \\n2. 點擊[編輯]按鈕", "expected": "1. 顯示[...] 彈窗 ..."},
            ...
        ]
      },
      ...
    ]
    """
    default_format_hint = """每個 step 的 content / expected 用「數字編號 + 條列」的方式撰寫，
可以在同一個 step 裡放多個子項目，例如：
content: "1. 路徑：GoMoney > 權限管理 > 系統帳號管理\\n2. 點擊[編輯]按鈕\\n3. 編輯下面資訊\\n   • 編輯帳號類型：商戶管理員 → 系統管理員"
expected: "1. 顯示[檢查更改 / Review Changes] 彈窗\\n2. 標題：檢查更改\\n3. 項目/變更前/變更後 三欄比對內容"
中英對照的名詞可以用「中文 / English」並列。"""

    path_instruction = (
        f'所有案例的 "path" 欄位請固定填入："{path_hint}"'
        if path_hint
        else '請依需求內容自行判斷合理的分類路徑，格式為 "父層 > 子層"，填入 "path" 欄位；若不確定就填 null。'
    )

    prompt = f"""你是資深 QA 工程師，請依照以下資訊產生完整的測試案例，並且「只輸出 JSON，不要有任何其他文字、不要用 ```包裹」。

需求標題：{summary}

需求描述：
{description or "(無描述)"}

已確認的測試大綱：
{confirmed_outline}

輸出格式（JSON array）：
[
  {{
    "title": "測試案例標題（繁體中文，具體描述情境）",
    "path": "分類路徑或 null",
    "preconditions": ["前置條件1", "前置條件2"],
    "steps": [
      {{"content": "操作步驟文字", "expected": "預期結果文字"}}
    ]
  }}
]

撰寫規則：
- 每一條大綱項目至少對應一個測試案例。
- {default_format_hint if not format_example else format_example}
- {path_instruction}
- 用詞盡量對齊金融/後台管理系統情境（帳號、角色、商戶、權限等）。
- 只輸出 JSON，不要加前言、註解或 markdown 符號。"""

    raw = _call_llm(prompt, max_tokens=4000, api_key=api_key, provider=provider)
    parsed = _extract_json(raw)

    if isinstance(parsed, dict):
        parsed = [parsed]
    if not isinstance(parsed, list):
        raise CaseGenError("AI 回傳的資料結構不是預期的陣列格式。")

    return parsed
