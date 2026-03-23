import re, time, streamlit as st
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return "（無詳細步驟）"
    text = str(raw_html)
    
    # 1. 基礎清理
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # 🚀 2. 核心拆分術：針對妳 Step 2 這種「黏死死」的文字
    # 我們在常見的動作關鍵字（路徑、選擇、URL、點擊、登入、查看）前面強制補換行
    keywords = ["路徑", "選擇", "URL", "點擊", "点击", "登入", "查看", "成功"]
    for word in keywords:
        # 如果關鍵字前面不是換行，就幫它補一個
        text = re.sub(f'(?<!\\n)({word})', r'\n\1', text)
    
    # 🚀 3. 如果裡面原本就有數字編號（如 1. 2.），也強制換行
    text = re.sub(r'(?<!\\n)(\d+[\.\、])', r'\n\1', text)

    # 4. 切開所有行並去除前後空格
    raw_lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # 5. 重新分配 12345 編號
    final_output = []
    current_num = 1
    for line in raw_lines:
        # 去除掉 line 開頭原本可能存在的任何數字編號（避免出現 1. 1. 路徑）
        clean_line = re.sub(r'^\d+[\.\、\:\s]*', '', line)
        if clean_line:
            final_output.append(f"{current_num}. {clean_line}")
            current_num += 1
            
    return "\n".join(final_output)

# 下方的 fetch_data_from_tr 保持不變 ...
@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        sections_data = api.sections.get_sections(project_id=pid, suite_id=sid)
        sect_dict = {s['id']: s for s in sections_data['sections']}
        
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            return f"{get_path(curr.get('parent_id'))} > {curr['name']}" if curr.get('parent_id') else curr['name']
            
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}
        
        all_cases_list, offset = [], 0
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
