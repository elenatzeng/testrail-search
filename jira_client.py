# jira_client.py
"""
最小化的 Jira Cloud REST API v3 客戶端。
只負責「讀取」需求單，不做任何寫入操作。

安全性注意事項：
- 這裡故意不寫死任何 API Token，一律由呼叫端 (OnlineApp.py) 從
  st.secrets 或環境變數帶進來。
- 若 Token 曾經在聊天紀錄 / Slack / Email 中明文出現過，請務必到
  Atlassian 帳號設定重新產生一組新的，並撤銷舊的。
"""

import base64
from typing import Any, Dict, List, Optional

import requests


class JiraError(Exception):
    """Jira 相關操作發生錯誤時拋出。"""


def _auth_header(email: str, api_token: str) -> Dict[str, str]:
    raw = f"{email}:{api_token}".encode("utf-8")
    token = base64.b64encode(raw).decode("utf-8")
    return {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
    }


def fetch_issue(jira_base_url: str, email: str, api_token: str, issue_key: str) -> Dict[str, Any]:
    """
    讀取單一 Jira issue。

    jira_base_url 範例: https://yourteam.atlassian.net
    issue_key 範例: PROJ-123
    """
    if not issue_key or not issue_key.strip():
        raise JiraError("請輸入需求單編號，例如 PROJ-123。")

    url = f"{jira_base_url.rstrip('/')}/rest/api/3/issue/{issue_key.strip()}"
    headers = _auth_header(email, api_token)

    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except requests.RequestException as e:
        raise JiraError(f"無法連線至 Jira：{e}") from e

    if resp.status_code == 401:
        raise JiraError("驗證失敗，請確認 Jira Email 與 API Token 是否正確（或 Token 已被撤銷）。")
    if resp.status_code == 404:
        raise JiraError(f"找不到需求單 {issue_key}，請確認單號或存取權限是否正確。")
    if not resp.ok:
        raise JiraError(f"Jira API 回傳錯誤 ({resp.status_code})：{resp.text[:300]}")

    content_type = resp.headers.get("Content-Type", "")
    if "application/json" not in content_type:
        # 狀態碼是 2xx，但回傳的不是 JSON —— 常見原因：
        # 1) jira_base_url 打錯（打到官網/其他網站，而不是你的 Jira 站台）
        # 2) 這是 Jira Server/Data Center 而非 Jira Cloud，API 路徑應為 /rest/api/2/... 而非 /rest/api/3/...
        # 3) 公司網路/SSO 攔截，回傳的是登入頁 HTML
        raise JiraError(
            "Jira 回應的內容不是 JSON（可能收到的是網頁而非 API 資料）。\n"
            f"請確認：\n"
            f"1. Jira 網域網址是否正確（應該像 https://yourteam.atlassian.net，不要含多餘路徑）\n"
            f"2. 是否為 Jira Server/Data Center（此工具預設走 Jira Cloud 的 /rest/api/3 路徑）\n"
            f"3. 公司網路是否有 SSO/VPN 攔截\n\n"
            f"實際收到的 Content-Type：{content_type or '(未提供)'}\n"
            f"回應內容前 300 字：\n{resp.text[:300]}"
        )

    try:
        return resp.json()
    except ValueError as e:
        raise JiraError(
            f"無法解析 Jira 回傳的 JSON：{e}\n回應內容前 300 字：\n{resp.text[:300]}"
        ) from e


def _adf_to_text(node: Any) -> str:
    """
    將 Jira 的 Atlassian Document Format (ADF) 描述欄位攤平成純文字。
    description 欄位在 API v3 是巢狀 JSON 結構，不是單純字串。

    特別處理表格 (table/tableRow/tableCell)，因為需求單常常用表格列
    「類型 vs 欄位」這種對照資訊，如果沒特別處理，內容會糊在一起，
    AI 收到的需求描述就會不完整。
    """
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if not isinstance(node, dict):
        return ""

    node_type = node.get("type")

    if node_type == "text":
        return node.get("text", "")

    if node_type == "hardBreak":
        return "\n"

    children = node.get("content", []) or []

    if node_type == "table":
        rows = [_adf_to_text(child) for child in children]
        rows = [r for r in rows if r]
        return "\n".join(rows)

    if node_type == "tableRow":
        cells = [_adf_to_text(child).strip() for child in children]
        cells = [c for c in cells if c]
        return " | ".join(cells)

    if node_type in ("tableCell", "tableHeader"):
        # 一個儲存格內可能有多個段落/清單，攤平成用「；」分隔的一行文字，
        # 避免整個表格因為儲存格內換行而錯位。
        parts = [_adf_to_text(child) for child in children]
        parts = [p.replace("\n", "；") for p in parts if p]
        return "；".join(parts)

    rendered = [_adf_to_text(child) for child in children]
    rendered = [r for r in rendered if r]

    if node_type == "listItem":
        return "• " + " ".join(rendered)
    if node_type in ("bulletList", "orderedList"):
        return "\n".join(rendered)
    if node_type == "heading":
        return "\n### " + " ".join(rendered)
    if node_type == "paragraph":
        return " ".join(rendered)

    return "\n".join(rendered)


def extract_issue_summary(issue_json: Dict[str, Any]) -> Dict[str, Any]:
    """把原始 Jira JSON 整理成前端好用的欄位。"""
    fields = issue_json.get("fields", {}) or {}
    return {
        "key": issue_json.get("key", ""),
        "summary": fields.get("summary", "") or "",
        "description": _adf_to_text(fields.get("description")),
        "issue_type": (fields.get("issuetype") or {}).get("name", ""),
        "status": (fields.get("status") or {}).get("name", ""),
        "reporter": (fields.get("reporter") or {}).get("displayName", ""),
        "labels": fields.get("labels", []) or [],
    }
