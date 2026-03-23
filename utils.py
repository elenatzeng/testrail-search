import re, time, streamlit as st
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return "（無詳細步驟）"
    text = str(raw_html)
    
    # 1. 處理 HTML 換行標籤
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text) 
    
    # 2. 移除所有剩餘的 HTML 標籤
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', text)
    
    # 3. 處理轉義字元
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # 4. 🚀 數字編號核心邏輯：將擠在一起的 "2.路徑" 拆開
    # 在「數字+點」前面如果不是換行，就強行補一個換行
    text = re.sub(r'(?<!\n)(\d+[\.\、])', r'\n\1', text)
    
    # 5. 清理空行並重新整理
    raw_lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # 6. 💡 自動補全數字邏輯：
    # 如果妳的文字裡本來就有 "1." "2."，我們會保留它
    # 如果妳的文字只是普通句子，我們幫它加上編號
    final_lines = []
    for i, line in enumerate(raw_lines, 1):
        # 如果這一行開頭已經是數字編號（例如 1. 或 2、），就直接用
        if re.match(r'^\d+[\.\、\:]', line):
            final_lines.append(line)
        else:
            # 如果沒有編號，我們幫它加上去
            final_lines.append(f"{i}. {line}")
            
    return "\n".join(final_lines)

# --- 以下 fetch_data_from_tr 等函數保持不變 ---
@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        all_sects = api.sections.get_sections(project_id=pid, suite_id=sid)
        sect_dict = {s['id']: s for s in all_sects['sections']}
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            return f"{get_path(curr.get('parent_id'))} > {curr['name']}" if curr.get('parent_id') else curr['name']
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}
        
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
