import re
import time
import streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def clean_html(text):
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)import re
import time
import streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def clean_html(text):
    """
    ✨ 完整 HTML 清理工具
    處理 TestRail 導出的 <br>, <div> 以及轉義字元，確保輸出為純文字。
    """
    if not text:
        return ""
    
    # 1. 處理 HTML 轉義字元 (如 &nbsp;, &quot;)
    t = unescape(str(text))
    
    # 2. 將換行標籤轉為真正的換行符號
    t = t.replace('<br />', '\n').replace('<br>', '\n')
    t = t.replace('</div>', '\n').replace('</p>', '\n')
    
    # 3. 移除所有剩餘的 HTML 標籤
    t = re.sub(r'<[^>]*>', '', t)
    
    # 4. 去除多餘的空格與頭尾空白
    return t.strip()

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    """
    🚀 核心資料抓取邏輯 (強化穩定版)
    支援自動辨識 List/Dict 結構，防止紅字報錯。
    """
    try:
        # 自動格式化網址，移除多餘的 index.php 或斜線
        base_url = url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, user, key)
        
        # A. 抓取專案資訊 (驗證連線)
        p_info = api.projects.get_project(project_id=pid)
        p_name = p_info.get('name', 'Project')
        
        # B. 抓取目錄結構 (Sections)
        all_sects = api.sections.get_sections(project_id=pid)
        path_map = {s['id']: s['name'] for s in all_sects}
        
        # C. 抓取測試案例 (Cases)
        # 這裡加了 limit=1000 確保資料抓得夠多
        resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        
        # 🛡️ 關鍵修復：自動相容不同的 API 回傳格式
        if isinstance(resp, list):
            cases_list = resp
        elif isinstance(resp, dict):
            cases_list = resp.get('cases', [])
        else:
            cases_list = []
            
        sync_time = time.strftime("%H:%M:%S")
        return cases_list, path_map, sync_time, p_name

    except Exception as e:
        # 發生錯誤時，將錯誤訊息傳回給介面顯示
        error_msg = str(e)
        return None, None, error_msg, None

def multi_lang_search(text, dictionary):
    """
    📖 聯想詞檢索工具
    根據 keywords.py 裡的字典，自動擴展搜尋詞。
    """
    if not text:
        return []
        
    t_lower = text.lower().strip()
    res = {t_lower} # 使用集合防止重複
    
    # 在字典中尋找匹配的聯想詞群組
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break # 找到一組後就跳出，避免過度擴展
            
    return list(res)

def get_case_steps(item):
    """
    📝 額外擴充：步驟格式標準化
    TestRail 的步驟有兩種格式 (custom_steps 或 custom_steps_separated)
    """
    steps = item.get('custom_steps') or item.get('custom_steps_separated') or ""
    return steps
    return t.strip()

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    try:
        base_url = url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, user, key)
        p_info = api.projects.get_project(project_id=pid)
        all_sects = api.sections.get_sections(project_id=pid)
        path_map = {s['id']: s['name'] for s in all_sects}
        resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        
        # 🛡️ 修正：防止 string indices must be integers 錯誤
        cases_list = resp if isinstance(resp, list) else resp.get('cases', [])
        return cases_list, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)
