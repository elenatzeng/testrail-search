import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search, match_keyword
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 初始化
st.set_page_config(page_title="TestRail Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key): return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url, tr_user, tr_pw = st.text_input("URL", value=get_val("url")), st.text_input("Email", value=get_val("user")), st.text_input("API Key", type="password", value=get_val("pw"))
    pid, sid = st.number_input("Project ID", value=int(get_val("pid") or 10)), st.number_input("Suite ID", value=int(get_val("sid") or 10))
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 純淨檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        st.markdown(f"📍 Project：{p_name} | Suite：#{sid}", unsafe_allow_html=True)
        q_input = st.text_input("● 搜尋內容:", value=st.session_state.get("q_text", ""), placeholder="例如: 充值 CNY")
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                # 💡 這裡就是妳要的：只抓「純文字」欄位
                cid = str(c.get('id'))
                title = str(c.get('title', ''))
                f_path = str(path_map.get(c.get('section_id'), ""))
                # 內容處理
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                steps_text = str(steps_raw)
                
                # --- ⚔️ 硬核交集判定 ---
                is_all_passed, score = True, 0
                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    # 每一組詞都必須在「純文字」的標題、路徑或內容中「精確命中」
                    hit = any(match_keyword(title, v) or match_keyword(f_path, v) or match_keyword(steps_text, v) for v in variants) or (t == cid)
                    
                    if hit:
                        if any(match_keyword(title, v) for v in variants): score += 10
                        elif any(match_keyword(f_path, v) for v in variants): score += 1
                    else:
                        is_all_passed = False
                        break
                
                if is_all_passed:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    quality = 10000 if len(steps_text) > 20 else 0
                    results.append((score + quality, f_path, c, u))

            results.sort(key=lambda x: (-x[0], x[1]))
            st.success(f"找到 {len(results)} 筆精確符合案例 (已排除 HTML)")
            
            for _, path, item, u in results:
                cid_str = str(item.get('id'))
                tag = f'<span class="author-tag status-{"active" if u.get("is_active", True) else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                st.markdown(f'<div style="color:#adb5bd; font-size:12px; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                c1.markdown(f'<div style="display:flex; align-items:center;"><h4>{item.get("title")} (#{cid_str})</h4>{tag}</div>', unsafe_allow_html=True)
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid_str}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                with st.expander("查看步驟"):
                    # 顯示時使用美化後的文字
                    st.write(smart_format(str(item.get('custom_steps') or item.get('custom_steps_separated'))))
                st.markdown("---")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端">🚀</a>', unsafe_allow_html=True)
