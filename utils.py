import re, time, streamlit as st
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return "（無詳細步驟）"
    
    # 1. 先處理掉 HTML 標籤
    text = str(raw_html)
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")

    # 🚀 2. 核心魔法：強制在「數字.」前面加上換行符號
    # 即使妳寫的是 "1.XXX 2.YYY"，我也會把它變成：
    # 1.XXX
    # 2.YYY
    text = re.sub(r'(\d+[\.\、])', r'\n\1', text)

    # 3. 把文字切開並去除多餘空格
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # 4. 再次檢查：如果每一行開頭沒編號，幫妳補上；如果有編號，維持原樣
    final_output = []
    current_num = 1
    for line in lines:
        # 檢查開頭是不是已經有 1. 或 2. 這樣的格式
        if re.match(r'^\d+[\.\、]', line):
            final_output.append(line)
            # 更新計數器，確保下一個沒編號的行接得上下去
            try:
                current_num = int(re.search(r'^(\d+)', line).group(1)) + 1
            except:
                current_num += 1
        else:
            final_output.append(f"{current_num}. {line}")
            current_num += 1

    return "\n".join(final_output)

# --- 剩下的 fetch_data_from_tr 保持不變 ---
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
