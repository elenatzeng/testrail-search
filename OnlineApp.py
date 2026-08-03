import re
import streamlit as st

from auth_whitelist import is_authorized
from case_generator import CaseGenError, generate_test_cases, generate_test_outline, SYSTEM_PATHS
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
    st.error(f"⚠️ 匯入 testrail_write 失敗，請確認檔案已 Commit 至 GitHub 且分支正確：{e}")

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

            default_token = st.secrets.get("JIRA_API_TOKEN", "") if hasattr(st, "secrets") else ""
            jira_token = st.text_input(
                "Jira API Token",
                type="password",
                value=default_token or get_val("jira_token"),
                help="🔒 系統已預設讀取 Secrets 設定，若需更換可直接修改"
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

        # --- Step 3: 確認/編輯大綱 + 分頁生成設定 + 選擇 TestRail 推送目標 ---
        if "test_outline" in st.session_state:
            st.markdown("### 🧭 測試大綱（可編輯修訂）")
            outline_text = st.text_area(
                "測試大綱",
                value=st.session_state["test_outline"],
                height=200,
                key="outline_editor"
            )
            st.session_state["test_outline"] = outline_text

            st.markdown("---")
            st.markdown("### 🌐 系統端選擇")
            env_type = st.selectbox(
                "這個需求單屬於哪個系統端？",
                options=list(SYSTEM_PATHS.keys()),
                help="AI 只會從這個系統端底下的路徑清單挑選 path，選錯會導致案例被歸到「其他」或錯誤分類。"
            )

            st.markdown("---")
            st.markdown("### 📄 大綱分頁生成設定（防止 Token 截斷）")

            outline_lines = [line.strip() for line in outline_text.splitlines() if line.strip()]
            total_items = len(outline_lines)

            col_batch_size, col_page_select = st.columns([1, 2])
            with col_batch_size:
                batch_size = st.number_input(
                    "每頁包含大綱條數",
                    min_value=1,
                    max_value=10,
                    value=5,
                    help="建議設定 3~5 條，避免 AI 回覆過長導致中斷。"
                )

            page_options = ["全部一次產生"]
            if total_items > 0:
                num_pages = (total_items + batch_size - 1) // batch_size
                for p in range(num_pages):
                    start_i = p * batch_size + 1
                    end_i = min((p + 1) * batch_size, total_items)
                    page_options.append(f"第 {p+1} 頁 (處理第 {start_i} ~ {end_i} 條大綱，共 {total_items} 條)")

            if "current_page_idx" not in st.session_state:
                st.session_state["current_page_idx"] = 1 if len(page_options) > 1 else 0

            with col_page_select:
                selected_page = st.selectbox(
                    "請選擇本次要產生的分頁",
                    options=page_options,
                    index=min(st.session_state["current_page_idx"], len(page_options) - 1)
                )
                st.session_state["current_page_idx"] = page_options.index(selected_page)

            if selected_page == "全部一次產生" or total_items == 0:
                active_outline = outline_text
            else:
                page_idx = page_options.index(selected_page) - 1
                start_i = page_idx * batch_size
                end_i = min((page_idx + 1) * batch_size, total_items)
                selected_lines = outline_lines[start_i:end_i]
                active_outline = "\n".join(selected_lines)

            st.markdown("---")
            st.markdown("### 🎯 TestRail 推送目標與路徑選取")

            target_pid, target_sid = None, None
            selected_path_hint = None

            if not (tr_url and tr_user and tr_pw):
                st.warning("👈 請先在側邊欄填寫 TestRail 連線資訊（帳號/API Key），才能載入 Project 與路徑清單。")
            else:
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

                    if target_pid and target_sid:
                        sec_cache_key = f"tr_sections_path_{target_pid}_{target_sid}"
                        if sec_cache_key not in st.session_state:
                            try:
                                with st.spinner("正在讀取 TestRail 分類路徑..."):
                                    sec_map = fetch_sections(tr_url, tr_user, tr_pw, target_pid, target_sid)
                                    st.session_state[sec_cache_key] = sec_map
                            except Exception as e:
                                st.session_state[sec_cache_key] = {}

                        existing_paths = sorted(list(set(st.session_state.get(sec_cache_key, {}).values())))

                        path_options = ["🤖 [自動由 AI 判斷路徑]", "✍️ [手動輸入新路徑...]"] + existing_paths
                        chosen_option = st.selectbox(
                            "📂 選擇測試案例存放路徑 (Section)",
                            options=path_options,
                            index=0,
                            help="可直接點選現有的 TestRail 分類路徑，避免手動輸入錯誤。"
                        )

                        if chosen_option == "✍️ [手動輸入新路徑...]":
                            selected_path_hint = st.text_input(
                                "手動輸入新路徑（格式：父層 > 子層，例如「行銷推廣 > 優惠券管理」）",
                                placeholder="轉帳 > 充值"
                            )
                        elif chosen_option != "🤖 [自動由 AI 判斷路徑]":
                            selected_path_hint = chosen_option

                    if st.button("🔄 重新整理專案與分類清單"):
                        st.session_state.pop("tr_projects", None)
                        for k in list(st.session_state.keys()):
                            if k.startswith("tr_suites_") or k.startswith("tr_sections_"):
                                st.session_state.pop(k, None)
                        st.rerun()
                else:
                    if st.session_state.get("tr_projects_error"):
                        st.warning(f"無法自動讀取 Project 清單：{st.session_state['tr_projects_error']}")
                    col_p_m, col_s_m = st.columns(2)
                    target_pid = col_p_m.number_input("Project ID", value=int(pid), key="target_pid_manual")
                    target_sid = col_s_m.number_input("Suite ID", value=int(sid), key="target_sid_manual")
                    selected_path_hint = st.text_input("路徑（格式：父層 > 子層）", placeholder="轉帳 > 充值")

            st.markdown("---")

            col_prev, col_main_btn, col_next = st.columns([1.5, 7, 1.5], vertical_alignment="center")
            curr_idx = st.session_state.get("current_page_idx", 0)

            with col_prev:
                if st.button("⬅️ 上一頁", disabled=(curr_idx <= 1)):
                    st.session_state["current_page_idx"] = curr_idx - 1
                    st.rerun()

            with col_next:
                if st.button("➡️ 下一頁", disabled=(curr_idx >= len(page_options) - 1 or curr_idx == 0)):
                    st.session_state["current_page_idx"] = curr_idx + 1
                    st.rerun()

            with col_main_btn:
                if st.button(f"✅ 確認【{selected_page}】與目標，產生完整測試案例", use_container_width=True):
                    try:
                        with st.spinner("AI 正在產生測試案例..."):
                            s = st.session_state["jira_summary"]

                            cases = generate_test_cases(
                                s['summary'],
                                s['description'],
                                active_outline,
                                env_type=env_type,
                                path_hint=selected_path_hint,
                            )
                            st.session_state["generated_cases"] = cases
                            st.session_state["target_pid_final"] = target_pid
                            st.session_state["target_sid_final"] = target_sid
                            st.session_state["selected_path_hint"] = selected_path_hint

                            # 💡 每次新產生案例時，清除之前的全選與個案勾選紀錄
                            st.session_state["select_all_cases"] = False
                            for k in list(st.session_state.keys()):
                                if k.startswith("case_select_"):
                                    st.session_state.pop(k, None)
                    except CaseGenError as e:
                        st.error(str(e))

        # --- Step 4: 顯示產生結果 + 全選/選擇性推送至 TestRail ---
        if "generated_cases" in st.session_state:
            st.markdown("### ✅ 產生結果與推送")
            cases = st.session_state["generated_cases"]
            target_pid = st.session_state.get("target_pid_final", target_pid)
            target_sid = st.session_state.get("target_sid_final", target_sid)
            override_path = st.session_state.get("selected_path_hint")

            # 🛠️ 回調函式：當全選狀態改變時，強制更新每一個案例的 Session State 並 rerun
            def on_select_all_change():
                new_status = st.session_state.get("select_all_cases", False)
                for idx in range(len(cases)):
                    st.session_state[f"case_select_{idx}"] = new_status

            col_sel_all, col_batch_btn = st.columns([2, 3], vertical_alignment="center")
            with col_sel_all:
                st.checkbox(
                    "全選所有案例",
                    value=st.session_state.get("select_all_cases", False),
                    key="select_all_cases",
                    on_change=on_select_all_change
                )

            def push_case_to_tr(case_item, path_to_use):
                cache_key = f"push_path_map_{target_pid}_{target_sid}"
                if cache_key not in st.session_state:
                    st.session_state[cache_key] = fetch_sections(
                        tr_url, tr_user, tr_pw, target_pid, target_sid
                    )
                target_path_map = st.session_state[cache_key]

                target_section_id = get_or_create_section(
                    tr_url, tr_user, tr_pw, target_pid, target_sid, target_path_map,
                    path_to_use
                )

                preconds_raw = case_item.get("preconditions", [])
                if isinstance(preconds_raw, list):
                    preconds_str = "\n".join(
                        f"{i}. {p}" if not str(p).startswith(f"{i}.") else str(p)
                        for i, p in enumerate(preconds_raw, 1)
                    )
                else:
                    preconds_str = str(preconds_raw or "")

                return create_test_case(
                    tr_url, tr_user, tr_pw,
                    target_section_id,
                    case_item.get("title", "未命名案例"),
                    preconds_str,
                    case_item.get("steps", []),
                    template_id=2,
                )

            selected_indices = []

            for idx, case in enumerate(cases):
                final_push_path = override_path or case.get("path") or "未分類"

                # 💡 每個案例的 key，預設皆為 False (預設不勾選)
                case_key = f"case_select_{idx}"
                if case_key not in st.session_state:
                    st.session_state[case_key] = False

                with st.container(border=True):
                    head_col1, head_col2 = st.columns([0.5, 9.5])
                    with head_col1:
                        is_selected = st.checkbox(
                            "",
                            key=case_key,
                            label_visibility="collapsed"
                        )
                        if is_selected:
                            selected_indices.append(idx)

                    with head_col2:
                        st.markdown(f"**{case.get('title', '(未命名案例)')}**")
                        st.caption(f"📍 預計寫入路徑：**{final_push_path}**")

                    st.markdown("**Preconditions**")
                    for i, pc in enumerate(case.get("preconditions", []), 1):
                        st.markdown(f"{i}. {pc}")

                    st.markdown("**Steps**")
                    for s_idx, step in enumerate(case.get("steps", []), 1):
                        c1, c2 = st.columns(2)
                        c1.markdown(f"**Step {s_idx}**\n\n{step.get('content', '')}")
                        c2.markdown(f"**Expected**\n\n{step.get('expected', '')}")

                    if st.button(f"📤 單獨推送案例 #{idx+1}", key=f"push_single_{idx}"):
                        if not (tr_url and tr_user and tr_pw):
                            st.warning("請先在側邊欄填寫 TestRail 連線資訊。")
                        elif not target_pid or not target_sid:
                            st.warning("無法取得正確的 Project / Suite ID，請確認連線。")
                        else:
                            try:
                                with st.spinner(f"正在寫入 TestRail（分類：{final_push_path}）..."):
                                    res = push_case_to_tr(case, final_push_path)
                                st.success(f"✅ 已成功建立測試案例 #{res.get('id')}！")
                            except (TestRailWriteError, NameError) as e:
                                st.error(str(e))

            with col_batch_btn:
                if st.button(f"🚀 批次推送已勾選案例 ({len(selected_indices)}/{len(cases)})", use_container_width=True):
                    if not (tr_url and tr_user and tr_pw):
                        st.warning("請先在側邊欄填寫 TestRail 連線資訊。")
                    elif not target_pid or not target_sid:
                        st.warning("無法取得正確的 Project / Suite ID，請確認連線。")
                    elif not selected_indices:
                        st.warning("請至少勾選一個測試案例進行推送。")
                    else:
                        success_count = 0
                        error_msgs = []
                        progress_bar = st.progress(0, text="正在進行批次推送...")

                        for progress_idx, case_idx in enumerate(selected_indices, 1):
                            target_case = cases[case_idx]
                            final_path = override_path or target_case.get("path") or "未分類"
                            try:
                                progress_bar.progress(
                                    progress_idx / len(selected_indices),
                                    text=f"正在推送第 ({progress_idx}/{len(selected_indices)}) 個案例：{target_case.get('title')}"
                                )
                                push_case_to_tr(target_case, final_path)
                                success_count += 1
                            except Exception as e:
                                error_msgs.append(f"案例【{target_case.get('title')}】推送失敗：{str(e)}")

                        progress_bar.empty()
                        if success_count > 0:
                            st.success(f"🎉 成功批次推送 {success_count} 個測試案例至 TestRail！")
                        if error_msgs:
                            for err in error_msgs:
                                st.error(err)
