import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

# 💡 終極守門員：先把 HTML 標籤拔掉，再用 \b 搜尋
def match_currency_only(text, keyword):
    if not text or not keyword: return False
    # 1. 物理移除所有 HTML 標籤 (比如把 <div>CNY</div> 變成 " CNY ")
    clean_text = re.sub(r'<.*?>', ' ', str(text))
    # 2. 移除多餘空白並轉小寫
    clean_text = " ".join(clean_text.split()).lower()
    # 3. 執行 \b 鎖死匹配：搜尋 CNY 絕對不會抓到 Currency 或連結裡的網址
    return re.search(rf'\b{re.escape(str(keyword).lower())}\b', clean_text)

def smart_format(text):
    if not text: return ""
    # 讓顯示出來的文字也是乾淨的
    t = text.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<.*?>', '', t)
    t = t.replace('&nbsp;', ' ')
    return t.strip()

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    item['content'] = smart_format(item.get('content', ''))
                    item['expected'] = smart_format(item.get('expected', ''))
                return parsed_data 
        except: pass
    return smart_format(text)

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

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    # 🛡️ 幣種鎖死：3 碼不擴展，避免 USDT 聯想到 CNY
    if len(t_lower) == 3 and t_lower.isalpha():
        return [t_lower]
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)
