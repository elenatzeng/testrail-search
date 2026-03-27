import re, time, streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def match_visual_only(text, keyword):
    if not text or not keyword: return False
    # 徹底剝皮：還原轉義字元 -> 殺掉所有標籤 -> 規格化
    clean = unescape(str(text))
    clean = re.sub(r'<[^>]*>', ' ', clean) 
    clean = " ".join(clean.split()).lower()
    # \b 鎖死
    return re.search(rf'\b{re.escape(str(keyword).lower())}\b', clean)

def smart_format(text):
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    if len(t_lower) == 3 and t_lower.isalpha(): # 幣別鎖死
        return [t_lower]
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)
