import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def smart_format(text):
    """將 TestRail 的亂碼或 HTML 轉為漂亮的條列式步驟"""
    if not text: return ""
    # 1. 基本清理：將常見標籤換成換行
    t = str(text).replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n').replace('<div>', '')
    t = t.replace('&nbsp;', ' ')
    t = re.sub(r'<.*?>', '', t) # 移除所有 HTML 標籤
    
    # 2. 動作關鍵字拆分：自動在動作前換行，增加可讀性
    keys = ["路徑", "內容管理", "選擇", "URL", "點擊", "点击", "登入", "進入", "查看", "確認", "正確", "輸入"]
    for key in keys:
        # 使用正則表達式，確保只在關鍵字前面補換行（如果前面不是換行的話）
        t = re.sub(f'([^\\n])({key})', r'\1\n\2', t)
    
    # 3. 補上 1. 2. 3. 序號
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    final_lines = []
    count = 1
    for line in lines:
        # 如果這一行開頭已經有數字了，就直接用；沒有的話幫它加上去
        if not re.match(r'^\d+[\.\s]', line):
            final_lines.append(f"{count}. {line}")
            count += 1
        else:
            final_lines.append(line)
    return "\n".join(final_lines)

def clean_html(raw_html):
    """判斷是分步 Case 還是純文字 Case 並處理"""
    if not raw_html: return ""
    text = str(raw_html).strip()
    # 如果內容長得像 list/dict (TestRail 分步格式)，嘗試解析它
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
    """核心：從 TestRail 抓取全量目錄與案例"""
    try:
        # 移除 URL 尾端的 index.php
        base_url = url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, user, key)
        
        # 取得專案名稱
        p_info = api.projects.get_project(project_id=pid)
        
        # 🚀 抓取全量目錄 (處理分頁 offset)
        all_sects = []
        offset = 0
        while True:
            sect_resp = api.sections.get_sections(project_id=pid, suite_id=sid, offset=offset)
            sects = sect_resp['sections'] if isinstance(sect_resp, dict) else sect_resp
            if not sects: break
            all_sects.extend(sects)
            if len(sects) < 250: break
            offset += 250
        
        # 建立目錄路徑地圖
        id_to_name = {s['id']: s['name'] for s in all_sects}
        id_to_parent = {s['id']: s.get('parent_id') for s in all_sects}
        
        path_map = {}
        for s_id in id_to_name:
            parts = []
            curr = s_id
            # 向上追溯父目錄直到頂層
            while curr in id_to_name:
                parts.insert(0, id_to_name[curr])
                curr = id_to_parent.get(curr)
            path_map[s_id] = " › ".join(parts)
            
        # 🚀 抓取全量測試案例 (處理分頁 offset)
        all_cases, offset = [], 0
        while True:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            # 修正：有些 API 回傳格式不同，確保抓到的是 list
            cases = resp['cases'] if isinstance(resp, dict) and 'cases' in resp else resp
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
            
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        # 發生錯誤時回傳錯誤訊息，讓 OnlineApp.py 可以顯示 st.error
        return None, None, str(e), None

def multi_lang_search(text, dictionary):
    """多語系聯想搜尋：CNY 搜尋也能命中"""
    t_lower = text.lower().strip()
    res = {t_lower} # 先把原始關鍵字放進去
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        # 如果輸入的字在字典組裡，就把整組聯想詞都加進去
        if t_lower in g_lower: 
            res.update(g_lower)
    return list(res)
