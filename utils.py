import re, time, streamlit as st, ast
from testrail_api import TestRailAPI
from html import unescape

# 💡 視覺化匹配：先把標籤剝掉，再搜純文字
def match_visual_only(text, keyword):
    if not text or not keyword: return False
    # 1. 物理移除：先把 HTML 轉義字元轉回 (如 &nbsp; 變空格)
    clean = unescape(str(text))
    # 2. 物理移除：移除所有 <...> 標籤 (包含屬性)
    clean = re.sub(r'<[^>]*>', ' ', clean)
    # 3. 規格化：移除多餘換行與空白，轉小寫
    clean = " ".join(clean.split()).lower()
    # 4. \b 鎖死：搜尋 "cny" 時，前後必須是邊界，不准連在其他字裡面
    return re.search(rf'\b{re.escape(str(keyword).lower())}\b', clean)

def smart_format(text):
    """用於前端顯示，保持閱讀感"""
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    # 🛡️ 幣別鎖死：3 碼英文（如 CNY）絕對不准聯想，回傳只有自己
    if len(t_lower) == 3 and t_lower.isalpha():
        return [t_lower]
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    try:
        api = TestRailAPI(url.split('/index.php')[0].strip('/'), user, key)
        p_info = api.projects.get_project(project_id=pid)
        all_sects, offset = [], 0
        while True:
            sect_resp = api.sections.get_sections(project_id=pid, offset=offset)
            sects = sect_resp['sections'] if isinstance(sect_resp, dict) else sect_resp
            if not sects: break
            all_sects.extend(sects)
            if len(sects) < 250: break
            offset += 250
        id_to_name = {s['id']: s['name'] for s in all_sects}
        id_to_parent = {s['id']: s.get('parent_id') for s in all_sects}
        path_map = {}
        for s_id in id_to_name:
            parts, curr = [], s_id
            while curr in id_to_name:
                parts.insert(0, id_to_name[curr])
                curr = id_to_parent.get(curr)
            path_map[s_id] = " › ".join(parts)
        all_cases, offset = [], 0
        while True:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = resp['cases']
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e: return None, None, str(e), None
