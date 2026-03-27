import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def smart_format(text):
    """
    優化步驟內容的閱讀格式
    """
    if not text: return ""
    # 清理常見 HTML 標籤
    t = text.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n').replace('<div>', '')
    t = t.replace('&nbsp;', ' ')
    t = re.sub(r'<.*?>', '', t)
    
    # 針對特定動作關鍵字進行換行，讓排版更美
    keys = ["路徑", "內容管理", "選擇", "URL", "點擊", "点击", "登入", "進入", "查看", "確認", "正確"]
    for key in keys:
        t = re.sub(f'({key})', r'\n\1', t)
    
    # 自動補上 1. 2. 3. 序號
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    final_lines = []
    count = 1
    for line in lines:
        if not re.match(r'^\d+[\.\s]', line):
            final_lines.append(f"{count}. {line}")
            count += 1
        else:
            final_lines.append(line)
    return "\n".join(final_lines)

def clean_html(raw_html):
    """
    處理 TestRail 傳回的原始資料，包含分組步驟與一般 HTML
    """
    if not raw_html: return ""
    text = str(raw_html).strip()
    # 判斷是否為分步格式 [{}, {}]
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
    """
    從 TestRail 抓取全量 Case 資料
    """
    try:
        api = TestRailAPI(url.split('/index.php')[0].strip('/'), user, key)
        p_info = api.projects.get_project(project_id=pid)
        
        # 1. 抓取目錄 (Sections)
        all_sects = []
        offset = 0
        while True:
            sect_resp = api.sections.get_sections(project_id=pid, offset=offset)
            sects = sect_resp['sections'] if isinstance(sect_resp, dict) else sect_resp
            if not sects: break
            all_sects.extend(sects)
            if len(sects) < 250: break
            offset += 250
        
        id_to_name = {s['id']: s['name'] for s in all_sects}
        id_to_parent = {s['id']: s.get('parent_id') for s in all_sects}
        
        # 2. 遞迴組出完整路徑
        path_map = {}
        for s_id in id_to_name:
            parts = []
            curr = s_id
            while curr in id_to_name:
                parts.insert(0, id_to_name[curr])
                curr = id_to_parent.get(curr)
            path_map[s_id] = " › ".join(parts)
            
        # 3. 分頁抓取 Case
        all_cases, offset = [], 0
        while True:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = resp['cases']
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
            
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None

def multi_lang_search(text, dictionary):
    """
    【最終正確版】搜尋擴展邏輯
    這段代碼是「交集搜尋」的核心基礎。
    """
    t_lower = text.lower().strip()
    
    # 🛡️ 關鍵隔離：幣種 (CNY, THB, VND) 三碼單字不擴展字典
    # 這樣搜尋 "CNY" 時，絕對不會因為 "充值=deposit" 的關聯讓 Meh 混進來
    if len(t_lower) == 3 and t_lower.isalpha():
        return [t_lower]

    # 🛡️ 精確同義詞擴展
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        # 只有當輸入完全等於字典中某個字時，才把該組同義詞全拉進來
        if t_lower in g_lower: 
            res.update(g_lower)
            
    return list(res)
