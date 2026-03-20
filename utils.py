import re
import streamlit as st
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return "（無步驟）"
    text = re.sub(r'<[^>]*>', '\n', str(raw_html))
    return "\n".join([f"{i+1}. {l.strip()}" for i, l in enumerate(text.split('\n')) if l.strip()])

@st.cache_data(ttl=600)
def fetch_tr_data(url, user, pw, pid, sid):
    try:
        api = TestRailAPI(url.split('/index.php')[0].strip('/'), user, pw)
        all_cases = api.cases.get_cases(project_id=pid, suite_id=sid)
        # ... 這裡放入妳之前的 fetch 邏輯 ...
        return all_cases, "Success"
    except Exception as e:
        return None, str(e)