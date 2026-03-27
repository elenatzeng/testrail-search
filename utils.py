import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

# 💡 核心：先剝皮 HTML，再用 \b 鎖死搜尋
def match_strict(text, keyword):
    if not text or not keyword: return False
    # 1. 殺掉所有 HTML 標籤 (確保不被 class="cny" 影響)
    clean_text = re.sub(r'<.*?>', ' ', str(text))
    # 2. 移除多餘空白、換行
    clean_text = " ".join(clean_text.split()).lower()
    # 3. \b 鎖死單字邊界
    return re.search(rf'\b{re.escape(str(keyword).lower())}\b', clean_text)

def smart_format(text):
    if not text: return ""
    t = str(text).replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    return re.sub(r'<.*?>', '', t).strip()

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    # 🛡️ 幣別鎖死：搜尋 3 碼英文時，回傳列表只有它自己，不准聯想！
    if len(t_lower) == 3 and t_lower.isalpha():
        return [t_lower]
    
    # 非幣別詞才走字典
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    # ... (此處保留妳原本的 TestRail 連線代碼，包含 path_map 的生成) ...
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
