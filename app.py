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

    /* 6. 원부자재 구매액 25년 (기본 스타일) */
    .grid-purchase-card {
        background-color: #FFFFFF;
        border: 1.5px solid #CBD5E1;
        border-radius: 12px;
        padding: 10px 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 10px;
    }
    .grid-purchase-title {
        font-size: 13px;
        font-weight: 800;
        color: #64748B;
        margin-bottom: 2px;
    }
    .grid-purchase-val {
        font-size: 20px;
        font-weight: 900;
        color: #334155;
        line-height: 1.1;
    }
    .grid-purchase-sub {
        font-size: 10px;
        color: #94A3B8;
        font-weight: 600;
        margin-top: 3px;
    }

    /* 7. 원부자재 구매액 26년 (2026 하이라이트 스타일) */
    .grid-purchase-card-highlight {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0F7FF 100%);
        border: 2px solid #0D6DFD;
        border-radius: 12px;
        padding: 10px 12px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(13, 109, 253, 0.12);
        margin-bottom: 10px;
    }
    .grid-purchase-title-hl {
        font-size: 13px;
        font-weight: 900;
        color: #0F172A;
        margin-bottom: 2px;
    }
    .grid-purchase-val-hl {
        font-size: 21px;
        font-weight: 900;
        color: #0D6DFD;
        line-height: 1.1;
    }
    .grid-purchase-sub-hl {
        font-size: 10.5px;
        color: #3B82F6;
        font-weight: 700;
        margin-top: 3px;
    }

    /* 8. 드롭다운(Selectbox) 박스 배경 흰색 지정 */
    div[data-testid="stSelectbox"] div[role="combobox"],
    div[data-testid="stSelectbox"] > div > div,
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }
    div[data-testid="stSelectbox"] div[role="combobox"] * {
        background-color: transparent !important;
        color: #1E293B !important;
        font-weight: 700 !important;
    }

    /* 9. 차트 상단 요약 카드 컴팩트 스타일 */
    .price-kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 4px 8px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }
    .price-kpi-title {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        white-space: nowrap;
    }
    .price-kpi-val {
        font-size: 14px;
        font-weight: 900;
        color: #0F172A;
        line-height: 1.2;
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

# 일반 대시보드 시트용 헤더 정리 함수
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

# 금액 절삭 포맷터 ($1000 미만 반올림 절삭 -> $1,260K)
def format_k_dollar(val):
    try:
        if pd.isna(val) or val == '' or val == '-':
            return "-"
        clean_val = float(str(val).replace('$', '').replace(',', '').strip())
        k_val = round(clean_val / 1000.0)
        return f"${k_val:,.0f}K"
    except:
        return "-"

# 달러 포맷터
def format_currency_val(val, default_str="$4.40"):
    try:
        if pd.isna(val) or val == '' or val == '-':
            return default_str
        clean_val = float(str(val).replace('$', '').replace(',', '').strip())
        return f"${clean_val:.2f}"
    except:
        return str(val) if pd.notna(val) else default_str

# 백분율 포맷터
def format_percent(val):
    try:
        if pd.isna(val) or val == '' or val == '-':
            return "-2%"
        
        val_str = str(val).strip()
        if '%' in val_str:
            num = float(val_str.replace('%', '').strip())
            return f"{round(num):+.0f}%" if round(num) != 0 else "0%"
        
        num = float(val_str)
        if abs(num) < 1.0:
            pct = round(num * 100)
            return f"{pct:+.0f}%" if pct != 0 else "0%"
        else:
            return f"{round(num):+.0f}%"
    except:
        return "-2%"

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

        purchase_sheet = None
        for sheet in sheet_names:
            if "원부자재" in sheet or "구매액" in sheet:
                purchase_sheet = sheet
                break

        df_hr = pd.read_excel(file_bytes, sheet_name=hr_sheet)
        df_stock = pd.read_excel(file_bytes, sheet_name=stock_sheet)
        df_schedule = pd.read_excel(file_bytes, sheet_name=schedule_sheet)
        
        df_price_raw = pd.read_excel(file_bytes, sheet_name=price_sheet, header=None) if price_sheet else None
        df_purchase_raw = pd.read_excel(file_bytes, sheet_name=purchase_sheet, header=None) if purchase_sheet else None

        df_hr = fix_excel_header(df_hr)
        df_stock = fix_excel_header(df_stock)
        df_schedule = fix_excel_header(df_schedule)

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

        # --- [1행 우측] 주요 아이템 현황 ---
        with col_top_right:
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
        # 2행: [원부자재 구매액]
        # ====================================================================
        col_mid_left, col_mid_right = st.columns([1, 2])

        with col_mid_left:
            st.markdown('<div class="section-title" style="margin-top:10px;">💰 원부자재 구매액</div>', unsafe_allow_html=True)
            
            p_data = {
                '25년 전체': {'tot': '$17,679K', 'sub': '원 $15,521K / 부 $2,158K'},
                '25년 월평균': {'tot': '$1,473K', 'sub': '원 $1,293K / 부 $180K'},
                '26년 누적': {'tot': '$10,059K', 'sub': '원 $8,817K / 부 $1,242K'},
                '26년 월평균': {'tot': '$1,437K', 'sub': '원 $1,260K / 부 $177K'}
            }
            
            if df_purchase_raw is not None and not df_purchase_raw.empty:
                try:
                    def parse_num(v):
                        if pd.isna(v): return 0.0
                        s = str(v).replace('$', '').replace(',', '').strip()
                        try: return float(s)
                        except: return 0.0

                    valid_rows = []
                    for r_i in range(len(df_purchase_raw)):
                        row_vals = df_purchase_raw.iloc[r_i].values
                        nums = [parse_num(x) for x in row_vals if parse_num(x) > 0]
                        if len(nums) >= 2:
                            cat_text = str(row_vals[0]) if len(row_vals) > 0 else ""
                            valid_rows.append((cat_text, nums[0], nums[1]))

                    for cat_text, val_raw, val_sub in valid_rows:
                        c_clean = cat_text.replace(" ", "")
                        
                        target_key = None
                        if '25년전체' in c_clean or '2025년전체' in c_clean: target_key = '25년 전체'
                        elif '25년월평균' in c_clean or '2025년월평균' in c_clean: target_key = '25년 월평균'
                        elif '26년누적' in c_clean or '2026년누적' in c_clean: target_key = '26년 누적'
                        elif '26년월평균' in c_clean or '2026년월평균' in c_clean: target_key = '26년 월평균'

                        if target_key:
                            p_data[target_key] = {
                                'tot': format_k_dollar(val_raw + val_sub),
                                'sub': f"원 {format_k_dollar(val_raw)} / 부 {format_k_dollar(val_sub)}"
                            }

                    order_keys = ['25년 전체', '25년 월평균', '26년 누적', '26년 월평균']
                    for idx, (cat_text, val_raw, val_sub) in enumerate(valid_rows[:4]):
                        if idx < len(order_keys):
                            k = order_keys[idx]
                            if p_data[k]['tot'] == '-':
                                p_data[k] = {
                                    'tot': format_k_dollar(val_raw + val_sub),
                                    'sub': f"원 {format_k_dollar(val_raw)} / 부 {format_k_dollar(val_sub)}"
                                }
                except:
                    pass

            g_r1_c1, g_r1_c2 = st.columns([1, 1])
            with g_r1_c1:
                v1 = p_data.get('25년 전체', {'tot': '$17,679K', 'sub': '원 $15,521K / 부 $2,158K'})
                st.markdown(f"""
                <div class="grid-purchase-card">
                    <div class="grid-purchase-title">25년 전체</div>
                    <div class="grid-purchase-val">{v1['tot']}</div>
                    <div class="grid-purchase-sub">{v1['sub']}</div>
                </div>
                """, unsafe_allow_html=True)
            with g_r1_c2:
                v2 = p_data.get('25년 월평균', {'tot': '$1,473K', 'sub': '원 $1,293K / 부 $180K'})
                st.markdown(f"""
                <div class="grid-purchase-card">
                    <div class="grid-purchase-title">25년 월평균</div>
                    <div class="grid-purchase-val">{v2['tot']}</div>
                    <div class="grid-purchase-sub">{v2['sub']}</div>
                </div>
                """, unsafe_allow_html=True)

            g_r2_c1, g_r2_c2 = st.columns([1, 1])
            with g_r2_c1:
                v3 = p_data.get('26년 누적', {'tot': '$10,059K', 'sub': '원 $8,817K / 부 $1,242K'})
                st.markdown(f"""
                <div class="grid-purchase-card-highlight">
                    <div class="grid-purchase-title-hl">26년 누적</div>
                    <div class="grid-purchase-val-hl">{v3['tot']}</div>
                    <div class="grid-purchase-sub-hl">{v3['sub']}</div>
                </div>
                """, unsafe_allow_html=True)
            with g_r2_c2:
                v4 = p_data.get('26년 월평균', {'tot': '$1,437K', 'sub': '원 $1,260K / 부 $177K'})
                st.markdown(f"""
                <div class="grid-purchase-card-highlight">
                    <div class="grid-purchase-title-hl">26년 월평균</div>
                    <div class="grid-purchase-val-hl">{v4['tot']}</div>
                    <div class="grid-purchase-sub-hl">{v4['sub']}</div>
                </div>
                """, unsafe_allow_html=True)

        # --- [2행 우측] 소전각 가격 변동 트렌드 ---
        with col_mid_right:
            st.markdown('<div class="section-title" style="margin-top:10px;">🐮 소전각 가격 변동 트렌드</div>', unsafe_allow_html=True)
            
            if df_price_raw is not None and not df_price_raw.empty:
                try:
                    def parse_num_float(v):
                        try:
                            if pd.isna(v): return None
                            s = str(v).replace('$', '').replace('%', '').replace(',', '').strip()
                            return float(s)
                        except:
                            return None

                    # ★ [요청 적용] H3(H열3행), H4, H5, H6 셀 직접 지정 파싱 (인덱스: Row 2, 3, 4, 5 / Col 7)
                    avg_market_str = "$4.40"
                    avg_buy_str = "$4.33"
                    diff_str = "-2%"
                    cum_qty_str = "41FTL"

                    try:
                        # 엑셀의 H열은 7번째 인덱스 (0,1,2,3,4,5,6,7 -> H)
                        col_h_idx = 7 if len(df_price_raw.columns) > 7 else len(df_price_raw.columns) - 1

                        # H3 (Row index 2)
                        if len(df_price_raw) > 2:
                            val_h3 = df_price_raw.iloc[2, col_h_idx]
                            avg_market_str = format_currency_val(val_h3, "$4.40")

                        # H4 (Row index 3)
                        if len(df_price_raw) > 3:
                            val_h4 = df_price_raw.iloc[3, col_h_idx]
                            avg_buy_str = format_currency_val(val_h4, "$4.33")

                        # H5 (Row index 4)
                        if len(df_price_raw) > 4:
                            val_h5 = df_price_raw.iloc[4, col_h_idx]
                            diff_str = format_percent(val_h5)

                        # H6 (Row index 5)
                        if len(df_price_raw) > 5:
                            val_h6 = df_price_raw.iloc[5, col_h_idx]
                            cum_qty_str = str(val_h6).strip() if pd.notna(val_h6) else "41FTL"
                    except:
                        pass

                    # 날짜 및 수치 열 위치 기반 차트용 파싱
                    h_row = -1
                    for r_i in range(min(5, len(df_price_raw))):
                        row_cells = [str(x) for x in df_price_raw.iloc[r_i].values if pd.notna(x)]
                        if any('날짜' in x or '일자' in x for x in row_cells):
                            h_row = r_i
                            break

                    if h_row != -1:
                        data_part = df_price_raw.iloc[h_row + 1:].copy().reset_index(drop=True)
                        header_cells = [str(x).strip() for x in df_price_raw.iloc[h_row].values]

                        date_idx = None
                        market_idx = None
                        buy_idx = None

                        for c_i, h_text in enumerate(header_cells):
                            ht = h_text.replace(" ", "")
                            if ('날짜' in ht or '일자' in ht) and date_idx is None:
                                date_idx = c_i
                            elif ('시장' in ht) and '-3' not in ht and '3%' not in ht and market_idx is None:
                                market_idx = c_i
                            elif ('구매' in ht or '매입' in ht) and buy_idx is None:
                                buy_idx = c_i

                        if date_idx is not None and market_idx is not None:
                            dates_series = pd.to_datetime(data_part.iloc[:, date_idx], errors='coerce')
                            valid_m = dates_series.notna()

                            dates = dates_series[valid_m]
                            vals_market = data_part.iloc[:, market_idx][valid_m].apply(parse_num_float)
                            vals_buy = data_part.iloc[:, buy_idx][valid_m].apply(parse_num_float) if buy_idx is not None else None

                            # ★ 상단 H3, H4, H5, H6 미니 카드 4개 출력
                            kpi_c1, kpi_c2, kpi_c3, kpi_c4, _ = st.columns([1, 1, 1, 1, 2])
                            with kpi_c1:
                                st.markdown(f"""
                                <div class="price-kpi-card">
                                    <div class="price-kpi-title">시장가 누계평균</div>
                                    <div class="price-kpi-val" style="color:#0D6DFD;">{avg_market_str}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            with kpi_c2:
                                st.markdown(f"""
                                <div class="price-kpi-card">
                                    <div class="price-kpi-title">구매가 누계평균</div>
                                    <div class="price-kpi-val" style="color:#EF4444;">{avg_buy_str}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            with kpi_c3:
                                diff_color = "#16A34A" if "-" in diff_str else "#DC2626"
                                st.markdown(f"""
                                <div class="price-kpi-card">
                                    <div class="price-kpi-title">평균 단가 차이</div>
                                    <div class="price-kpi-val" style="color:{diff_color};">{diff_str}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            with kpi_c4:
                                st.markdown(f"""
                                <div class="price-kpi-card">
                                    <div class="price-kpi-title">누계 구매량</div>
                                    <div class="price-kpi-val" style="color:#8B5CF6;">{cum_qty_str}</div>
                                </div>
                                """, unsafe_allow_html=True)

                            fig = go.Figure()

                            # 1. 시장가격 (파란색 실선)
                            fig.add_trace(go.Scatter(
                                x=dates, y=vals_market,
                                mode='lines', name='시장가격',
                                line=dict(color='#0d6dfd', width=2.5, shape='spline')
                            ))

                            # 2. 구매가격 (빨간색 점)
                            if vals_buy is not None and vals_buy.notna().sum() > 0:
                                fig.add_trace(go.Scatter(
                                    x=dates, y=vals_buy,
                                    mode='markers', name='구매가격',
                                    marker=dict(color='#EF4444', size=7, symbol='circle')
                                ))

                            fig.update_layout(
                                xaxis=dict(gridcolor='#EDF2F7', tickfont=dict(size=11, color='#718096')),
                                yaxis=dict(gridcolor='#EDF2F7', tickfont=dict(size=11, color='#718096'), tickprefix="$", tickformat=",.2f"),
                                paper_bgcolor='white', plot_bgcolor='white', hovermode='x unified',
                                legend=dict(font=dict(size=11), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                margin=dict(l=15, r=15, t=20, b=15),
                                height=170
                            )
                            st.plotly_chart(fig, use_container_width=True)
                except Exception as ex:
                    st.warning(f"차트 데이터 처리 중 알림: {ex}")

        # ====================================================================
        # 3행: [출고 타임라인 달력]
        # ====================================================================
        st.markdown('<div class="section-title" style="margin-top:10px;">📅 출고 타임라인</div>', unsafe_allow_html=True)
        
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

            c_yr, c_m, _ = st.columns([1, 1, 10])
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
                .cal-td { vertical-align: top; height: 75px; padding: 4px 6px; border-bottom: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; position: relative; }
                .cal-day-num { font-weight: 400 !important; font-size: 18px; margin-bottom: 4px; color: #1A202C; line-height: 1.0; }
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
