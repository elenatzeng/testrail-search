# testrail_write.py
"""
負責「寫入」TestRail 的部分：
  - 依路徑字串找到對應 section_id，找不到就沿路徑自動建立
  - 建立測試案例 (custom_steps_separated 格式)

沿用你原本 OnlineApp.py 裡 fetch_data_from_tr() 產生的 path_map
(dict: section_id -> "父層 > 子層 > ..." 這種字串)，所以不需要改動
utils.py 就能接上。
"""

from typing import Any, Dict, List, Optional

import requests
from requests.auth import HTTPBasicAuth


class TestRailWriteError(Exception):
    pass


def _get(tr_url: str, tr_user: str, tr_pw: str, path: str) -> Any:
    url = f"{tr_url.rstrip('/')}/index.php?{path}"
    try:
        resp = requests.get(
            url, auth=_auth(tr_user, tr_pw), headers={"Content-Type": "application/json"}, timeout=15
        )
    except requests.RequestException as e:
        raise TestRailWriteError(f"連線 TestRail 失敗：{e}") from e
    if not resp.ok:
        raise TestRailWriteError(f"TestRail API 錯誤 ({resp.status_code})：{resp.text[:300]}")
    return resp.json()


def _unwrap_list(data: Any, key: str) -> List[Dict[str, Any]]:
    """
    TestRail 新版 API 會把清單包在 {"<key>": [...], "_links": {...}} 裡，
    舊版直接回傳 [...]，這裡統一處理兩種格式。
    """
    if isinstance(data, dict):
        return data.get(key, []) or []
    if isinstance(data, list):
        return data
    return []


def list_projects(tr_url: str, tr_user: str, tr_pw: str) -> List[Dict[str, Any]]:
    """回傳 [{"id": ..., "name": ...}, ...]，讓使用者可以用選單挑 Project。"""
    data = _get(tr_url, tr_user, tr_pw, "/api/v2/get_projects")
    return _unwrap_list(data, "projects")


def list_suites(tr_url: str, tr_user: str, tr_pw: str, project_id: int) -> List[Dict[str, Any]]:
    """回傳指定 Project 底下的 [{"id": ..., "name": ...}, ...] Suite 清單。"""
    data = _get(tr_url, tr_user, tr_pw, f"/api/v2/get_suites/{project_id}")
    return _unwrap_list(data, "suites")


def fetch_sections(
    tr_url: str, tr_user: str, tr_pw: str, project_id: int, suite_id: int
) -> Dict[int, str]:
    """
    針對指定的 Project/Suite，重新抓一份「section_id -> 完整路徑」的對照表，
    格式跟 utils.fetch_data_from_tr() 產生的 path_map 一致，讓
    get_or_create_section() 可以直接沿用。
    """
    data = _get(
        tr_url, tr_user, tr_pw, f"/api/v2/get_sections/{project_id}&suite_id={suite_id}"
    )
    sections = _unwrap_list(data, "sections")

    by_id = {s["id"]: s for s in sections}

    def build_path(sec: Dict[str, Any], _seen: Optional[set] = None) -> str:
        _seen = _seen or set()
        name = sec.get("name", "")
        parent_id = sec.get("parent_id")
        if parent_id and parent_id in by_id and parent_id not in _seen:
            return build_path(by_id[parent_id], _seen | {sec["id"]}) + " > " + name
        return name

    return {s["id"]: build_path(s) for s in sections}


def _auth(tr_user: str, tr_pw: str) -> HTTPBasicAuth:
    return HTTPBasicAuth(tr_user, tr_pw)


def find_section_id_by_path(path_map: Dict[int, str], path_str: str) -> Optional[int]:
    target = (path_str or "").strip()
    for sid, p in path_map.items():
        if (p or "").strip() == target:
            return sid
    return None


def get_or_create_section(
    tr_url: str,
    tr_user: str,
    tr_pw: str,
    project_id: int,
    suite_id: int,
    path_map: Dict[int, str],
    path_str: str,
) -> int:
    """
    如果 path_str 已存在就回傳現有 section_id。
    如果不存在，依 " > " 拆解路徑，逐層檢查/建立，回傳最末層的 section_id。
    path_map 會被就地更新（同一個 dict 物件），方便後續案例沿用同一次查詢結果。
    """
    path_str = (path_str or "未分類").strip()

    existing = find_section_id_by_path(path_map, path_str)
    if existing is not None:
        return existing

    segments = [s.strip() for s in path_str.split(">") if s.strip()]
    if not segments:
        segments = ["未分類"]

    parent_id: Optional[int] = None
    current_path = ""

    for seg in segments:
        current_path = f"{current_path} > {seg}" if current_path else seg

        existing_id = find_section_id_by_path(path_map, current_path)
        if existing_id is not None:
            parent_id = existing_id
            continue

        payload: Dict[str, Any] = {"name": seg, "suite_id": suite_id}
        if parent_id is not None:
            payload["parent_id"] = parent_id

        url = f"{tr_url.rstrip('/')}/index.php?/api/v2/add_section/{project_id}"
        try:
            resp = requests.post(
                url,
                auth=_auth(tr_user, tr_pw),
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15,
            )
        except requests.RequestException as e:
            raise TestRailWriteError(f"建立分類「{current_path}」失敗：{e}") from e

        if not resp.ok:
            raise TestRailWriteError(
                f"建立分類「{current_path}」失敗 ({resp.status_code})：{resp.text[:300]}"
            )

        new_section = resp.json()
        new_id = new_section["id"]
        path_map[new_id] = current_path
        parent_id = new_id

    return parent_id  # type: ignore[return-value]


def create_test_case(
    tr_url: str,
    tr_user: str,
    tr_pw: str,
    section_id: int,
    title: str,
    preconditions: str,
    steps_separated: List[Dict[str, str]],
    template_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    steps_separated: [{"content": "...", "expected": "..."}, ...]

    ⚠️ template_id 因 TestRail 站台設定而異，代表「Test Case (Steps)」樣板。
    若你的站台不確定 ID 是多少，可先呼叫
    GET /index.php?/api/v2/get_templates/{project_id} 查詢，
    再把正確的 ID 傳進來；留 None 會使用專案預設樣板（但預設樣板不一定支援
    custom_steps_separated 欄位，建議明確指定）。
    """
    payload: Dict[str, Any] = {
        "title": title,
        "custom_preconds": preconditions,
        "custom_steps_separated": steps_separated,
    }
    if template_id is not None:
        payload["template_id"] = template_id

    url = f"{tr_url.rstrip('/')}/index.php?/api/v2/add_case/{section_id}"
    try:
        resp = requests.post(
            url,
            auth=_auth(tr_user, tr_pw),
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15,
        )
    except requests.RequestException as e:
        raise TestRailWriteError(f"建立測試案例失敗：{e}") from e

    if not resp.ok:
        raise TestRailWriteError(f"建立測試案例失敗 ({resp.status_code})：{resp.text[:300]}")

    return resp.json()
