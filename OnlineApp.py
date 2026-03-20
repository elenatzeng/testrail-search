# --- 6. 主介面邏輯 ---
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    data_container = st.empty()
    data_container.info("⏳ 正在同步 TestRail 數據...")
    all_cases, path_map, user_map, sync_time, project_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases:
        data_container.empty()
        st.markdown(f'<div class="location-tag">📍 <b>Project：</b>{project_name} | <b>Suite：</b>#{suite_id}</div>', unsafe_allow_html=True)
        
        # 🚀 布局优化：搜索框与按钮整齐排列
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2])
        
        # 初始化 Session State (用于控制搜索框内容)
        if "query_text" not in st.session_state:
            st.session_state.query_text = ""

        with col_search:
            query = st.text_input(
                "🔍 搜尋內容 (輸入 Key、地道繁體或 #ID):", 
                value=st.session_state.query_text,
                placeholder="多關鍵字請以空格分隔 (交集搜尋)",
                key="search_box"
            )
            # 实时同步输入值到 session_state
            st.session_state.query_text = query

        with col_clear:
            # st.write("") 的作用是把按钮往下推，对齐输入框
            st.markdown('<p style="margin-bottom: 28px;"></p>', unsafe_allow_html=True) 
            if st.button("🗑️ 清除條件", use_container_width=True):
                st.session_state.query_text = ""
                # 这里强制刷新页面以清空输入框
                st.rerun()

        with col_run:
            st.markdown('<p style="margin-bottom: 28px;"></p>', unsafe_allow_html=True)
            if st.button("🔎 重新查詢", use_container_width=True):
                st.rerun()

        # 使用当前 session_state 中的值进行搜索
        final_query = st.session_state.query_text

        if final_query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            
            # 🚀 1. 拆分原始輸入關鍵字 (交集逻辑)
            raw_input_terms = final_query.strip().split()
            
            scored_results = []
            for c in all_cases:
                cid = str(c.get('id', ''))
                title = c.get('title', '').lower()
                section_path = path_map.get(c.get('section_id'), "").lower()
                full_text = str(c).lower()
                
                # 🚀 2. 核心邏輯：交集檢查
                is_all_match = True
                combined_score = 0 
                
                for term in raw_input_terms:
                    expanded_terms = multi_lang_search(term)
                    match_this_term = False
                    
                    if term.strip('#') == cid:
                        combined_score += 100000
                        match_this_term = True
                    elif any(et in section_path for et in expanded_terms):
                        combined_score += 50000
                        match_this_term = True
                    elif any(et in title for et in expanded_terms):
                        combined_score += 10000
                        match_this_term = True
                    elif any(et in full_text for et in expanded_terms):
                        combined_score += 1000
                        match_this_term = True
                    
                    if not match_this_term:
                        is_all_match = False
                        break
                
                if is_all_match:
                    score = combined_score
                    author_id = c.get('created_by')
                    u_info = USER_CONFIG.get(author_id, DEFAULT_CONFIG)
                    
                    raw_steps = c.get('custom_steps_separated') or c.get('custom_steps') or c.get('steps') or []
                    steps_count = len(raw_steps) if isinstance(raw_steps, list) else 0
                    content_len = len(str(raw_steps))
                    
                    score += (steps_count * 500) + (content_len // 10)
                    score += u_info.get("weight", 0)
                    
                    if not u_info.get("is_active", True): score -= 45000
                    if steps_count == 0 or content_len < 15: score -= 40000 
                    
                    scored_results.append((score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            
            if scored_results:
                st.write(f"### 🎯 找到 {len(scored_results)} 個案例")
                for _, item, u_info in scored_results:
                    cid = str(item.get('id'))
                    
                    if u_info.get("is_active", True):
                        status_emoji = "🟢"
                        author_style = "color: #4CAF50; background: rgba(76, 175, 80, 0.15); border: 1.5px solid #4CAF50;"
                    else:
                        status_emoji = "🔴"
                        author_style = "color: #ff4b4b; background: rgba(255, 75, 75, 0.15); border: 1.5px solid #ff4b4b;"

                    with st.container():
                        st.markdown(f'<span style="font-size:12px; color:#8b949e;">{path_map.get(item.get("section_id"), "Unknown")}</span>', unsafe_allow_html=True)
                        col_t, col_b = st.columns([7, 1.5])
                        with col_t:
                            st.markdown(f'''
                                <div style="font-size:16px; font-weight:bold;">
                                    {item.get("title")} 
                                    <small style="color:#8b949e">(#{cid})</small> 
                                    <span class="author-tag" style="{author_style}">
                                        {status_emoji} {u_info["name"]}
                                    </span>
                                </div>
                            ''', unsafe_allow_html=True)
                        with col_b:
                            st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                        with st.expander("🔽 查看測試步驟"):
                            raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or item.get('steps')
                            if isinstance(raw_steps, list) and len(raw_steps) > 0:
                                for i, s in enumerate(raw_steps, 1):
                                    st.markdown(f'<div class="step-item"><span style="color:#79c0ff; font-weight:800;">Step {i}:</span><div class="step-content-box">{clean_html_and_add_numbers(s.get("content", s.get("step", "")))}</div><div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div><div class="step-content-box" style="border-left: 2px solid #4CAF50;">{clean_html_and_add_numbers(s.get("expected", ""))}</div></div>', unsafe_allow_html=True)
                            else: st.info("無步驟資料。")
                        st.markdown("---")
            else: st.warning("查無符合所有交集條件的結果。")
    else: st.error(f"❌ 同步失敗")
else: st.warning("👈 請輸入連線資訊。")
