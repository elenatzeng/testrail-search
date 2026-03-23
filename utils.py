import re, time, streamlit as st
from testrail_api import TestRailAPI

# 🚀 終極修復：自動編號與換行功能
def clean_html(raw_html):
    if not raw_html: return "（無詳細步驟）"
    text = str(raw_html)
    
    # 處理 HTML 標籤
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text) 
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")

    # 🚀 無敵拆分術：只要看到「數字.」就強制換行
    text = re.sub(r'(\d+[\.\、])', r'\n\1', text)
    
    # 清理多餘空行
    raw_lines = [l.strip() for l in text.split('\n') if l.strip()]
    final_output = []
    current_num = 1
    
    # 💡 數字編號核心邏輯：自動補全或修正跳號
    for line in raw_lines:
        # 如果這一行開頭已經有 1. 或 2、 這樣的格式，我們修正它的號碼
        if re.match(r'^\d+[\.\、]', line):
            # 去除原本的編號，重新編號
            clean_line = re.sub(r'^\d+[\.\、]\s*', '', line)
            final_output.append(f"{current_num}. {clean_line}")
            current_num += 1
        else:
            # 如果沒有編號，我們幫它加上去
            final_output.append(f"{current_num}. {line}")
            current_num += 1
            
    return "\n".join(final_output)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        
        # 正確抓取 Section 資料
        sections_data = api.sections.get_sections(project_id=pid, suite_id=sid)
        sect_dict = {s['id']: s for s in sections_data['sections']}
        
        # 递归抓取完整目錄路徑
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            parent_id = curr.get('parent_id')
            if parent_id:
                return f"{get_path(parent_id)} > {curr['name']}"
            return curr['name']
            
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}

        # 分頁抓取 Case 資料 (確保抓到 5000 筆以上)
        all_cases_list = []
        offset = 0
        while True:
            response = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = response['cases']
            if not cases: break
            all_cases_list.extend(cases)
            if len(cases) < 250: break
            offset += 250
            
        return all_cases_list, path_map, time.strftime("%H:%M:%S"), p_info.get('name')
    except Exception as e:
        return None, None, None, str(e)

def multi_lang_search(text, dictionary):
    text_lower = text.lower().strip()
    related_words = {text_lower}
    for group in dictionary:
        group_lower = [str(word).lower() for word in group]
        if any(text_lower in word for word in group_lower) or any(word in text_lower for word in group_lower):
            related_words.update(group_lower)
    return list(related_words)
