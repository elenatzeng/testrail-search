import json
import re
import time
import google.generativeai as genai
import streamlit as st

# 📌 直接從獨立檔案引入路徑地圖
from system_paths import SYSTEM_PATHS


class CaseGenError(Exception):
    """自訂 AI 測試案例產生異常"""
    pass


def get_gemini_model():
    """初始化 Gemini API 模型（最新穩定版）"""
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        raise CaseGenError("未設定 GEMINI_API_KEY，請在 Secrets 中配置。")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-3.6-flash")


def call_gemini_with_retry(prompt_input, max_retries=3, delay=5):
    """帶有自動重試機制與 429 處理的 Gemini 呼叫"""
    model = get_gemini_model()
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt_input,
                generation_config={"temperature": 0.2}
            )
            return response.text
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "ResourceExhausted" in err_str or "Quota" in err_str:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise CaseGenError("API 請求過於頻繁（已達免費額度），請等待約 20 秒後再試。")
            raise CaseGenError(f"Gemini API 呼叫失敗：{e}")


def get_candidate_paths(env_type: str, query_text: str, available_paths: list = None) -> list:
    """計算並排序最合適的系統路徑"""
    paths_to_check = available_paths if available_paths else SYSTEM_PATHS.get(env_type, SYSTEM_PATHS["GoGaming"])
    
    scored_paths = []
    q_words = [w.lower() for w in re.split(r"[\s>_/,\.-]+", query_text) if w]

    for p in paths_to_check:
        score = 0
        p_lower = p.lower()
        for word in q_words:
            if len(word) > 1 and word in p_lower:
                score += 2
        scored_paths.append((score, p))

    scored_paths.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored_paths]


def generate_test_outline(summary: str, description: str) -> str:
    """產生測試大綱"""
    prompt = f"""請分析以下 Jira 需求，列出測試重點大綱：
1. 請包含 [UI/介面]、[業務邏輯]（如狀態流轉/限制）、[異常/邊界] 測試。
2. 每行一條重點，保持精簡。

Jira 摘要：{summary}
Jira 描述：{description}"""
    return call_gemini_with_retry(prompt)


def generate_test_cases(
    summary: str,
    description: str,
    outline: str,
    env_type: str = "GoGaming",
    path_hint: str = None,
    selected_path: str = None,
    available_paths: list = None,
) -> list:
    """產生高品質測試案例"""
    target_path = selected_path or path_hint

    has_custom_path = target_path and target_path not in [
        "🤖 [自動由 AI 判斷路徑]",
        "其他",
        "",
        None
    ]

    candidate_paths = get_candidate_paths(env_type, f"{summary} {description} {outline}", available_paths=available_paths)
    fallback_default = candidate_paths[0] if candidate_paths else SYSTEM_PATHS.get(env_type, ["其他"])[0]
    display_path = target_path if has_custom_path else fallback_default

    # 📌 智能發送機制：指定路徑則直接發送；選 AI 自動判斷時僅提供 Top 20 相關路徑，防止暴 Token
    if has_custom_path:
        path_instruction = f'path 與 Step 1 請固定寫為："路徑：{target_path}"'
    else:
        short_paths = candidate_paths[:20]
        paths_str = "\n".join([f"- {p}" for p in short_paths])
        path_instruction = f"path 請從以下最匹配的路徑中挑選一條：\n{paths_str}"

    system_prompt = f"""你是一位 senior QA。請將 Jira 需求與大綱轉為 TestRail 測試案例 JSON Array。

【核心規則】：
1. {path_instruction}
2. **測試深度**：必須包含 UI 介面、業務邏輯限制（如重複操作阻擋、狀態變更）與異常邊界。
3. **Step 拆分**：必須拆為 2~3 個獨立 Step 物件（Step 1: 進入路徑; Step 2: 操作與輸入; Step 3: 邏輯驗證與預期結果）。
4. Preconditions 不要包含序號（如 1. ）。

JSON 範例：
[
  {{
    "title": "[模組]-情境或邏輯驗證",
    "path": "{display_path}",
    "preconditions": ["前置條件描述"],
    "steps": [
      {{"content": "路徑：{display_path}", "expected": "成功進入頁面"}},
      {{"content": "測試操作與輸入數據", "expected": "畫面與邏輯反應正常"}}
    ]
  }}
]"""

    user_input = f"Jira 摘要：{summary}\n需求描述：{description}\n大綱：\n{outline}"

    raw_text = call_gemini_with_retry([system_prompt, user_input])

    cleaned_text = re.sub(r"^```json\s*", "", raw_text, flags=re.MULTILINE)
    cleaned_text = re.sub(r"^```\s*", "", cleaned_text, flags=re.MULTILINE).strip()

    try:
        cases = json.loads(cleaned_text)

        # 後處理保證路徑精確度
        for case in cases:
            if has_custom_path:
                case["path"] = target_path
            elif not case.get("path") or case.get("path") == "其他":
                case["path"] = fallback_default

            steps = case.get("steps", [])
            if steps and isinstance(steps, list):
                first_step = steps[0]
                content = first_step.get("content", "")

                if "路徑：" in content or "路徑:" in content:
                    new_content = re.sub(r".*?路徑[:：].*?(\n|$)", f"路徑：{case['path']}\n", content)
                    first_step["content"] = new_content.strip()
                else:
                    first_step["content"] = f"路徑：{case['path']}\n" + content

            preconds = case.get("preconditions", [])
            if isinstance(preconds, list):
                case["preconditions"] = [re.sub(r"^\d+[\.\s]*", "", str(p).strip()) for p in preconds]

        return cases
    except json.JSONDecodeError:
        raise CaseGenError("AI 回傳格式非有效 JSON，請再試一次。")
