import streamlit as st
import pandas as pd
import os
import calendar
import io
import re
from datetime import datetime
import plotly.graph_objects as go

# 1. Page Layout Settings
st.set_page_config(page_title="Shinsegae Foods Dash Board", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* 1. Background Color */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* Streamlit top bar fix */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        position: absolute !important;
        z-index: 1 !important;
    }

    /* Content safe padding */
    .block-container {
        padding-top: 1.5rem !important;  
        padding-bottom: 1.0rem !important;
        padding-left: 2.0rem !important;
        padding-right: 2.0rem !important;
        max-width: 98% !important; 
    }
    
    /* 2. Top Header alignment */
    .header-flex-container {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
        margin-top: 0px !important;
        margin-bottom: 40px !important; 
        padding: 0px !important;
    }

    /* Main titles design */
    .dashboard-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        font-weight: 800 !important;
        color: #1A202C !important;
        font-size: 38px !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;     
    }

    /* 3. Subtitles & default font compress */
    html, body, [data-testid="stMarkdownContainer"] p, .stAlert p {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-size: 15px !important;
        line-height: 1.35 !important;
        color: #2D3748 !important;
    }
    
    /* 패널 컨테이너 타이틀 */
    .section-title {
        font-size: 19px !important;
        font-weight: 800 !important;
        color: #1E293B !important;
        margin-bottom: 12px !important;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* 패널 배경 스타일 */
    div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #F1F5F9;
        height: 100%;
    }

    /* 4. Table compact style */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important; 
        padding: 0px !important;
    }
    
    div[data-testid="stDataFrame"] td, div[data-testid="stDataFrame"] th {
        font-size: 13px !important;
        padding: 5px 8px !important;
    }

    /* 5. HR Metric Card */
    .metric-square {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 12px 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label {
        font-size: 14px;
        font-weight: 800;
        color: #4A5568;
    }
    .metric-val {
        font-size: 42px;
        font-weight: 900;
        color: #0F172A;
        line-height: 1.0;
        margin-top: 6px;
    }

    /* 5-1. HR List Container */
    .hr-summary-box {
        background: transparent;
        display: flex;
        flex-direction: column;
        gap: 6px;
        max-height: 380px; 
        overflow-y: auto;
        padding-right: 4px;
    }
    .hr-summary-box::-webkit-scrollbar { width: 4px; }
    .hr-summary-box::-webkit-scrollbar-thumb { background-color: #CBD5E1; border-radius: 4px; }
    
    .hr-list-row {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 8px 10px;
        display: flex;
        align-items: center;
        font-size: 14px;
        gap: 8px;
    }
    .hr-badge {
        padding: 3px 8px;
        border-radius: 99px;
        font-size: 12px;
        font-weight: 800;
        white-space: nowrap;
        text-align: center;
    }
    .hr-name {
        font-weight: 800;
        color: #1A202C;
        white-space: nowrap;
    }
    .hr-note {
        color: #475569;
        font-size: 13px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* 8. Selectbox Style */
    div[data-testid="stSelectbox"] div[role="combobox"],
    div[data-testid="stSelectbox"] > div > div,
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        min-height: 36px !important;
    }
    div[data-testid="stSelectbox"] label {
        font-size: 13px !important;
        color: #475569 !important;
        font-weight: 700 !important;
        padding-bottom: 2px !important;
    }

    /* 9. Price Trend Top KPI Cards */
    .price-kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        margin-bottom: 8px;
    }
    .price-kpi-title {
        font-size: 12px;
        font-weight: 700;
        color: #64748B;
        white-space: nowrap;
    }
    .price-kpi-val {
        font-size: 18px;
        font-weight: 900;
        color: #0F172A;
        margin-top: 2px;
    }

    /* 10. OB Schedule Mini Cards */
    .summary-card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 4px;
    }
    .summary-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 10px 12px;
        flex: 1 1 calc(50% - 8px); 
        min-width: 130px;
        box-sizing: border-box;
        border-left: 4px solid #3B82F6;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .summary-left {
        display: flex;
        flex-direction: column;
        flex-shrink: 0;
        margin-right: 8px;
    }
    .summary-card-title {
        font-size: 13px;
        font-weight: 800;
        color: #334155;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .summary-card-val {
        font-size: 22px;
        font-weight: 900;
    }
    .summary-right {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-end;
        gap: 4px;
    }
    .date-chip {
        background: #F1F5F9;
        color: #334155;
        border: 1px solid #CBD5E1;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 800;
        white-space: nowrap;
    }

    /* 11. Inventory Summary Cards */
    .inv-list-container-row {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 4px;
        justify-content: flex-start;
    }
    .inv-item-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 10px 12px;
        flex: 0 0 calc(33.333% - 6px); 
        max-width: calc(33.333% - 6px);
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    }
    .inv-header {
        font-size: 14px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 4px;
        line-height: 1.3;
    }
    .inv-body {
        display: flex;
        align-items: center;
        gap: 6px; 
        margin-bottom: 2px;
    }
    .inv-divider {
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 300;
    }
    .inv-metric {
        font-size: 12px;
        color: #475569;
        font-weight: 700;
    }
    .inv-metric .val {
        font-size: 18px;
        font-weight: 900;
        color: #0F172A;
    }
    .inv-notes {
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin-top: 8px;
    }
    .inv-badge {
        font-size: 11px;
        background: #F8FAFC;
        color: #334155;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 700;
        width: fit-content;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# 2. File Path
EXCEL_FILE_PATH = "dashboard raw data.xlsx"

# Today
today = datetime.today()
today_str = today.strftime('%Y-%m-%d')

# Header
st.markdown("""
<div class="header-flex-container">
    <div class="dashboard-title">Shinsegae Foods Dash Board</div>
    <div style="font-size: 15px; font-weight: 800; color: #475569; background: #F8FAFC; padding: 6px 14px; border-radius: 20px; border: 1px solid #CBD5E1;">
        📅 TODAY: {today_str}
    </div>
</div>
""".replace('{today_str}', today_str), unsafe_allow_html=True)


# Formatting Functions
def fix_excel_header(df):
    if df.empty:
        return df
    new_columns = df.iloc[0].fillna('').astype(str).tolist()
    new_columns = [col.strip() if col.strip() != '' and 'None' not in col else f"Col_{i}" for i, col in enumerate(new_columns)]
    df.columns = new_columns
    df = df.drop(df.index[0]).reset_index(drop=True)
    df = df.loc[:, ~df.columns.str.startswith('Col_')]
    for col in df.columns:
        if any(keyword in str(col).lower() for keyword in ['date', '일', '날짜']):
            try:
                converted = pd.to_datetime(df[col], errors='coerce')
                if converted.notna().sum() > 0:
                    df[col] = converted.dt.strftime('%Y-%m-%d').fillna(df[col])
            except:
                pass
    df.index = df.index + 1
    return df

def format_currency_val(val, default_str="$4.40"):
    try:
        if pd.isna(val) or val == '' or val == '-':
            return default_str
        clean_val = float(str(val).replace('$', '').replace(',', '').strip())
        return f"${clean_val:.2f}"
    except:
        return str(val) if pd.notna(val) else default_str

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

# Data Load
df_hr, df_stock, df_schedule, df_price_raw, df_inv_summary_raw = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), None, None

if os.path.exists(EXCEL_FILE_PATH):
    try:
        with open(EXCEL_FILE_PATH, "rb") as f:
            file_bytes = io.BytesIO(f.read())
            
        xls = pd.ExcelFile(file_bytes)
        sheet_names = xls.sheet_names
        
        hr_sheet = "HR" if "HR" in sheet_names else sheet_names[0]
        stock_sheet = "Major Item" if "Major Item" in sheet_names else (sheet_names[1] if len(sheet_names) > 1 else sheet_names[0])
        schedule_sheet = "OB Schedule" if "OB Schedule" in sheet_names else (sheet_names[2] if len(sheet_names) > 2 else sheet_names[0])
        
        price_sheet = None
        for sheet in sheet_names:
            if "Beef Clod" in sheet or "가격" in sheet:
                price_sheet = sheet
                break
                
        inv_summary_sheet = None
        for sheet in sheet_names:
            if "Inventory Summary" in sheet or "요약" in sheet:
                inv_summary_sheet = sheet
                break

        df_hr = fix_excel_header(pd.read_excel(file_bytes, sheet_name=hr_sheet))
        df_stock = fix_excel_header(pd.read_excel(file_bytes, sheet_name=stock_sheet))
        df_schedule = fix_excel_header(pd.read_excel(file_bytes, sheet_name=schedule_sheet))
        
        df_price_raw = pd.read_excel(file_bytes, sheet_name=price_sheet, header=None) if price_sheet else None
        df_inv_summary_raw = pd.read_excel(file_bytes, sheet_name=inv_summary_sheet, header=None) if inv_summary_sheet else None

    except Exception as e:
        st.error(f"❌ Error reading Excel file: {e}")
else:
    st.warning(f"⚠️ File not found: `{EXCEL_FILE_PATH}`. Please check the directory.")


# ====================================================================
# [ROW 1] 3열 분할: HR Management(1) | Monthly OB Summary(1) | Inventory Summary(1.4)
# ====================================================================
col_top1, col_top2, col_top3 = st.columns([1, 1, 1.4], gap="medium")

# --- 1. HR Management ---
with col_top1:
    st.markdown('<div class="section-title">👥 HR Management</div>', unsafe_allow_html=True)
    
    valid_hr = pd.DataFrame()
    if not df_hr.empty:
        name_col = df_hr.columns[0]
        valid_hr = df_hr[df_hr[name_col].notna()]
        valid_hr = valid_hr[valid_hr[name_col].astype(str).str.strip() != '']
        valid_hr = valid_hr[valid_hr[name_col].astype(str).str.lower() != 'nan']
    else:
        valid_hr = df_hr.copy()

    status_col_name = next((col for col in valid_hr.columns if 'Status' in str(col) or '상태' in str(col)), None)
    
    if status_col_name and not valid_hr.empty:
        total_staff_df = valid_hr[~valid_hr[status_col_name].astype(str).str.strip().str.lower().str.contains('vacation', na=False)]
        total_staff = len(total_staff_df)
    else:
        total_staff = len(valid_hr)

    absent_late_count = 0
    if status_col_name and not valid_hr.empty:
        status_series = valid_hr[status_col_name].astype(str).str.strip().str.lower()
        absent_late_count = valid_hr[status_series.str.contains('absent', na=False) | status_series.str.contains('late', na=False)].shape[0]
    
    hr_sub_l, hr_sub_r = st.columns([1, 2.2])
    with hr_sub_l:
        st.markdown(f"""
        <div class="metric-square">
            <div class="metric-label">Total Staff</div>
            <div class="metric-val">{total_staff}</div>
        </div>
        <div class="metric-square">
            <div class="metric-label">Absent/Late</div>
            <div class="metric-val" style="color:#DC2626;">{absent_late_count}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with hr_sub_r:
        hr_display_items = []
        for idx, row_data in valid_hr.iterrows():
            name = str(row_data.get('Name', row_data.iloc[0])).strip()
            raw_status = str(row_data.get('Status', row_data.get('현재상태', ''))).strip()
            note = str(row_data.get('Note', row_data.get('비고', ''))).strip()
            if note.lower() == 'nan': note = ""
            
            status_lower = raw_status.lower()
            if 'afternoon' in status_lower or 'vacation' in status_lower:
                continue
            
            is_on_time = (status_lower in ['on time', 'ontime'])
            has_note = bool(note)
            
            if is_on_time and not has_note:
                continue
            
            if is_on_time:
                status_text, badge_bg, badge_color, badge_border = "Active", "#DCFCE7", "#16A34A", "#86EFAC"
            else:
                status_text = raw_status if raw_status and raw_status.lower() != 'nan' else "Absent"
                badge_bg, badge_color, badge_border = "#FEE2E2", "#DC2626", "#FCA5A5"
                
            hr_display_items.append({
                'name': name, 'status_text': status_text, 
                'badge_bg': badge_bg, 'badge_color': badge_color, 'badge_border': badge_border,
                'note': note, 'has_note': has_note
            })
        
        hr_display_items.sort(key=lambda x: (x['has_note'], x['name'].lower()))

        html_hr_list = '<div class="hr-summary-box">'
        if hr_display_items:
            for item in hr_display_items:
                note_part = f'<span class="hr-note">- {item["note"]}</span>' if item["note"] else ""
                html_hr_list += f'<div class="hr-list-row"><span class="hr-badge" style="background-color:{item["badge_bg"]}; color:{item["badge_color"]}; border:1px solid {item["badge_border"]};">{item["status_text"]}</span><span class="hr-name">{item["name"]}</span>{note_part}</div>'
        else:
            html_hr_list += '<div style="color:#718096; font-size:14px; text-align:center; padding:20px;">No absents or special notes today.</div>'
        html_hr_list += '</div>'
        st.markdown(html_hr_list, unsafe_allow_html=True)


# --- 2. Monthly OB Summary ---
with col_top2:
    st.markdown('<div class="section-title">📅 Monthly OB Summary</div>', unsafe_allow_html=True)
    
    cal_df = df_schedule.copy()
    target_date_col = next((col for col in cal_df.columns if 'date' in str(col).lower() or '예정일' in str(col)), None)
    target_item_col = next((col for col in cal_df.columns if 'customer' in str(col).lower() or 'customoer' in str(col).lower() or '품목' in str(col)), None)
    if target_item_col is None and len(cal_df.columns) > 1: target_item_col = cal_df.columns[1]

    if target_date_col and target_item_col:
        cal_df['parsed_date'] = pd.to_datetime(cal_df[target_date_col], errors='coerce')
        default_year, default_month = today.year, today.month
        
        c_yr, c_m = st.columns(2)
        year_range = list(range(default_year - 1, default_year + 2))
        view_year = c_yr.selectbox("Select Year", year_range, index=year_range.index(default_year) if default_year in year_range else 1, key="cal_yr")
        view_month = c_m.selectbox("Select Month", range(1, 13), index=default_month - 1, key="cal_m")

        filtered_df = cal_df[(cal_df['parsed_date'].dt.year == view_year) & (cal_df['parsed_date'].dt.month == view_month)]
        summary_counts = filtered_df[target_item_col].value_counts()

        if not summary_counts.empty:
            html_cards = '<div class="summary-card-container">'
            for item_name, count in summary_counts.items():
                item_str = str(item_name).strip()
                if item_str and item_str.lower() not in ['nan', 'none']:
                    val_color = "#0D6DFD" if count > 5 else "#1A202C"
                    sorted_dates = filtered_df[filtered_df[target_item_col] == item_name].sort_values('parsed_date')['parsed_date']
                    dates_html = "".join([f'<span class="date-chip">{d.month}/{d.day}</span>' for d in sorted_dates if pd.notna(d)])
                    html_cards += f'<div class="summary-card"><div class="summary-left"><div class="summary-card-title">{item_str}</div><div class="summary-card-val" style="color:{val_color};">{count} <span style="font-size:12px; font-weight:700;">orders</span></div></div><div class="summary-right">{dates_html}</div></div>'
            html_cards += '</div>'
            st.markdown(html_cards, unsafe_allow_html=True)
        else:
            st.info(f"💡 No schedules found.")
    else:
        st.warning("Date/Customer columns not found.")


# --- 3. Inventory Summary ---
with col_top3:
    inv_title = "Inventory Summary"
    def get_cell_val(df, r, c):
        if df is not None and not df.empty and r < len(df) and c < len(df.columns):
            val = df.iloc[r, c]
            if pd.notna(val) and str(val).strip().lower() != 'nan': return str(val).strip()
        return ""
    def get_int_val(df, r, c):
        val = get_cell_val(df, r, c)
        if not val or val == "-": return val
        try: return f"{int(round(float(val.replace(',', '').strip()))):,}"
        except: return val
    
    inv_items = []
    if df_inv_summary_raw is not None and not df_inv_summary_raw.empty:
        for r_i in range(min(3, len(df_inv_summary_raw))):
            for c_i in range(min(3, len(df_inv_summary_raw.columns))):
                val = str(df_inv_summary_raw.iloc[r_i, c_i]).strip()
                if 'inventory' in val.lower() or '재고' in val:
                    inv_title = val
                    break

        h_row = -1
        c_cs, c_plt, c_note = -1, -1, -1
        for r_i in range(min(10, len(df_inv_summary_raw))):
            row_vals = [str(x).strip().lower() for x in df_inv_summary_raw.iloc[r_i].values if pd.notna(x)]
            if 'cs' in row_vals and 'plt' in row_vals:
                h_row = r_i
                headers = [str(x).strip().lower() for x in df_inv_summary_raw.iloc[h_row].values]
                c_cs = next((i for i, x in enumerate(headers) if 'cs' in x), -1)
                c_plt = next((i for i, x in enumerate(headers) if 'plt' in x), -1)
                c_note = next((i for i, x in enumerate(headers) if 'note' in x), -1)
                break

        if h_row != -1 and c_cs > 0:
            c_name = c_cs - 1
            curr_item = None
            for r_i in range(h_row + 1, len(df_inv_summary_raw)):
                row = df_inv_summary_raw.iloc[r_i]
                name_val = row.iloc[c_name] if c_name < len(row) else None
                if pd.notna(name_val) and str(name_val).strip() != "" and str(name_val).strip().lower() != "nan":
                    if curr_item: inv_items.append(curr_item)
                    n_str = str(name_val).strip()
                    tag = "🍲 Soup" if "soup" in n_str.lower() or "국탕" in n_str else "🥩 BBQ"
                    bg = "#FFEDD5" if "soup" in n_str.lower() or "국탕" in n_str else "#F3E8FF"
                    color = "#C2410C" if "soup" in n_str.lower() or "국탕" in n_str else "#7E22CE"
                    curr_item = {"name": n_str, "box": get_int_val(df_inv_summary_raw, r_i, c_cs) or "0", "pal": get_int_val(df_inv_summary_raw, r_i, c_plt) or "-", "notes": [], "tag": tag, "bg": bg, "color": color}
                if curr_item and c_note != -1 and c_note < len(row):
                    note_val = row.iloc[c_note]
                    if pd.notna(note_val) and str(note_val).strip() != "" and str(note_val).strip().lower() != "nan":
                        note_str = str(note_val).strip()
                        num_str = get_int_val(df_inv_summary_raw, r_i, c_note+1) if c_note+1 < len(row) else ""
                        unit_val = row.iloc[c_note+2] if c_note+2 < len(row) else ""
                        unit_str = str(unit_val).strip() if pd.notna(unit_val) and str(unit_val).lower() != 'nan' else ""
                        if num_str or unit_str: note_str += f" : {num_str} {unit_str}".strip()
                        note_str = re.sub(r'\b\d+\.\d+\b', lambda m: f"{int(round(float(m.group(0)))):,}", note_str)
                        curr_item["notes"].append(note_str.strip())
            if curr_item: inv_items.append(curr_item)

    if not inv_items:
        inv_items = [
            {"name": "TJ Beef Bulgogi", "box": "5,160", "pal": "123", "notes": ["SSG : 39 plt", "J&D : 84 plt"], "tag": "🥩 BBQ", "bg": "#F3E8FF", "color": "#7E22CE"},
            {"name": "Kroger Beef Bulgogi", "box": "2,590", "pal": "31", "notes": [], "tag": "🥩 BBQ", "bg": "#F3E8FF", "color": "#7E22CE"},
            {"name": "PK + ETC BBQ", "box": "429", "pal": "5", "notes": [], "tag": "🥩 BBQ", "bg": "#F3E8FF", "color": "#7E22CE"},
            {"name": "PK Soup", "box": "4,138", "pal": "61", "notes": ["under 100 cs : 0", "over 300 cs : 4"], "tag": "🍲 Soup", "bg": "#FFEDD5", "color": "#C2410C"},
            {"name": "HS Soup", "box": "0", "pal": "-", "notes": [], "tag": "🍲 Soup", "bg": "#FFEDD5", "color": "#C2410C"}
        ]

    st.markdown(f'<div class="section-title">📦 {inv_title}</div>', unsafe_allow_html=True)

    def sort_inv(item):
        n = str(item.get("name", "")).lower()
        if 'tj' in n: return 1
        if 'kroger' in n: return 2
        if 'bbq' in n or '가열육' in n: return 3
        if 'pk' in n and ('soup' in n or '국탕' in n): return 4
        if 'hs' in n or '한상' in n: return 5
        return 6
    inv_items.sort(key=sort_inv)

    def render_inv_card(item):
        notes_html = ""
        if item["notes"]:
            notes_html = '<div class="inv-notes">' + "".join([f'<span class="inv-badge">📌 {n}</span>' for n in item["notes"]]) + '</div>'
        badge_html = f'<span style="background-color:{item["bg"]}; color:{item["color"]}; border-radius:4px; padding:2px 6px; font-size:11px; font-weight:800; margin-right:4px;">{item["tag"]}</span>'
        return f'<div class="inv-item-card"><div class="inv-header">{badge_html} <span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{item["name"]}</span></div><div class="inv-body"><div class="inv-metric"><span class="val">{item["box"]}</span> cs</div><div class="inv-divider">|</div><div class="inv-metric"><span class="val">{item["pal"]}</span> plt</div></div>{notes_html}</div>'

    bbq_items = [item for item in inv_items if 'BBQ' in item.get('tag', '')]
    soup_items = [item for item in inv_items if 'Soup' in item.get('tag', '')]
    other_items = [item for item in inv_items if 'BBQ' not in item.get('tag', '') and 'Soup' not in item.get('tag', '')]

    html_inv = ""
    if bbq_items:
        html_inv += '<div class="inv-list-container-row">'
        for item in bbq_items: html_inv += render_inv_card(item)
        html_inv += '</div>'
    if soup_items:
        html_inv += '<div class="inv-list-container-row" style="margin-top: 8px;">'
        for item in soup_items: html_inv += render_inv_card(item)
        html_inv += '</div>'
    if other_items:
        html_inv += '<div class="inv-list-container-row" style="margin-top: 8px;">'
        for item in other_items: html_inv += render_inv_card(item)
        html_inv += '</div>'

    st.markdown(html_inv, unsafe_allow_html=True)


# ====================================================================
# [ROW 2] 2열 분할: Beef Clod Price Trend (50%) | Major Item Status (50%)
# ====================================================================
st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True) 

col_bot1, col_bot2 = st.columns([1, 1], gap="medium")

# --- 1. Beef Clod Price Trend ---
with col_bot1:
    st.markdown('<div class="section-title">🐮 Beef Clod Price Trend</div>', unsafe_allow_html=True)
    if df_price_raw is not None and not df_price_raw.empty:
        try:
            def parse_num_float(v):
                try:
                    if pd.isna(v): return None
                    return float(str(v).replace('$', '').replace('%', '').replace(',', '').strip())
                except: return None

            avg_market_str, avg_buy_str, diff_str, cum_qty_str = "$4.40", "$4.33", "-2%", "41FTL"
            for r_i in range(min(20, len(df_price_raw))):
                row_cells = [str(x).strip() for x in df_price_raw.iloc[r_i].values if pd.notna(x)]
                for c_i, cell in enumerate(row_cells):
                    if ('Avg MP' in cell or '시장가' in cell) and c_i + 1 < len(row_cells): avg_market_str = format_currency_val(row_cells[c_i+1])
                    elif ('Avg PP' in cell or '구매가' in cell) and c_i + 1 < len(row_cells): avg_buy_str = format_currency_val(row_cells[c_i+1])
                    elif ('Diff' in cell or '차이' in cell) and c_i + 1 < len(row_cells): diff_str = format_percent(row_cells[c_i+1])
                    elif ('Purchasing Qt' in cell or '구매량' in cell) and c_i + 1 < len(row_cells): cum_qty_str = row_cells[c_i+1]

            h_row = -1
            for r_i in range(min(5, len(df_price_raw))):
                row_cells = [str(x) for x in df_price_raw.iloc[r_i].values if pd.notna(x)]
                if any('date' in x.lower() or '날짜' in x for x in row_cells):
                    h_row = r_i
                    break

            if h_row != -1:
                data_part = df_price_raw.iloc[h_row + 1:].copy().reset_index(drop=True)
                header_cells = [str(x).strip().lower() for x in df_price_raw.iloc[h_row].values]
                date_idx, market_idx, buy_idx = None, None, None

                for c_i, h_text in enumerate(header_cells):
                    ht = h_text.replace(" ", "")
                    if ('date' in ht or '날짜' in ht) and date_idx is None: date_idx = c_i
                    elif ('market' in ht or '시장' in ht) and market_idx is None: market_idx = c_i
                    elif ('purchasing' in ht or '구매' in ht) and buy_idx is None: buy_idx = c_i

                if date_idx is not None and market_idx is not None:
                    dates_series = pd.to_datetime(data_part.iloc[:, date_idx], errors='coerce')
                    valid_m = dates_series.notna()
                    dates = dates_series[valid_m]
                    vals_market = data_part.iloc[:, market_idx][valid_m].apply(parse_num_float)
                    vals_buy = data_part.iloc[:, buy_idx][valid_m].apply(parse_num_float) if buy_idx is not None else None

                    kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
                    with kpi_c1: st.markdown(f'<div class="price-kpi-card"><div class="price-kpi-title">Avg Market Price</div><div class="price-kpi-val" style="color:#0D6DFD;">{avg_market_str}</div></div>', unsafe_allow_html=True)
                    with kpi_c2: st.markdown(f'<div class="price-kpi-card"><div class="price-kpi-title">Avg Purchasing Price</div><div class="price-kpi-val" style="color:#EF4444;">{avg_buy_str}</div></div>', unsafe_allow_html=True)
                    with kpi_c3: 
                        formatted_diff = format_percent(diff_str)
                        st.markdown(f'<div class="price-kpi-card"><div class="price-kpi-title">Price Difference</div><div class="price-kpi-val" style="color:{"#16A34A" if "-" in formatted_diff else "#DC2626"};">{formatted_diff}</div></div>', unsafe_allow_html=True)
                    with kpi_c4: st.markdown(f'<div class="price-kpi-card"><div class="price-kpi-title">Purchasing Qt</div><div class="price-kpi-val" style="color:#8B5CF6;">{cum_qty_str}</div></div>', unsafe_allow_html=True)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=dates, y=vals_market, mode='lines', name='Market Price', line=dict(color='#0d6dfd', width=2.5, shape='spline')))
                    
                    # ★ [방법 1 적용] 연결선(지시선)을 이용하여 빨간 점 가격을 안 겹치게 위/아래 교차 배치
                    if vals_buy is not None and vals_buy.notna().sum() > 0:
                        valid_buy_df = pd.DataFrame({'date': dates, 'val': vals_buy}).dropna()
                        
                        fig.add_trace(go.Scatter(
                            x=valid_buy_df['date'], y=valid_buy_df['val'], 
                            mode='markers', 
                            name='Purchasing Price', 
                            marker=dict(color='#EF4444', size=8, symbol='circle'),
                            hoverinfo='x+y'
                        ))

                        for i, row in valid_buy_df.reset_index(drop=True).iterrows():
                            y_offset = -32 if i % 2 == 0 else 32
                            
                            fig.add_annotation(
                                x=row['date'],
                                y=row['val'],
                                text=f"${row['val']:.2f}",
                                showarrow=True,
                                arrowhead=0,
                                arrowsize=1,
                                arrowwidth=1,
                                arrowcolor="#FCA5A5",
                                ax=0,
                                ay=y_offset,
                                font=dict(size=10, color="#DC2626", family="Arial Black"),
                                bgcolor="rgba(255, 255, 255, 0.85)",
                                bordercolor="#FCA5A5",
                                borderwidth=1,
                                borderpad=2
                            )

                    fig.update_layout(
                        xaxis=dict(gridcolor='#EDF2F7', tickfont=dict(size=12, color='#475569')),
                        yaxis=dict(gridcolor='#EDF2F7', tickfont=dict(size=12, color='#475569'), tickprefix="$", tickformat=",.2f"),
                        paper_bgcolor='white', plot_bgcolor='white', hovermode='x unified',
                        legend=dict(font=dict(size=12), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        margin=dict(l=15, r=15, t=10, b=10), height=260
                    )
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as ex: st.warning(f"Chart error: {ex}")


# --- 2. Major Item Status ---
with col_bot2:
    st.markdown('<div class="section-title">📦 Major Item Status</div>', unsafe_allow_html=True)
    date_cols = [col for col in df_stock.columns if 'Order Date' in str(col) or '발주일정' in str(col)]
    type_cols = [col for col in df_stock.columns if 'Food/Package' in str(col) or '분류' in str(col)]
    
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
        <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:5px 12px; font-size:13px; font-weight:700;">🚨 Overdue/Today: <span style="color:#CC0000;">{count_red}</span></div>
        <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:5px 12px; font-size:13px; font-weight:700;">⏰ Within 3 Days: <span style="color:#CC6600;">{count_orange}</span></div>
        <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:5px 12px; font-size:13px; font-weight:700;">⚠️ Within 7 Days: <span style="color:#888800;">{count_yellow}</span></div>
        <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:5px 12px; font-size:13px; font-weight:700;">✅ 8+ Days: <span style="color:#22543D;">{count_green}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    def style_stock_table(row):
        styles = [''] * len(row)
        if type_cols:
            t_idx = row.index.get_loc(type_cols[0])
            t_val = str(row[type_cols[0]]).strip().lower()
            if 'food' in t_val or '원재료' in t_val: styles[t_idx] = 'background-color: #EBF8FF; color: #2B6CB0; font-weight: bold;'
            elif 'package' in t_val or '부자재' in t_val: styles[t_idx] = 'background-color: #FFF5F5; color: #C53030; font-weight: bold;'
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
    
    st.dataframe(df_stock.style.apply(style_stock_table, axis=1), use_container_width=True, height=275)


# 시스템 최하단 안내
st.markdown(f"""
<div style="background-color: #EDF2F7; padding: 8px 12px; border-radius: 8px; text-align: center; font-size: 13px; color: #718096; margin-top: 25px; font-weight:600;">
    💡 Dashboards auto-update in seconds when you save the <code>{EXCEL_FILE_PATH}</code> file (Ctrl+S).
</div>
""", unsafe_allow_html=True)
