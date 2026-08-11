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
        background-color: #F4F5F7 !important;
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
    }
    
    /* 2. Top Header alignment */
    .header-flex-container {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        padding: 0px !important;
    }

    /* Main titles design */
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

    /* 3. Subtitles & default font compress */
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

    /* 4. Table compact style */
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

    /* 5. HR Metric Card */
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

    /* 6. Purchase Amount Card (2025) */
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

    /* 7. Purchase Amount Card (2026 Highlight) */
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

    /* 8. Selectbox Style */
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

    /* 9. Price Trend Top KPI Cards */
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

    /* 10. OB Schedule Mini Cards */
    .summary-card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 8px;
        margin-bottom: 15px;
    }
    .summary-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 10px 14px;
        flex: 1 1 calc(50% - 10px); 
        min-width: 140px;
        box-sizing: border-box;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border-left: 4px solid #3B82F6;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .summary-left {
        display: flex;
        flex-direction: column;
        flex-shrink: 0;
        margin-right: 10px;
    }
    .summary-card-title {
        font-size: 13px;
        font-weight: 800;
        color: #64748B;
        margin-bottom: 4px;
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
        color: #475569;
        border: 1px solid #E2E8F0;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        white-space: nowrap;
    }

    /* 11. Inventory Summary Cards */
    .inv-list-container-row {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 5px;
    }
    .inv-item-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 12px;
        flex: 1 1 0; 
        min-width: 160px; 
        box-sizing: border-box;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        display: flex;
        flex-direction: column;
    }
    .inv-header {
        font-size: 13px;
        font-weight: 800;
        color: #1A202C;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 4px;
        line-height: 1.3;
    }
    
    .inv-body {
        display: flex;
        align-items: center;
        gap: 8px; 
        margin-bottom: 4px;
        margin-top: 0px; 
    }
    .inv-divider {
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 300;
        margin-top: 1px;
    }
    .inv-metric {
        font-size: 11px;
        color: #718096;
        font-weight: 600;
    }
    .inv-metric .val {
        font-size: 15px;
        font-weight: 900;
        color: #2D3748;
    }
    
    .inv-notes {
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin-top: 6px;
    }
    .inv-badge {
        font-size: 10px;
        background: #F8FAFC;
        color: #475569;
        padding: 3px 6px;
        border-radius: 4px;
        font-weight: 600;
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
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; font-weight: 600; color: #718096; margin-top: 2px; margin-bottom: 8px;">
    📅 TODAY: {today_str}
</div>
""", unsafe_allow_html=True)

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

def format_k_dollar(val):
    try:
        if pd.isna(val) or val == '' or val == '-':
            return "-"
        clean_val = float(str(val).replace('$', '').replace(',', '').strip())
        k_val = round(clean_val / 1000.0)
        return f"${k_val:,.0f}K"
    except:
        return "-"

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
if os.path.exists(EXCEL_FILE_PATH):
    try:
        with open(EXCEL_FILE_PATH, "rb") as f:
            file_bytes = io.BytesIO(f.read())
            
        xls = pd.ExcelFile(file_bytes)
        sheet_names = xls.sheet_names
        
        # Mapping English Sheet Names
        hr_sheet = "HR" if "HR" in sheet_names else sheet_names[0]
        stock_sheet = "Major Item" if "Major Item" in sheet_names else (sheet_names[1] if len(sheet_names) > 1 else sheet_names[0])
        schedule_sheet = "OB Schedule" if "OB Schedule" in sheet_names else (sheet_names[2] if len(sheet_names) > 2 else sheet_names[0])
        
        price_sheet = None
        for sheet in sheet_names:
            if "Beef Clod" in sheet or "가격" in sheet:
                price_sheet = sheet
                break

        purchase_sheet = None
        for sheet in sheet_names:
            if "Purchasing Amount" in sheet or "구매액" in sheet:
                purchase_sheet = sheet
                break
                
        inv_summary_sheet = None
        for sheet in sheet_names:
            if "Inventory Summary" in sheet or "요약" in sheet:
                inv_summary_sheet = sheet
                break

        df_hr = pd.read_excel(file_bytes, sheet_name=hr_sheet)
        df_stock = pd.read_excel(file_bytes, sheet_name=stock_sheet)
        df_schedule = pd.read_excel(file_bytes, sheet_name=schedule_sheet)
        
        df_price_raw = pd.read_excel(file_bytes, sheet_name=price_sheet, header=None) if price_sheet else None
        df_purchase_raw = pd.read_excel(file_bytes, sheet_name=purchase_sheet, header=None) if purchase_sheet else None
        df_inv_summary_raw = pd.read_excel(file_bytes, sheet_name=inv_summary_sheet, header=None) if inv_summary_sheet else None

        df_hr = fix_excel_header(df_hr)
        df_stock = fix_excel_header(df_stock)
        df_schedule = fix_excel_header(df_schedule)

        # ====================================================================
        # ROW 1: [HR Management] (1/3)  +  [Inventory Summary] (2/3)
        # ====================================================================
        col_top_left, col_top_right = st.columns([1, 2])

        # --- [Row 1 Left] HR Management ---
        with col_top_left:
            st.markdown('<div class="section-title">👥 HR Management</div>', unsafe_allow_html=True)
            
            status_col = [col for col in df_hr.columns if 'Status' in str(col) or '상태' in str(col)]
            total_staff = len(df_hr)
            on_leave = df_hr[df_hr[status_col[0]].astype(str).str.upper().str.contains('OFF', na=False)].shape[0] if status_col else 0
            
            hr_sub_l, hr_sub_r = st.columns([1, 2.3])
            
            with hr_sub_l:
                st.markdown(f"""
                <div class="metric-square">
                    <div class="metric-label">Total Staff</div>
                    <div class="metric-val">{total_staff}</div>
                </div>
                <div class="metric-square">
                    <div class="metric-label">On Leave</div>
                    <div class="metric-val">{on_leave}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with hr_sub_r:
                for idx, row_data in df_hr.iterrows():
                    name = str(row_data.get('Name', row_data.get('이름', 'Unknown'))).strip()
                    job = str(row_data.get('Department', row_data.get('담당업무', '-'))).strip()
                    raw_status = str(row_data.get('Status', row_data.get('현재상태', 'ON'))).strip()
                    note = str(row_data.get('Note', row_data.get('비고', ''))).strip()
                    initial = name[0].upper() if name else '?'
                    
                    is_off = "OFF" in raw_status.upper()
                    status_text = "OFF" if is_off else "Active"
                    
                    badge_bg = "#FEE2E2" if is_off else "#DCFCE7"
                    badge_color = "#DC2626" if is_off else "#16A34A"
                    badge_border = "#FCA5A5" if is_off else "#86EFAC"
                    
                    note_part = f"<div style='font-size: 11px; color: #475569; background:#F8FAFC; padding: 2px 6px; border-radius:4px; margin-top:2px;'>📝 {note}</div>" if (note and note.lower() not in ['none', 'nan', '', 'null']) else ""
                    
                    card_html = f"""<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:6px 10px; margin-bottom:5px; display:flex; align-items:center; gap:8px;"><div style="background:#EDF2F7; color:#4A5568; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:12px; flex-shrink:0;">{initial}</div><div style="flex-grow:1;"><div style="display:flex; align-items:center; gap:6px;"><span style="background-color:{badge_bg}; color:{badge_color}; border:1px solid {badge_border}; padding:1px 6px; border-radius:99px; font-size:10px; font-weight:800;">{status_text}</span><span style="font-size:13px; font-weight:700; color:#1A202C;">{name}</span></div><div style="font-size:11px; color:#718096;">{job}</div>{note_part}</div></div>"""
                    
                    st.markdown(card_html, unsafe_allow_html=True)

        # --- [Row 1 Right] Inventory Summary ---
        with col_top_right:
            inv_title = "Inventory Summary"
            
            def get_cell_val(df, r, c):
                if df is not None and not df.empty and r < len(df) and c < len(df.columns):
                    val = df.iloc[r, c]
                    if pd.notna(val) and str(val).strip().lower() != 'nan':
                        return str(val).strip()
                return ""

            def get_int_val(df, r, c):
                val = get_cell_val(df, r, c)
                if not val or val == "-": return val
                try:
                    num = float(val.replace(',', '').strip())
                    return f"{int(round(num)):,}"
                except:
                    return val
            
            # Extract dynamically
            inv_items = []
            if df_inv_summary_raw is not None and not df_inv_summary_raw.empty:
                # Top title from top left area
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
                        cs_val = row.iloc[c_cs] if c_cs < len(row) else None
                        plt_val = row.iloc[c_plt] if c_plt < len(row) else None
                        
                        if pd.notna(name_val) and str(name_val).strip() != "" and str(name_val).strip().lower() != "nan":
                            if curr_item: inv_items.append(curr_item)
                            
                            n_str = str(name_val).strip()
                            # Auto assign tags based on name
                            tag = "🍲 Soup" if "soup" in n_str.lower() or "국탕" in n_str else "🥩 BBQ"
                            bg = "#FFEDD5" if "soup" in n_str.lower() or "국탕" in n_str else "#F3E8FF"
                            color = "#C2410C" if "soup" in n_str.lower() or "국탕" in n_str else "#7E22CE"

                            curr_item = {
                                "name": n_str,
                                "box": get_int_val(df_inv_summary_raw, r_i, c_cs) or "0",
                                "pal": get_int_val(df_inv_summary_raw, r_i, c_plt) or "-",
                                "notes": [],
                                "tag": tag, "bg": bg, "color": color
                            }
                            
                        if curr_item and c_note != -1 and c_note < len(row):
                            note_val = row.iloc[c_note]
                            if pd.notna(note_val) and str(note_val).strip() != "" and str(note_val).strip().lower() != "nan":
                                note_str = str(note_val).strip()
                                
                                num_str = get_int_val(df_inv_summary_raw, r_i, c_note+1) if c_note+1 < len(row) else ""
                                unit_val = row.iloc[c_note+2] if c_note+2 < len(row) else ""
                                unit_str = str(unit_val).strip() if pd.notna(unit_val) and str(unit_val).lower() != 'nan' else ""
                                
                                if num_str or unit_str:
                                    note_str += f" : {num_str} {unit_str}".strip()
                                    
                                note_str = re.sub(r'\b\d+\.\d+\b', lambda m: f"{int(round(float(m.group(0)))):,}", note_str)
                                curr_item["notes"].append(note_str.strip())
                    if curr_item:
                        inv_items.append(curr_item)

            if not inv_items:
                inv_items = [
                    {"name": "PK Soup", "box": "4,138", "pal": "61", "notes": ["under 100 cs : 0", "over 300 cs : 4"], "tag": "🍲 Soup", "bg": "#FFEDD5", "color": "#C2410C"},
                    {"name": "HS Soup", "box": "0", "pal": "-", "notes": [], "tag": "🍲 Soup", "bg": "#FFEDD5", "color": "#C2410C"},
                    {"name": "PK + ETC BBQ", "box": "429", "pal": "5", "notes": [], "tag": "🥩 BBQ", "bg": "#F3E8FF", "color": "#7E22CE"},
                    {"name": "Kroger Beef Bulgogi", "box": "2,590", "pal": "31", "notes": [], "tag": "🥩 BBQ", "bg": "#F3E8FF", "color": "#7E22CE"},
                    {"name": "TJ Beef Bulgogi", "box": "5,160", "pal": "123", "notes": ["SSG : 39 plt", "J&D : 84 plt"], "tag": "🥩 BBQ", "bg": "#F3E8FF", "color": "#7E22CE"}
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
                badge_html = f'<span style="background-color:{item["bg"]}; color:{item["color"]}; border-radius:4px; padding:2px 6px; font-size:11px; font-weight:800; margin-right:6px; vertical-align:text-bottom; white-space:nowrap;">{item["tag"]}</span>'
                
                return f'<div class="inv-item-card"><div class="inv-header">{badge_html} <span>{item["name"]}</span></div><div class="inv-body"><div class="inv-metric"><span class="val">{item["box"]}</span> cs</div><div class="inv-divider">|</div><div class="inv-metric"><span class="val">{item["pal"]}</span> plt</div></div>{notes_html}</div>'

            html_inv = '<div class="inv-list-container-row">'
            for item in inv_items:
                html_inv += render_inv_card(item)
            html_inv += '</div>'
            st.markdown(html_inv, unsafe_allow_html=True)

        # ====================================================================
        # ROW 2: [Monthly OB Summary] (Left) + [Beef Clod Price Trend] (Right)
        # ====================================================================
        col_mid_left, col_mid_right = st.columns([1, 2]) 

        # --- [Row 2 Left] Monthly OB Summary ---
        with col_mid_left:
            st.markdown('<div class="section-title" style="margin-top:10px;">📅 Monthly OB Summary</div>', unsafe_allow_html=True)
            
            cal_df = df_schedule.copy()
            
            target_date_col = next((col for col in cal_df.columns if 'date' in str(col).lower() or '예정일' in str(col)), None)
            target_item_col = next((col for col in cal_df.columns if 'customer' in str(col).lower() or 'customoer' in str(col).lower() or '품목' in str(col)), None)
            
            if target_item_col is None and len(cal_df.columns) > 1:
                target_item_col = cal_df.columns[1]

            if target_date_col and target_item_col:
                cal_df['parsed_date'] = pd.to_datetime(cal_df[target_date_col], errors='coerce')

                default_year = today.year
                default_month = today.month

                c_yr, c_m = st.columns(2)
                year_range = list(range(default_year - 1, default_year + 2))
                default_year_idx = year_range.index(default_year) if default_year in year_range else 1
                
                view_year = c_yr.selectbox("Select Year", year_range, index=default_year_idx, key="cal_yr")
                view_month = c_m.selectbox("Select Month", range(1, 13), index=default_month - 1, key="cal_m")

                filtered_df = cal_df[
                    (cal_df['parsed_date'].dt.year == view_year) & 
                    (cal_df['parsed_date'].dt.month == view_month)
                ]

                summary_counts = filtered_df[target_item_col].value_counts()

                if not summary_counts.empty:
                    html_cards = '<div class="summary-card-container">'
                    for item_name, count in summary_counts.items():
                        item_str = str(item_name).strip()
                        if item_str and item_str.lower() not in ['nan', 'none']:
                            val_color = "#0D6DFD" if count > 5 else "#1A202C"
                            
                            sorted_dates = filtered_df[filtered_df[target_item_col] == item_name].sort_values('parsed_date')['parsed_date']
                            date_strs = [f"{d.month}/{d.day}" for d in sorted_dates if pd.notna(d)]
                            dates_html = "".join([f'<span class="date-chip">{d}</span>' for d in date_strs])
                            
                            html_cards += f'<div class="summary-card"><div class="summary-left"><div class="summary-card-title">{item_str}</div><div class="summary-card-val" style="color:{val_color};">{count} <span style="font-size:12px; font-weight:700;">orders</span></div></div><div class="summary-right">{dates_html}</div></div>'
                    html_cards += '</div>'
                    st.markdown(html_cards, unsafe_allow_html=True)
                else:
                    st.info(f"💡 No schedules found for {view_month}/{view_year}.")
            else:
                st.warning("Cannot find 'Date' or 'Customer' column.")

        # --- [Row 2 Right] Beef Clod Price Trend ---
        with col_mid_right:
            st.markdown('<div class="section-title" style="margin-top:10px;">🐮 Beef Clod Price Trend</div>', unsafe_allow_html=True)
            
            if df_price_raw is not None and not df_price_raw.empty:
                try:
                    def parse_num_float(v):
                        try:
                            if pd.isna(v): return None
                            s = str(v).replace('$', '').replace('%', '').replace(',', '').strip()
                            return float(s)
                        except:
                            return None

                    avg_market_str = "$4.40"
                    avg_buy_str = "$4.33"
                    diff_str = "-2%"
                    cum_qty_str = "41FTL"

                    # Dynamically search for KPIs
                    for r_i in range(min(20, len(df_price_raw))):
                        row_cells = [str(x).strip() for x in df_price_raw.iloc[r_i].values if pd.notna(x)]
                        for c_i, cell in enumerate(row_cells):
                            if ('Avg MP' in cell or '시장가' in cell) and c_i + 1 < len(row_cells):
                                avg_market_str = format_currency_val(row_cells[c_i+1])
                            elif ('Avg PP' in cell or '구매가' in cell) and c_i + 1 < len(row_cells):
                                avg_buy_str = format_currency_val(row_cells[c_i+1])
                            elif ('Diff' in cell or '차이' in cell) and c_i + 1 < len(row_cells):
                                diff_str = format_percent(row_cells[c_i+1])
                            elif ('Purchasing Qt' in cell or '구매량' in cell) and c_i + 1 < len(row_cells):
                                cum_qty_str = row_cells[c_i+1]

                    h_row = -1
                    for r_i in range(min(5, len(df_price_raw))):
                        row_cells = [str(x) for x in df_price_raw.iloc[r_i].values if pd.notna(x)]
                        if any('date' in x.lower() or '날짜' in x for x in row_cells):
                            h_row = r_i
                            break

                    if h_row != -1:
                        data_part = df_price_raw.iloc[h_row + 1:].copy().reset_index(drop=True)
                        header_cells = [str(x).strip().lower() for x in df_price_raw.iloc[h_row].values]

                        date_idx = None
                        market_idx = None
                        buy_idx = None

                        for c_i, h_text in enumerate(header_cells):
                            ht = h_text.replace(" ", "")
                            if ('date' in ht or '날짜' in ht) and date_idx is None:
                                date_idx = c_i
                            elif ('market' in ht or '시장' in ht) and market_idx is None:
                                market_idx = c_i
                            elif ('purchasing' in ht or '구매' in ht) and buy_idx is None:
                                buy_idx = c_i

                        if date_idx is not None and market_idx is not None:
                            dates_series = pd.to_datetime(data_part.iloc[:, date_idx], errors='coerce')
                            valid_m = dates_series.notna()

                            dates = dates_series[valid_m]
                            vals_market = data_part.iloc[:, market_idx][valid_m].apply(parse_num_float)
                            vals_buy = data_part.iloc[:, buy_idx][valid_m].apply(parse_num_float) if buy_idx is not None else None

                            kpi_c1, kpi_c2, kpi_c3, kpi_c4, _ = st.columns([1, 1, 1, 1, 1])
                            with kpi_c1:
                                st.markdown(f"""
                                <div class="price-kpi-card">
                                    <div class="price-kpi-title">Avg Market Price</div>
                                    <div class="price-kpi-val" style="color:#0D6DFD;">{avg_market_str}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            with kpi_c2:
                                st.markdown(f"""
                                <div class="price-kpi-card">
                                    <div class="price-kpi-title">Avg Purchasing Price</div>
                                    <div class="price-kpi-val" style="color:#EF4444;">{avg_buy_str}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            with kpi_c3:
                                formatted_diff = format_percent(diff_str)
                                diff_color = "#16A34A" if "-" in formatted_diff else "#DC2626"
                                st.markdown(f"""
                                <div class="price-kpi-card">
                                    <div class="price-kpi-title">Price Difference</div>
                                    <div class="price-kpi-val" style="color:{diff_color};">{formatted_diff}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            with kpi_c4:
                                st.markdown(f"""
                                <div class="price-kpi-card">
                                    <div class="price-kpi-title">Purchasing Qt</div>
                                    <div class="price-kpi-val" style="color:#8B5CF6;">{cum_qty_str}</div>
                                </div>
                                """, unsafe_allow_html=True)

                            fig = go.Figure()

                            fig.add_trace(go.Scatter(
                                x=dates, y=vals_market,
                                mode='lines', name='Market Price',
                                line=dict(color='#0d6dfd', width=2.5, shape='spline')
                            ))

                            if vals_buy is not None and vals_buy.notna().sum() > 0:
                                fig.add_trace(go.Scatter(
                                    x=dates, y=vals_buy,
                                    mode='markers', name='Purchasing Price',
                                    marker=dict(color='#EF4444', size=7, symbol='circle')
                                ))

                            # ★ [수정 적용] 차트 세로 높이를 170 -> 280으로 확대하여 왼쪽 영역과 균형 맞춤
                            fig.update_layout(
                                xaxis=dict(gridcolor='#EDF2F7', tickfont=dict(size=11, color='#718096')),
                                yaxis=dict(gridcolor='#EDF2F7', tickfont=dict(size=11, color='#718096'), tickprefix="$", tickformat=",.2f"),
                                paper_bgcolor='white', plot_bgcolor='white', hovermode='x unified',
                                legend=dict(font=dict(size=11), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                margin=dict(l=15, r=15, t=20, b=15),
                                height=280 
                            )
                            st.plotly_chart(fig, use_container_width=True)
                except Exception as ex:
                    st.warning(f"Chart error: {ex}")


        # ====================================================================
        # ROW 3: [Purchasing Amount] (Left) + [Major Item Status] (Right)
        # ====================================================================
        col_bot_left, col_bot_right = st.columns([1, 2])
        
        # --- [Row 3 Left] Purchasing Amount ---
        with col_bot_left:
            st.markdown('<div class="section-title" style="margin-top:10px;">💰 Purchasing Amount</div>', unsafe_allow_html=True)
            
            p_data = {
                '2025 Cumulative': {'tot': '$17,679K', 'sub': 'Food $15,521K / Pkg $2,158K'},
                '2025 Monthly Avg': {'tot': '$1,473K', 'sub': 'Food $1,293K / Pkg $180K'},
                '2026 Cumulative': {'tot': '$10,059K', 'sub': 'Food $8,817K / Pkg $1,242K'},
                '2026 Monthly Avg': {'tot': '$1,437K', 'sub': 'Food $1,260K / Pkg $177K'}
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
                            cat_text = str(row_vals[0]).strip() if len(row_vals) > 0 else ""
                            valid_rows.append((cat_text, nums[0], nums[1]))

                    for cat_text, val_raw, val_sub in valid_rows:
                        c_clean = cat_text.replace(" ", "")
                        target_key = None
                        
                        if '25년전체' in c_clean or '2025Cumulative' in c_clean or '2025전체' in c_clean: target_key = '2025 Cumulative'
                        elif '25년월평균' in c_clean or '2025MonthlyAvg' in c_clean: target_key = '2025 Monthly Avg'
                        elif '26년누적' in c_clean or '2026Cumulative' in c_clean: target_key = '2026 Cumulative'
                        elif '26년월평균' in c_clean or '2026MonthlyAvg' in c_clean: target_key = '2026 Monthly Avg'

                        if target_key:
                            p_data[target_key] = {
                                'tot': format_k_dollar(val_raw + val_sub),
                                'sub': f"Food {format_k_dollar(val_raw)} / Pkg {format_k_dollar(val_sub)}"
                            }
                except:
                    pass

            g_r1_c1, g_r1_c2 = st.columns([1, 1])
            with g_r1_c1:
                v1 = p_data.get('2025 Cumulative', {'tot': '$17,679K', 'sub': 'Food $15,521K / Pkg $2,158K'})
                st.markdown(f"""
                <div class="grid-purchase-card">
                    <div class="grid-purchase-title">2025 Cumulative</div>
                    <div class="grid-purchase-val">{v1['tot']}</div>
                    <div class="grid-purchase-sub">{v1['sub']}</div>
                </div>
                """, unsafe_allow_html=True)
            with g_r1_c2:
                v2 = p_data.get('2025 Monthly Avg', {'tot': '$1,473K', 'sub': 'Food $1,293K / Pkg $180K'})
                st.markdown(f"""
                <div class="grid-purchase-card">
                    <div class="grid-purchase-title">2025 Monthly Avg</div>
                    <div class="grid-purchase-val">{v2['tot']}</div>
                    <div class="grid-purchase-sub">{v2['sub']}</div>
                </div>
                """, unsafe_allow_html=True)

            g_r2_c1, g_r2_c2 = st.columns([1, 1])
            with g_r2_c1:
                v3 = p_data.get('2026 Cumulative', {'tot': '$10,059K', 'sub': 'Food $8,817K / Pkg $1,242K'})
                st.markdown(f"""
                <div class="grid-purchase-card-highlight">
                    <div class="grid-purchase-title-hl">2026 Cumulative</div>
                    <div class="grid-purchase-val-hl">{v3['tot']}</div>
                    <div class="grid-purchase-sub-hl">{v3['sub']}</div>
                </div>
                """, unsafe_allow_html=True)
            with g_r2_c2:
                v4 = p_data.get('2026 Monthly Avg', {'tot': '$1,437K', 'sub': 'Food $1,260K / Pkg $177K'})
                st.markdown(f"""
                <div class="grid-purchase-card-highlight">
                    <div class="grid-purchase-title-hl">2026 Monthly Avg</div>
                    <div class="grid-purchase-val-hl">{v4['tot']}</div>
                    <div class="grid-purchase-sub-hl">{v4['sub']}</div>
                </div>
                """, unsafe_allow_html=True)

        # --- [Row 3 Right] Major Item Status ---
        with col_bot_right:
            st.markdown('<div class="section-title" style="margin-top:10px;">📦 Major Item Status</div>', unsafe_allow_html=True)
            
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
                <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:4px 10px; font-size:12px; font-weight:700;">🚨 Overdue/Today: <span style="color:#CC0000;">{count_red}</span></div>
                <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:4px 10px; font-size:12px; font-weight:700;">⏰ Within 3 Days: <span style="color:#CC6600;">{count_orange}</span></div>
                <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:4px 10px; font-size:12px; font-weight:700;">⚠️ Within 7 Days: <span style="color:#888800;">{count_yellow}</span></div>
                <div style="background:#FFF; border:1px solid #E2E8F0; border-radius:6px; padding:4px 10px; font-size:12px; font-weight:700;">✅ 8+ Days: <span style="color:#22543D;">{count_green}</span></div>
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
            
            st.dataframe(df_stock.style.apply(style_stock_table, axis=1), use_container_width=True, height=210)


        # Bottom System Info
        st.markdown(f"""
        <div style="background-color: #EDF2F7; padding: 6px 12px; border-radius: 8px; text-align: center; font-size: 12px; color: #718096; margin-top: 25px;">
            💡 Dashboards auto-update in seconds when you save the <code>{EXCEL_FILE_PATH}</code> file (Ctrl+S).
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error reading Excel file: {e}")
else:
    st.error(f"❌ File not found: Please ensure `{EXCEL_FILE_PATH}` exists in the current directory.")
