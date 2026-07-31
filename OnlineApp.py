import re
import streamlit as st

from auth_whitelist import is_authorized
from case_generator import CaseGenError, generate_test_cases, generate_test_outline
from jira_client import JiraError, extract_issue_summary, fetch_issue
from keywords import SEARCH_DICTIONARY
from style import apply_custom_style
from users import DEFAULT_CONFIG, USER_CONFIG
from utils import clean_html, fetch_data_from_tr, multi_lang_search

# --- 安全匯入 testrail_write 模組 ---
try:
    from testrail_write import (
        TestRailWriteError,
        create_test_case,
        fetch_sections,
        get_or_create_section,
        list_projects,
        list_suites,
    )
except ImportError as e:
    st.error(f"⚠️ 匯入 testrail_write 失敗，請確認檔案已 Commit 至 github 且分支正確：{e}")

# 1. 頁面初始化
st.set_page_config(
    page_title="TestRail AI Search",
    layout="wide",
    page_icon="🧪",
    initial_sidebar_state="expanded"
)
apply_custom_style()

PREVIEW_IMAGE_URL = "https://raw.githubusercontent.com/elenatzeng/testrail-search/main/CoverPic.jpg"
st.markdown(f"""
<head>
<meta property="og:title" content="TestRail AI Search" />
<meta property="og:description" content="🧪 智能檢索測試案例中心 - 快速查找您的 TestRail Cases" />
<meta property="og:image" content="{PREVIEW_IMAGE_URL}" />
<meta property="og:image:secure_url" content="{PREVIEW_IMAGE_URL}" />
<meta property="og:image:type" content="image/jpeg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="{PREVIEW_IMAGE_URL}" />
</head>
""", unsafe_allow_html=True)

st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)


def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))


# 2. 側邊欄守護 (連線設定)
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)

    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")

    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 預設變數初始化
all_cases, path_map, sync_time, p_name = [], {}, "", ""

tab1, tab2 = st.tabs(["🔍 案例查詢", "🤖 AI 產生測試案例 (Jira)"])

# ============================================================
# Tab 1：TestRail 案例查詢功能
# ============================================================
with tab1:
    if tr_url and tr_user and tr_pw:
        with st.spinner("🚀 正在從 TestRail 同步數據..."):
            all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)

        if all_cases is None:
            st.error(f"❌ 無法連線至 TestRail。原因：{sync_time}")
            st.info("💡 請檢查側邊欄的連線資訊是否正確。")
        elif not all_cases:
            st.warning(f"⚠️ 在 Suite #{sid} 中找不到任何測試案例。")
        else:
            st.markdown(
                f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | "
                f"Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>",
                unsafe_allow_html=True
            )
            col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
            if "q_text" not in st.session_state:
                st.session_state.q_text = ""
            if "search_key" not in st.session_state:
                st.session_state.search_key = 0

            with col_s:
                st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
                q_input = st.text_input(
                    "",
                    value=st.session_state.q_text,
                    placeholder="請輸入關鍵字查詢，若多個關鍵字請以空格格開",
                    label_visibility="collapsed",
                    key=f"search_input_{st.session_state.search_key}"
                )
                st.session_state.q_text = q_input

            with col_c:
                if st.button("🗑️ 清除條件", use_container_width=True):
                    st.session_state.q_text = ""
                    st.session_state.search_key += 1
                    st.rerun()

            with col_r:
                if st.button("🔎 查詢", use_container_width=True):
                    st.rerun()

            if st.session_state.q_text:
                terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
                results = []
                img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

                for c in all_cases:
                    title, cid = str(c.get('title', '')), str(c.get('id'))
                    f_path = path_map.get(c.get('section_id'), "")
                    match_score = 0
                    is_match = True
                    for t in terms:
                        exp = multi_lang_search(t, SEARCH_DICTIONARY)
                        if any(w in title.lower() or w in f_path.lower() or w == cid for w in exp):
                            if any(w in title.lower() for w in exp):
                                match_score += 10
                            else:
                                match_score += 1
                        else:
                            is_match = False
                            break
                    if is_match:
                        u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                        steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                        quality_weight = 10000 if len(str(steps_raw)) > 10 else 0
                        results.append((match_score + quality_weight, f_path, c, u))

                results.sort(key=lambda x: (-x[0], x[1]))

                if not results:
                    st.markdown('🚫 找不到符合的測試案例。')
                else:
                    for _, path, item, u in results:
                        cid = str(item.get('id'))
                        st.markdown(
                            f'<div style="font-size:13px; color:#adb5bd; margin-top:20px; margin-bottom:5px;">📁 {path}</div>',
                            unsafe_allow_html=True
                        )
                        tag = (
                            f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">'
                            f'{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                        )
                        c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                        c1.markdown(
                            f'<div style="display:flex; align-items:center; margin-bottom:15px;">'
                            f'<span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>',
                            unsafe_allow_html=True
                        )
                        c2.markdown(
                            f'''<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>''',
                            unsafe_allow_html=True
                        )

                        with st.expander("查閱測試步驟", expanded=False):
                            steps_data = item.get('custom_steps') or item.get('custom_steps_separated')

                            def final_render(text):
                                if not text:
                                    return "(無內容)"
                                text = re.sub(img_kill_pattern, '', str(text), flags=re.IGNORECASE).strip()
                                lines = text.splitlines()
                                html_out = '<div class="inner-text" style="font-weight: 400;">'
                                for line in lines:
                                    s = line.strip()
                                    if not s:
                                        continue
                                    is_list = re.match(r'^([•\-\*]|\d+\.)', s)
                                    style = "margin-bottom:4px; display:block; font-size:14px;"
                                    if is_list:
                                        style += "padding-left:18px;"
                                    html_out += f'<div style="{style}">{s}</div>'
                                html_out += '</div>'
                                return html_out

                            if isinstance(steps_data, list) and len(steps_data) > 0:
                                for s_idx, s in enumerate(steps_data, 1):
                                    st.markdown(f'''
                                    <div style="border-left:4px solid #2ea44f; padding-left:20px; margin-left:5px; margin-bottom:30px;">
                                        <div style="color:#8b949e; font-size:13px;">Step {s_idx}:</div>
                                        <div class="content-box">{final_render(s.get('content', ''))}</div>
                                        <div style="color:#8b949e; font-size:13px; margin-top:20px;">Expected:</div>
                                        <div class="content-box">{final_render(s.get('expected', ''))}</div>
                                    </div>
                                    ''', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="content-box">{final_render(steps_data)}</div>', unsafe_allow_html=True)
                        st.markdown("---")
    else:
        st.info("👈 請先在左側完成連線設定。")

# ============================================================
# Tab 2：Jira 需求單 → AI 產生測試案例 → 推送 TestRail
# ============================================================
with tab2:
    st.subheader("🤖 從 Jira 需求單自動產生測試案例")

    user_email = st.text_input("請輸入您的 Email 以使用此功能", key="jira_user_email")

    if not user_email:
        st.info("請先輸入 Email 進行身分確認。")
    elif not is_authorized(user_email):
        st.error("⛔ 您沒有使用此功能的權限。")
    else:
        st.success(f"✅ 已授權：{user_email}")

        with st.expander("🔧 Jira 連線設定", expanded=True):
            jira_url = st.text_input(
                "Jira 網域網址", value=get_val("jira_url"),
                placeholder="https://yourteam.atlassian.net"
            )
            jira_email = st.text_input("Jira 帳號 Email", value=get_val("jira_email") or user_email)
            jira_token = st.text_input(
                "Jira API Token",
                type="password",
                value=st.secrets.get("JIRA_API_TOKEN", "") if hasattr(st, "secrets") else ""
            )
            issue_key = st.text_input("需求單編號", placeholder="例如：PROJ-123")

        # --- Step 1: 讀取需求單 ---
        if st.button("📥 讀取需求單", use_container_width=False):
            if not (jira_url and jira_email and jira_token and issue_key):
                st.warning("請完整填寫 Jira 網域、帳號、API Token 與需求單編號。")
            else:
                try:
                    with st.spinner("正在讀取 Jira 需求單..."):
                        issue_json = fetch_issue(jira_url, jira_email, jira_token, issue_key)
                        st.session_state["jira_summary"] = extract_issue_summary(issue_json)
                        st.session_state.pop("test_outline", None)
                        st.session_state.pop("generated_cases", None)
                except JiraError as e:
                    st.error(str(e))

        if "jira_summary" in st.session_state:
            s = st.session_state["jira_summary"]
            st.markdown(f"### 📋 {s['key']}｜{s['summary']}")
            st.caption(f"類型：{s['issue_type']} ｜ 狀態：{s['status']} ｜ 提出人：{s['reporter']}")
            with st.expander("查看原始需求描述", expanded=False):
                st.text(s['description'] or "(無描述)")

            # --- Step 2: 產生測試大綱 ---
            if st.button("🧭 產生測試大綱"):
                try:
                    with st.spinner("AI 正在分析需求並整理測試重點..."):
                        outline = generate_test_outline(s['summary'], s['description'])
                        st.session_state["test_outline"] = outline
                except CaseGenError as e:
                    st.error(str(e))

        # --- Step 3: 確認/編輯大綱 ---
        if "test_outline" in st.session_state:
            st.markdown("### 🧭 測試大綱（請先確認或修改，再產生完整案例）")
            outline_text = st.text_area(
                "測試大綱",
                value=st.session_state["test_outline"],
                height=220,
                key="outline_editor"
            )
            st.session_state["test_outline"] = outline_text

            col_a, col_b = st.columns([1, 2])
            with col_a:
                path_mode = st.radio("測試案例路徑", ["自動判斷", "手動指定"], horizontal=True)
            with col_b:
                manual_path = st.text_input(
                    "路徑（格式：父層 > 子層，例如「行銷推廣 > 優惠券管理」）",
                    disabled=(path_mode == "自動判斷"),
                    placeholder="行銷推廣 > 優惠券管理",
                    help="請填 TestRail 分類的路徑名稱，不要貼網址。"
                )

            if st.button("✅ 確認大綱，產生完整測試案例"):
                try:
                    with st.spinner("AI 正在產生測試案例..."):
                        s = st.session_state["jira_summary"]
                        cases = generate_test_cases(
                            s['summary'],
                            s['description'],
                            st.session_state["test_outline"],
                            path_hint=(manual_path if path_mode == "手動指定" else None),
                        )
                        st.session_state["generated_cases"] = cases
                except CaseGenError as e:
                    st.error(str(e))

        # --- Step 4: 顯示產生結果 + 推送 TestRail ---
        if "generated_cases" in st.session_state:
            st.markdown("### 🎯 TestRail 推送目標")
            st.caption("這裡選的 Project / Suite 跟左側「案例查詢」用的完全獨立，不會互相影響。")

            if not (tr_url and tr_user and tr_pw):
                st.warning("請先在側邊欄填寫 TestRail 連線資訊（帳號/API Key），這裡才能抓 Project 清單。")
                target_pid, target_sid = None, None
            else:
                target_pid, target_sid = None, None

                if "tr_projects" not in st.session_state:
                    try:
                        st.session_state["tr_projects"] = list_projects(tr_url, tr_user, tr_pw)
                    except (TestRailWriteError, NameError) as e:
                        st.session_state["tr_projects_error"] = str(e)

                if st.session_state.get("tr_projects"):
                    proj_map = {p["name"]: p["id"] for p in st.session_state["tr_projects"]}
                    col_p, col_s = st.columns(2)

                    with col_p:
                        proj_name = st.selectbox("Project", list(proj_map.keys()), key="target_project_select")
                        target_pid = proj_map[proj_name]

                    suite_cache_key = f"tr_suites_{target_pid}"
                    if suite_cache_key not in st.session_state:
                        try:
                            st.session_state[suite_cache_key] = list_suites(tr_url, tr_user, tr_pw, target_pid)
                        except (TestRailWriteError, NameError) as e:
                            st.error(str(e))
                            st.session_state[suite_cache_key] = []

                    with col_s:
                        suites = st.session_state[suite_cache_key]
                        if suites:
                            suite_map = {sv["name"]: sv["id"] for sv in suites}
                            suite_name = st.selectbox("Suite", list(suite_map.keys()), key="target_suite_select")
                            target_sid = suite_map[suite_name]
                        else:
                            st.info("這個 Project 底下沒有 Suite。")

                    if st.button("🔄 重新整理清單"):
                        st.session_state.pop("tr_projects", None)
                        for k in list(st.session_state.keys()):
                            if k.startswith("tr_suites_"):
                                st.session_state.pop(k, None)
                        st.rerun()
                else:
                    if st.session_state.get("tr_projects_error"):
                        st.warning(f"無法自動讀取 Project 清單，改用手動輸入：{st.session_state['tr_projects_error']}")
                    target_pid = st.number_input("Project ID", value=int(pid), key="target_pid_manual")
                    target_sid = st.number_input("Suite ID", value=int(sid), key="target_sid_manual")

            st.markdown("### ✅ 產生結果")
            cases = st.session_state["generated_cases"]

            for idx, case in enumerate(cases):
                with st.container(border=True):
                    st.markdown(f"**{case.get('title', '(未命名案例)')}**")
                    st.caption(f"路徑建議：{case.get('path') or '(未指定，將建立於「未分類」)'}")

                    st.markdown("**Preconditions**")
                    for i, pc in enumerate(case.get("preconditions", []), 1):
                        st.markdown(f"{i}. {pc}")

                    st.markdown("**Steps**")
                    for s_idx, step in enumerate(case.get("steps", []), 1):
                        c1, c2 = st.columns(2)
                        c1.markdown(f"**Step {s_idx}**\n\n{step.get('content', '')}")
                        c2.markdown(f"**Expected**\n\n{step.get('expected', '')}")

                    if st.button("📤 推送至 TestRail", key=f"push_{idx}"):
                        if not (tr_url and tr_user and tr_pw):
                            st.warning("請先在側邊欄填寫 TestRail 連線資訊。")
                        elif not target_pid or not target_sid:
                            st.warning("請先在上方選擇（或輸入）要推送的 Project / Suite。")
                        else:
                            try:
                                with st.spinner("正在寫入 TestRail..."):
                                    cache_key = f"push_path_map_{target_pid}_{target_sid}"
                                    if cache_key not in st.session_state:
                                        st.session_state[cache_key] = fetch_sections(
                                            tr_url, tr_user, tr_pw, target_pid, target_sid
                                        )
                                    target_path_map = st.session_state[cache_key]

                                    target_section_id = get_or_create_section(
                                        tr_url, tr_user, tr_pw, target_pid, target_sid, target_path_map,
                                        case.get("path") or "未分類"
                                    )
                                    result = create_test_case(
                                        tr_url, tr_user, tr_pw,
                                        target_section_id,
                                        case.get("title", "未命名案例"),
                                        "\n".join(case.get("preconditions", [])),
                                        case.get("steps", []),
                                    )
                                st.success(
                                    f"✅ 已建立測試案例 #{result.get('id')}"
                                    f"（Project {target_pid} / Suite {target_sid}）"
                                )
                            except (TestRailWriteError, NameError) as e:
                                st.error(str(e))
