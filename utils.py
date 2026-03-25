import re, time, streamlit as st
from testrail_api import TestRailAPI

# ✨ 功能 1：自動格式化 (解析 HTML + 強制拆分編號)
def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html)
    
    # 基本清理 HTML 標籤與轉義符號
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # 🚀 強制拆分邏輯：針對黏在一起的業務關鍵字強制換行
    split_keys = ["路徑", "選擇", "URL", "點擊", "点击", "登入", "查看", "成功", "Request", "Expected"]
    for word in split_keys:
        # 使用正則表達式：如果關鍵字前面不是換行符，就補一個換行
        text = re.sub(f'(?<!\\n)({word})', r'\n\1', text)
    
    # 針對數字編號 (1. 2. 3.) 強制換行
    text = re.sub(r'(?<!\\n)(\d+[\.\、])', r'\n\1', text)

    # 切分行並重新排版
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    final_output = []
    for i, line in enumerate(lines, 1):
        # 去除行首可能殘留的舊編號
        clean_line = re.sub(r'^\d+[\.\、\:\s]*', '', line)
        if clean_line:
            final_output.append(f"{i}. {clean_line}")
    return "\n".join(final_output)

# 🌐 功能 2：智慧三語聯動 (精確匹配版)
def multi_lang_search(text, dictionary):
    """
    優化邏輯：
    1. 只有當搜尋詞『完全等於』字典組中的某個詞時，才展開該組的所有同義詞。
    2. 避免因為 '#' 或單個字造成的過度聯想。
    """
    text_lower = text.lower().strip()
    related_words = {text_lower}
    
    for group in dictionary:
        # 將整組字典詞轉為小寫清單
        group_lower = [str(word).lower() for word in group]
        
        # 🚀 只有『完全匹配』才擴展 (例如輸入 'deposit' 才會變出 '充值')
        if text_lower in group_lower:
            related_words.update(group_lower)
            
    return list(related_words)

# 📦 功能 3：TestRail API 資料抓取
@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        # 格式化 URL 並初始化 API
        base_url = _url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, _user, _pw)
        
        # 獲取專案名稱
        p_info = api.projects.get_project(project_id=pid)
        
        # 獲取所有目錄 (Sections) 並建立路徑地圖
        sections_data = api.sections.get_sections(project_id=pid, suite_id=sid)
        sect_dict = {s['id']: s for s in sections_data['sections']}
        
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            parent_id = curr.get('parent_id')
            if parent_id:
                return f"{get_path(parent_id)} > {curr['name']}"
            return curr['name']
            
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}
        
        # 分頁抓取所有案例 (Cases)
        all_cases_list = []
        offset = 0
        while True:
            response = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = response['cases']
            if not cases: break
            all_cases_list.extend(cases)
            if len(cases) < 250: break
            offset += 250
            
        sync_time = time.strftime("%H:%M:%S")
        return all_cases_list, path_map, sync_time, p_info.get('name')
        
    except Exception as e:
        # 發生錯誤時回傳錯誤訊息
        return None, None, str(e), None
