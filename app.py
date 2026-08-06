import streamlit as st
import pandas as pd
import os
import calendar
import io
from datetime import datetime
import plotly.graph_objects as go

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="Purchasing and S&R Dash Board", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* 1. 배경색 설정 */
    .stApp {
        background-color: #F4F5F7 !important;
    }

    /* Streamlit 고정 상단바의 위치 간섭 차단 및 배경 투명화 */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        position: absolute !important;
        z-index: 1 !important;
    }

    /* 본문 안전 여백 설정 */
    .block-container {
        padding-top: 4.5rem !important;  
        padding-bottom: 1.0rem !important;
        padding-left: 2.0rem !important;
        padding-right: 2.0rem !important;
    }
    
    /* 2. 상단 헤더 수평 정렬 */
    .header-flex-container {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        padding: 0px !important;
    }

    /* 메인 본문 타이틀 및 우측 컴퍼니 타이틀 디자인 (42px) */
    .dashboard-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        font-weight: 800 !important;
        color: #1A202C !important;
        font-size: 42px !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;     
    }
    
    .company-title-right {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        font-weight: 800 !important;
        color: #1A202C !important;
        font-size: 42px !important;          
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;     
        text-align: right !important;
        white-space: nowrap !important;
    }

    /* 3. 소제목 및 기본 글꼴 압축 */
    html, body, [data-testid="stMarkdownContainer"] p, .stAlert p {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-size: 14px !important;
        line-height: 1.3 !important;
        color: #2D3748 !important;
    }
    
    .section-title {
        font-size: 18px !important;
        font-weight: 800 !important;
        color: #1A202C !important;
        margin-bottom: 8px !important;
    }

    /* 4. 표 컴팩트 스타일 */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important; 
        padding: 5px !important;
    }
    
    div[data-testid="stDataFrame"] td, div[data-testid="stDataFrame"] th {
        font-size: 12px !important;
        padding: 2px 6px !important;
    }

    /* 5. 인원 카드 컴팩트화 */
    .metric-square {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        text-align: center;
        margin-bottom: 8px;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 800;
        color: #4A5568;
    }
    .metric-val {
        font-size: 38px;
        font-weight: 900;
        color: #1A202C;
        line-height: 1.0;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# 2. 파일 경로 설정
EXCEL_FILE_PATH = "dashboard raw data.xlsx"

# 오늘 날짜
today = datetime.today()
today_str = today.strftime('%Y-%m-%d')

# 상단 헤더
st.markdown("""
<div class="header-flex-container">
    <div class="dashboard-title">Purchasing and S&R Dash Board</div>
    <div class="company-title-right">Shinsegae Foods</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; font-weight: 600; color: #718096; margin-top: 2px; margin-bottom: 8px;">
    📅 TODAY: {today_str}
</div>
""", unsafe_allow_html=True)

# 데이터 구조 자동 보정 함수
def fix_excel_header(df):
    if df.empty:
        return df
    new_columns = df.iloc[0].fillna('').astype(str).tolist()
    new_columns = [col.strip() if col.strip() != '' and 'None' not in col else f"열_{i}" for i, col in enumerate(new_columns)]
    df.columns = new_columns
    df = df.drop(df.index[0]).reset_index(drop=True)
    df = df.loc[:, ~df.columns.str.startswith('열_')]
    for col in df.columns:
        if any(keyword in str(col) for keyword in ['일', '날짜', '기간']):
            try:
                converted = pd.to_datetime(df[col], errors='coerce')
                if converted.notna().sum() > 0:
                    df[col] = converted.dt.strftime('%Y-%m-%d').fillna(df[col])
            except:
                pass
    df.index = df.index + 1
    return df

if os.path.exists(EXCEL_FILE_PATH):
    try:
        with open(EXCEL_FILE_PATH, "rb") as f:
            file_bytes = io.BytesIO(f.read())
            
        xls = pd.ExcelFile(file_bytes)
        sheet_names = xls.sheet_names
        
        hr_sheet = "인사및일정" if "인사및일정" in sheet_names else sheet_names[0]
        stock_sheet = "재고현황" if "재고현황" in sheet_names else (sheet_names[1] if len(sheet_names) > 1 else sheet_names[0])
        schedule_sheet = "운영스케줄" if "운영스케줄" in sheet_names else (sheet_names[2] if len(sheet_names) > 2 else sheet_names[0])
        
        price_sheet = None
        for sheet in sheet_names:
            if "소전각" in sheet and "가격" in sheet:
                price_sheet = sheet
                break

        df_hr = pd.read_excel(file_bytes, sheet_name=hr_sheet)
        df_stock = pd.read_excel(file_bytes, sheet_name=stock_sheet)
        df_schedule = pd.read_excel(file_bytes, sheet_name=schedule_sheet)
        
        df_price = pd.read_excel(file_bytes, sheet_name=price_sheet) if price_sheet else None

        df_hr = fix_excel_header(df_hr)
        df_stock = fix_excel_header(df_stock)
        df_schedule = fix_excel_header(df_schedule)
        if df_price is not None:
            df_price = fix_excel_header(df_price)

        # ====================================================================
        # 1행: [인원 관리] (1/3)  +  [주요 아이템 현황] (2/3)
        # ====================================================================
        col_top_left, col_top_right = st.columns([1, 2])

        # --- [1행 좌측] 인원 관리 ---
        with col_top_left:
            st.markdown('<div class="section-title">👥 인원 관리</div>', unsafe_allow_html=True)
            
            status_col = [col for col in df_hr.columns if '상태' in str(col) or '근무' in str(col) or '구분' in str(col)]
            total_staff = len(df_hr)
            on_leave = df_hr[df_hr[status_col[0]].astype(str).str.upper().str.contains('OFF', na=False)].shape[0] if status_col else 0
            
            hr_sub_l, hr_sub_r = st.columns([1, 2.3])
            
            with hr_sub_l:
                st.markdown(f"""
                <div class="metric-square">
                    <div class="metric-label">총 인원</div>
                    <div class="metric-val">{total_staff}</div>
                </div>
                <div class="metric-square">
                    <div class="metric-label">결원</div>
                    <div class="metric-val">{on_leave}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with hr_sub_r:
                for idx, row_data in df_hr.iterrows():
                    name = str(row_data.get('이름', 'Unknown')).strip()
                    job = str(row_data.get('담당업무', '-')).strip()
                    status = str(row_data.get('현재상태', '근무중')).strip()
                    note = str(row_data.get('비고', '')).strip()
                    initial = name[0].upper() if name else '?'
                    
                    is_off = "OFF" in status.upper()
                    badge_bg = "#FEE2E2" if is_off else "#DCFCE7"
                    badge_color = "#DC2626" if is_off else "#16A34A"
                    badge_border = "#FCA5A5" if is_off else "#86EFAC"
                    
                    note_part = f"<div style='font-size: 11px; color: #475569; background:#F8FAFC; padding: 2px 6px; border-radius:4px; margin-top:2px;'>📝 {note}</div>" if (note and note.lower() not in ['none', 'nan', '', 'null']) else ""
                    
                    card_html = f"""<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:6px 10px; margin-bottom:5px; display:flex; align-items:center; gap:8px;"><div style="background:#EDF2F7; color:#4A5568; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:12px; flex-shrink:0;">{initial}</div><div style="flex-grow:1;"><div style="display:flex; align-items:center; gap:6px;"><span style="background-color:{badge_bg}; color:{badge_color}; border:1px solid {badge_border}; padding:1px 6px; border-radius:99px; font-size:10px; font-weight:800;">{status}</span><span style="font-size:13px; font-weight:700; color:#1A202C;">{name}</span></div><div style="font-size:11px; color:#718096;">{job}</div>{note_part}</div></div>"""
                    
                    st.markdown(card_html, unsafe_allow_html=True)

        # --- [1행 우측] 주요 아이템 현황 (기존: 재고 & 발주 현황) ---
        with col_top_right:
            # ★ [요청 변경 적용] 문구를 '주요 아이템 현황'으로 수정
            st.markdown('<div class="section-title">📦 주요 아이템 현황</div>', unsafe_allow_html=True)
            
            date_cols = [col for col in df_stock.columns if '발주일정' in str(col)]
            type_cols = [col for col in df_stock.columns if '분류' in str(col)]
            
            count_red = count_orange = count_yellow = count_green = 0
            if date_cols:
                for _, row in df_stock.iterrows():
                    d_val = row[date_cols[0]]
                    if pd.notna(d_val) and str(d_val).strip() not in ['', 'None', '-']:
                        try:
                            diff_days = (pd.to_datetime(d_val).date() - today.date()).days
                            if diff_days <= 0: count_red += 1
                            elif diff_days <= 3: count_orange += 1
                            elif diff_days <= 7: count_yellow += 1
                            else: count_green += 1
                        except: pass

            st.markdown(f"""
            <div style="display:flex; gap:10px; margin-bottom:8px;">
                <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:4px 10px; font-size:12px; font-weight:700;">🚨 당일/경과: <span style="color:#CC0000;">{count_red}개</span></div>
                <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:4px 10px; font-size:12px; font-weight:700;">⏰ 3일이내: <span style="color:#CC6600;">{count_orange}개</span></div>
                <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:4px 10px; font-size:12px; font-weight:700;">⚠️ 7일이내: <span style="color:#888800;">{count_yellow}개</span></div>
                <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:4px 10px; font-size:12px; font-weight:700;">✅ 8일이상: <span style="color:#22543D;">{count_green}개</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            def style_stock_table(row):
                styles = [''] * len(row)
                if type_cols:
                    t_idx = row.index.get_loc(type_cols[0])
                    t_val = str(row[type_cols[0]]).strip()
                    if '원재료' in t_val: styles[t_idx] = 'background-color: #EBF8FF; color: #2B6CB0; font-weight: bold;'
                    elif '부자재' in t_val: styles[t_idx] = 'background-color: #FFF5F5; color: #C53030; font-weight: bold;'
                if date_cols:
                    d_idx = row.index.get_loc(date_cols[0])
                    d_val = row[date_cols[0]]
                    if pd.notna(d_val) and str(d_val).strip() not in ['', 'None', '-']:
                        try:
                            diff_days = (pd.to_datetime(d_val).date() - today.date()).days
                            if diff_days <= 0: styles[d_idx] = 'background-color: #ffcccc; color: #cc0000; font-weight: bold;'
                            elif diff_days <= 3: styles[d_idx] = 'background-color: #ffe6cc; color: #cc6600; font-weight: bold;'
                            elif diff_days <= 7: styles[d_idx] = 'background-color: #fff9cc; color: #888800;'
                            else: styles[d_idx] = 'background-color: #f2f9f2; color: #227722;'
                        except: pass
                return styles
            
            st.dataframe(df_stock.style.apply(style_stock_table, axis=1), use_container_width=True, height=210)

        # ====================================================================
        # 2행: [소전각 가격 변동 트렌드]
        # ====================================================================
        st.markdown('<div class="section-title" style="margin-top:10px;">💰 소전각 가격 변동 트렌드</div>', unsafe_allow_html=True)
        
        if df_price is not None:
            date_col = [col for col in df_price.columns if '날짜' in str(col) or '일자' in str(col)]
            market_col = [col for col in df_price.columns if '시장가격' in str(col) or '시장 가격' in str(col) or '시중' in str(col)]
            buy_col = [col for col in df_price.columns if '구매가격' in str(col) or '구매 가격' in str(col) or '매입' in str(col)]
            
            if date_col and market_col and buy_col:
                d_col, m_col, b_col = date_col[0], market_col[0], buy_col[0]
                chart_df = df_price.copy()
                chart_df[d_col] = pd.to_datetime(chart_df[d_col], errors='coerce')
                chart_df = chart_df.dropna(subset=[d_col]).sort_values(by=d_col)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=chart_df[d_col], y=chart_df[m_col], mode='lines', name='시장가격', line=dict(color='#0d6dfd', width=2.5, shape='spline')))
                fig.add_trace(go.Scatter(x=chart_df[d_col], y=chart_df[b_col], mode='markers', name='구매가격', marker=dict(color='#EF4444', size=7, symbol='circle')))
                
                fig.update_layout(
                    title=dict(text="소전각 시장가 vs 구매가 비교", font=dict(size=14, weight='bold', color='#1A202C')),
                    xaxis=dict(gridcolor='#EDF2F7', tickfont=dict(size=11, color='#718096')),
                    yaxis=dict(gridcolor='#EDF2F7', tickfont=dict(size=11, color='#718096'), tickprefix="$", tickformat=",.2f"),
                    paper_bgcolor='white', plot_bgcolor='white', hovermode='x unified',
                    legend=dict(font=dict(size=12), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=220
                )
                st.plotly_chart(fig, use_container_width=True)

        # ====================================================================
        # 3행: [입출고 타임라인 달력]
        # ====================================================================
        st.markdown('<div class="section-title">⚙️ 입출고 타임라인</div>', unsafe_allow_html=True)
        
        target_date_col = next((col for col in df_schedule.columns if '예정일' in str(col) or '일' in str(col) or '날짜' in str(col)), None)
        type_col = [col for col in df_schedule.columns if '구분' in str(col) or '분류' in str(col)]
        item_col = [col for col in df_schedule.columns if '품목' in str(col) or '이름' in str(col)]
        qty_col = [col for col in df_schedule.columns if '수량' in str(col) or '개수' in str(col)]

        cal_df = df_schedule.copy()
        if target_date_col:
            cal_df['parsed_date'] = pd.to_datetime(cal_df[target_date_col], errors='coerce')

        if target_date_col and type_col and item_col:
            default_year = today.year
            default_month = today.month

            c_yr, c_m = st.columns([1, 1])
            year_range = list(range(default_year - 1, default_year + 2))
            
            default_year_idx = year_range.index(default_year) if default_year in year_range else 1
            
            view_year = c_yr.selectbox("연도 선택", year_range, index=default_year_idx, key="cal_yr")
            view_month = c_m.selectbox("월 선택", range(1, 13), index=default_month - 1, key="cal_m")

            cal = calendar.Calendar(firstweekday=6)
            month_days = cal.monthdayscalendar(view_year, view_month)

            html_code = """
            <style>
                .cal-table { width: 100%; border-collapse: separate; border-spacing: 0; background-color: white; table-layout: fixed; border-radius: 8px; overflow: hidden; border: 1px solid #E2E8F0; margin-bottom: 5px; }
                .cal-th { background-color: #F8FAFC; text-align: center; padding: 4px; font-weight: bold; border-bottom: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; width: 14.28%; font-size: 12px; color: #4A5568; }
                .cal-td { vertical-align: top; height: 65px; padding: 4px; border-bottom: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; position: relative; }
                .cal-day-num { font-weight: 700; font-size: 11px; margin-bottom: 2px; color: #4A5568; }
                .cal-today { background-color: #EFF6FF; border: 2px solid #3B82F6 !important; }
                .cal-event { font-size: 10px; padding: 1px 4px; margin-bottom: 2px; border-radius: 4px; color: white; font-weight: bold; line-height: 1.2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
                .ev-생산 { background-color: #10B981; } .ev-출고 { background-color: #EF4444; } .ev-입고 { background-color: #F59E0B; } .ev-default { background-color: #6B7280; }
            </style>
            <table class="cal-table">
                <thead>
                    <tr>
                        <th class="cal-th" style="color:#EF4444;">일</th><th class="cal-th">월</th><th class="cal-th">화</th><th class="cal-th">수</th>
                        <th class="cal-th">목</th><th class="cal-th">금</th><th class="cal-th" style="color:#3B82F6;">토</th>
                    </tr>
                </thead>
                <tbody>
            """

            for week in month_days:
                html_code += "<tr>"
                for day in week:
                    if day == 0:
                        html_code += "<td class='cal-td' style='background-color:#F8FAFC;'></td>"
                    else:
                        current_cell_date = f"{view_year}-{view_month:02d}-{day:02d}"
                        is_today = (view_year == today.year and view_month == today.month and day == today.day)
                        td_class = "cal-td cal-today" if is_today else "cal-td"
                        
                        html_code += f"<td class='{td_class}'>"
                        html_code += f"<div class='cal-day-num'>{day}</div>"
                        
                        day_events = cal_df[cal_df['parsed_date'].dt.strftime('%Y-%m-%d') == current_cell_date]
                        for _, row in day_events.iterrows():
                            ev_type = str(row[type_col[0]]).strip()
                            ev_item = str(row[item_col[0]])
                            ev_qty = f" ({row[qty_col[0]]})" if qty_col and pd.notna(row[qty_col[0]]) else ""
                            css_class = f"ev-{ev_type}" if f"ev-{ev_type}" in ['ev-생산', 'ev-출고', 'ev-입고'] else "ev-default"
                            html_code += f"<div class='cal-event {css_class}'>[{ev_type}] {ev_item}{ev_qty}</div>"
                        html_code += "</td>"
                html_code += "</tr>"
            html_code += "</tbody></table>"
            st.markdown(html_code, unsafe_allow_html=True)

        # 시스템 최하단 안내
        st.markdown(f"""
        <div style="background-color: #EDF2F7; padding: 6px 12px; border-radius: 8px; text-align: center; font-size: 12px; color: #718096; margin-top: 10px;">
            💡 <code>{EXCEL_FILE_PATH}</code> 파일을 수정하고 저장(Ctrl+S)하면 수 초 이내에 실시간 업데이트됩니다.
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ 엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.error(f"❌ 파일을 찾을 수 없습니다: 현재 폴더에 `{EXCEL_FILE_PATH}` 파일이 존재하는지 확인해 주세요.")
