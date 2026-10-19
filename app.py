import re
from io import BytesIO

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DataDoctor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

TYPE_OPTIONS = [
    "Auto detect",
    "Text",
    "Number",
    "Date",
    "Email",
    "Phone",
    "URL",
    "Category",
]

def inject_css(dark: bool) -> None:
    if dark:
        bg_primary = "#0f172a"
        bg_secondary = "#1e293b"
        bg_card = "#1e293b"
        bg_sidebar = "#0f172a"
        bg_input = "#334155"
        text_primary = "#e2e8f0"
        text_secondary = "#94a3b8"
        text_muted = "#64748b"
        accent = "#2dd4bf"
        accent_hover = "#14b8a6"
        accent_bg = "rgba(45, 212, 191, 0.10)"
        border_color = "#334155"
        shadow = "0 1px 3px rgba(0,0,0,0.4)"
        shadow_hover = "0 4px 12px rgba(0,0,0,0.5)"
        metric_bg = "#1e293b"
        success_bg = "rgba(34,197,94,0.12)"
        success_border = "#22c55e"
        warning_bg = "rgba(250,204,21,0.12)"
        warning_border = "#facc15"
        error_bg = "rgba(239,68,68,0.12)"
        error_border = "#ef4444"
        info_bg = "rgba(56,189,248,0.12)"
        info_border = "#38bdf8"
        df_header_bg = "#334155"
        df_row_hover = "rgba(45, 212, 191, 0.06)"
        scrollbar_thumb = "#475569"
        scrollbar_track = "#1e293b"
    else:
        bg_primary = "#e8ecf1"
        bg_secondary = "#dfe4eb"
        bg_card = "#f0f3f7"
        bg_sidebar = "#d5dbe5"
        bg_input = "#dce1e9"
        text_primary = "#111318"
        text_secondary = "#2d3242"
        text_muted = "#4a5168"
        accent = "#0b7a6f"
        accent_hover = "#096259"
        accent_bg = "rgba(11, 122, 111, 0.10)"
        border_color = "#b0b9c6"
        shadow = "0 1px 4px rgba(0,0,0,0.10), 0 0 1px rgba(0,0,0,0.06)"
        shadow_hover = "0 6px 16px rgba(0,0,0,0.14)"
        metric_bg = "#dfe4eb"
        success_bg = "rgba(22,163,74,0.12)"
        success_border = "#15803d"
        warning_bg = "rgba(202,138,4,0.12)"
        warning_border = "#a16207"
        error_bg = "rgba(220,38,38,0.12)"
        error_border = "#b91c1c"
        info_bg = "rgba(2,132,199,0.12)"
        info_border = "#0369a1"
        df_header_bg = "#cdd4de"
        df_row_hover = "rgba(11, 122, 111, 0.08)"
        scrollbar_thumb = "#8893a4"
        scrollbar_track = "#d5dbe5"

    light_overrides = ""
    if not dark:
        light_overrides = f"""
    
    .stApp, .stApp * {{
        color: {text_primary} !important;
    }}
    .stApp p, .stApp span, .stApp label, .stApp div, .stApp li, .stApp td, .stApp th,
    .stApp summary, .stApp a, .stApp strong, .stApp em, .stApp b, .stApp i,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
        color: {text_primary} !important;
    }}

    .stCaption, .stCaption *, [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {{
        color: {text_muted} !important;
    }}

    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {{
        color: {text_secondary} !important;
    }}

    .stDownloadButton > button, .stDownloadButton > button *,
    .stButton > button, .stButton > button * {{
        color: #ffffff !important;
    }}

    .stTabs [data-baseweb="tab"], .stTabs [data-baseweb="tab"] * {{
        color: {text_secondary} !important;
    }}
    .stTabs [aria-selected="true"], .stTabs [aria-selected="true"] * {{
        color: {accent} !important;
    }}

    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] .stCaption *,
    section[data-testid="stSidebar"] small {{
        color: {text_muted} !important;
    }}

    .stSelectbox div[data-baseweb="select"] *,
    [data-baseweb="popover"] *,
    [data-baseweb="menu"] *,
    [role="listbox"] *,
    [role="option"] * {{
        color: {text_primary} !important;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #c9d1dd 0%, {bg_sidebar} 100%) !important;
    }}

    [data-testid="stMetric"] {{
        background: {metric_bg} !important;
        border-left: 3px solid {accent} !important;
    }}

    [data-testid="stExpander"]:hover {{
        border-color: {border_color} !important;
    }}

    .stSelectbox > div > div {{
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
    }}
    .stSelectbox > div > div:focus-within {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px rgba(11, 122, 111, 0.18) !important;
    }}
    .stTextInput > div > div > input {{
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px rgba(11, 122, 111, 0.18) !important;
    }}

    [data-testid="stFileUploader"] section {{
        background: rgba(11, 122, 111, 0.06) !important;
        border: 2px dashed #8e99a9 !important;
    }}
    [data-testid="stFileUploader"] section:hover {{
        border-color: #8e99a9 !important;
        background: rgba(11, 122, 111, 0.06) !important;
    }}
    [data-testid="stFileUploader"] section small,
    [data-testid="stFileUploader"] section span {{
        color: {text_secondary} !important;
    }}

    .stDownloadButton > button,
    .stButton > button {{
        background: linear-gradient(135deg, {accent} 0%, {accent_hover} 100%) !important;
        box-shadow: 0 2px 6px rgba(11, 122, 111, 0.28) !important;
    }}
    .stDownloadButton > button:hover,
    .stButton > button:hover {{
        background: linear-gradient(135deg, {accent} 0%, {accent_hover} 100%) !important;
        box-shadow: 0 2px 6px rgba(11, 122, 111, 0.28) !important;
        transform: none !important;
    }}

    [data-testid="stMetric"]:hover {{
        box-shadow: {shadow} !important;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {scrollbar_thumb} !important;
    }}

    [data-testid="stDataFrame"] {{
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
    }}

    div[data-testid="stAlert"] {{
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    }}
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span {{
        color: {text_primary} !important;
    }}

    .stSlider [data-baseweb="slider"] div {{
        background-color: {border_color} !important;
    }}
    .stSlider [role="slider"] {{
        background-color: {accent} !important;
        border-color: {accent} !important;
    }}
    .stSlider div[data-testid="stTickBarMin"],
    .stSlider div[data-testid="stTickBarMax"] {{
        color: {text_secondary} !important;
    }}

    .stCheckbox > label > div[data-testid="stCheckbox"] {{
        border-color: {border_color} !important;
    }}
    .stToggle [data-testid="stToggle"] > label > div {{
        border-color: {border_color} !important;
    }}

    [data-baseweb="tooltip"] *, [data-baseweb="popover"] * {{
        color: {text_primary} !important;
    }}
    """

    css = f"""
    <style>
    *, *::before, *::after {{
        transition: background-color 0.25s ease, color 0.15s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .stApp {{
        background-color: {bg_primary} !important;
        color: {text_primary} !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {bg_sidebar} !important;
        border-right: 1px solid {border_color} !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] span {{
        color: {text_primary} !important;
    }}
    section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] small {{
        color: {text_secondary} !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: {text_primary} !important;
    }}
    .stMarkdown p, .stMarkdown li, .stMarkdown span {{
        color: {text_primary} !important;
    }}
    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {text_muted} !important;
    }}

    [data-testid="stMetric"] {{
        background: {metric_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: {shadow} !important;
    }}
    [data-testid="stMetric"]:hover {{
        box-shadow: {shadow_hover} !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {text_secondary} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {text_primary} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stExpander"] {{
        background: {bg_card} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        box-shadow: {shadow} !important;
        margin-bottom: 8px !important;
    }}
    [data-testid="stExpander"] summary {{
        color: {text_primary} !important;
    }}
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: {border_color} !important;
        border-radius: 10px !important;
    }}

    .stSelectbox > div > div,
    .stSlider > div,
    .stTextInput > div > div > input {{
        background-color: {bg_input} !important;
        color: {text_primary} !important;
        border-color: {border_color} !important;
    }}
    .stSelectbox label, .stSlider label, .stTextInput label, .stCheckbox label {{
        color: {text_primary} !important;
    }}

    .stCheckbox span {{
        color: {text_primary} !important;
    }}

    [data-testid="stFileUploader"] {{
        background: {bg_card} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stFileUploader"] section {{
        border: 2px dashed {border_color} !important;
        border-radius: 12px !important;
        padding: 24px !important;
        background: {accent_bg} !important;
    }}
    [data-testid="stFileUploader"] section:hover {{
        border-color: {accent} !important;
        background: {accent_bg} !important;
    }}

    .stDownloadButton > button,
    .stButton > button {{
        background: {accent} !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        box-shadow: {shadow} !important;
        transition: all 0.2s ease !important;
    }}
    .stDownloadButton > button:hover,
    .stButton > button:hover {{
        background: {accent_hover} !important;
        box-shadow: {shadow_hover} !important;
        transform: translateY(-1px);
    }}
    .stDownloadButton > button:active,
    .stButton > button:active {{
        transform: translateY(0px);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background: transparent !important;
        border-bottom: 2px solid {border_color} !important;
        gap: 0px !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {text_secondary} !important;
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {accent} !important;
        border-bottom-color: {accent} !important;
        font-weight: 600 !important;
    }}

    [data-testid="stDataFrame"] {{
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }}

    [data-testid="stAlert"] div[role="alert"] {{
        border-radius: 10px !important;
    }}
    .stSuccess, div[data-testid="stAlert"]:has([data-testid="stMarkdownContainer"]) {{
        border-radius: 10px !important;
    }}

    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {scrollbar_track};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {scrollbar_thumb};
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {accent};
    }}

    hr {{
        border-color: {border_color} !important;
    }}

    .stToggle label span {{
        color: {text_primary} !important;
    }}

    {light_overrides}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def load_data(file) -> pd.DataFrame:
    file.seek(0)
    if file.name.lower().endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)

def row_label(idx) -> str:
    if isinstance(idx, (int, float)):
        return str(int(idx) + 2)
    return str(idx)

def trim_text(df: pd.DataFrame):
    result = df.copy()
    changes = []

    for column in result.select_dtypes(include=["object", "string"]).columns:
        original = result[column].copy()
        result[column] = result[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
        count = int((original.ne(result[column]) & original.notna()).sum())

        if count:
            changes.append({
                "Action": "Trim spaces",
                "Column": column,
                "Items changed": count,
                "Reason": "Removed surrounding spaces",
            })

    return result, changes

def collapse_spaces(df: pd.DataFrame):
    result = df.copy()
    changes = []

    for column in result.select_dtypes(include=["object", "string"]).columns:
        original = result[column].copy()
        result[column] = result[column].map(
            lambda v: re.sub(r" {2,}", " ", v) if isinstance(v, str) else v
        )
        count = int((original.ne(result[column]) & original.notna()).sum())

        if count:
            changes.append({
                "Action": "Collapse spaces",
                "Column": column,
                "Items changed": count,
                "Reason": "Replaced multiple consecutive spaces with a single space",
            })

    return result, changes

def detect_type(series: pd.Series, column_name: str) -> str:
    name = str(column_name).lower()

    if "email" in name or "e-mail" in name:
        return "Email"
    if any(word in name for word in ["phone", "mobile", "tel", "contact"]):
        return "Phone"
    if any(word in name for word in ["url", "website", "link", "href"]):
        return "URL"
    if any(word in name for word in ["date", "dob", "time"]):
        return "Date"

    non_missing = series.dropna()

    if non_missing.empty:
        return "Text"

    numeric = pd.to_numeric(non_missing, errors="coerce")
    if numeric.notna().mean() >= 0.8:
        return "Number"

    if len(non_missing) >= 3:
        parsed_dates = pd.to_datetime(
            non_missing.astype(str), errors="coerce", format="mixed"
        )
        if parsed_dates.notna().mean() >= 0.8:
            return "Date"

    unique_count = non_missing.astype(str).nunique()
    if unique_count <= min(20, max(2, int(len(non_missing) * 0.2))):
        return "Category"

    return "Text"

def is_valid_email(value) -> bool:
    if pd.isna(value):
        return True
    value = str(value).strip()
    return bool(
        re.fullmatch(
            r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
            r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",
            value,
        )
    )

def is_valid_phone(value) -> bool:
    if pd.isna(value):
        return True
    value = str(value).strip()
    if not re.fullmatch(r"[\d\s\-\(\)\+]+", value):
        return False
    digit_count = sum(c.isdigit() for c in value)
    return 7 <= digit_count <= 15

def is_valid_url(value) -> bool:
    if pd.isna(value):
        return True
    value = str(value).strip()
    return bool(
        re.fullmatch(
            r"https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+",
            value,
        )
    )

def fill_missing_values(df: pd.DataFrame, strategy: str) -> tuple:
    result = df.copy()
    fill_changes: list[dict] = []

    if strategy == "Leave unchanged":
        return result, fill_changes

    for column in result.columns:
        missing_count = int(result[column].isna().sum())
        if missing_count == 0:
            continue

        series = result[column]

        if strategy == "Fill numeric columns with median":
            if not pd.api.types.is_numeric_dtype(series):
                continue
            fill_value = series.median()

        elif strategy == "Fill numeric columns with mean":
            if not pd.api.types.is_numeric_dtype(series):
                continue
            fill_value = series.mean()

        else:
            modes = series.mode(dropna=True)
            if modes.empty:
                continue
            fill_value = modes.iloc[0]

        if pd.isna(fill_value):
            continue

        result[column] = series.fillna(fill_value)

        fill_changes.append({
            "Action": "Fill missing values",
            "Column": column,
            "Items changed": missing_count,
            "Reason": f"{strategy}; value used: {fill_value}",
        })

    return result, fill_changes

def compute_column_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = []
    for col in df.columns:
        s = df[col]
        entry = {
            "Column": col,
            "Dtype": str(s.dtype),
            "Non-Null Count": int(s.notna().sum()),
            "Null Count": int(s.isna().sum()),
            "Unique Values": int(s.nunique(dropna=True)),
        }
        if pd.api.types.is_numeric_dtype(s):
            entry["Min"] = s.min()
            entry["Max"] = s.max()
            entry["Mean"] = round(s.mean(), 4) if s.notna().any() else None
            entry["Median"] = s.median() if s.notna().any() else None
        else:
            entry["Min"] = ""
            entry["Max"] = ""
            entry["Mean"] = ""
            entry["Median"] = ""
        stats.append(entry)
    return pd.DataFrame(stats)

def flag_outliers_iqr(df: pd.DataFrame, column_types: dict, repair: bool):
    result = df.copy()
    issues: list[dict] = []
    changes: list[dict] = []

    for col in result.columns:
        if column_types.get(col) != "Number":
            continue
        numeric = pd.to_numeric(result[col], errors="coerce")
        clean = numeric.dropna()
        if len(clean) < 4:
            continue

        q1 = clean.quantile(0.25)
        q3 = clean.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_mask = numeric.notna() & ((numeric < lower) | (numeric > upper))

        for idx in result.index[outlier_mask]:
            issues.append({
                "Row": row_label(idx),
                "Column": col,
                "Value": str(result.at[idx, col]),
                "Issue": f"Outlier (outside [{lower:.2f}, {upper:.2f}])",
            })

        if repair and outlier_mask.any():
            result.loc[outlier_mask, col] = float("nan")
            changes.append({
                "Action": "Remove outliers (IQR)",
                "Column": col,
                "Items changed": int(outlier_mask.sum()),
                "Reason": f"Values outside [{lower:.2f}, {upper:.2f}] set to NaN",
            })

    return result, issues, changes

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="CleanedData")
    return buffer.getvalue()

with st.sidebar:
    st.markdown("## 🩺 DataDoctor")
    st.caption("Detect · Clean · Export")
    st.divider()

    st.session_state.dark_mode = st.toggle(
        "🌙 Dark mode",
        value=st.session_state.dark_mode,
        key="theme_toggle",
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx"],
    )

    st.divider()

    with st.expander("Cleaning Options", expanded=True):
        trim_spaces = st.checkbox("Trim extra spaces in text", value=True)
        collapse_multi_spaces = st.checkbox(
            "Collapse multiple spaces inside text", value=False
        )
        remove_duplicates = st.checkbox("Remove exact duplicate rows", value=True)
        repair_invalid = st.checkbox(
            "Repair invalid values (convert to missing)", value=True
        )
        normalize_categories = st.checkbox(
            "Normalize category capitalization", value=False
        )
        standardize_col_names = st.checkbox(
            "Standardize column names (lowercase, underscores)", value=False
        )
        flag_outliers = st.checkbox("Flag outliers using IQR method", value=False)

    with st.expander("Missing-Value Handling"):
        drop_col_threshold = st.slider(
            "Drop columns with more than X% missing",
            min_value=0,
            max_value=100,
            value=100,
            step=5,
            help="Set to 100% to keep all columns.",
        )
        missing_strategy = st.selectbox(
            "Fill strategy",
            [
                "Leave unchanged",
                "Fill numeric columns with median",
                "Fill numeric columns with mean",
                "Fill each column with its most frequent value",
            ],
            index=1,
        )

    with st.expander("Validation Rules"):
        validate_age = st.checkbox("Flag negative Age values", value=True)
        validate_marks = st.checkbox(
            "Flag Marks/Score/Percentage outside 0–100", value=True
        )

inject_css(st.session_state.dark_mode)

st.title("DataDoctor")
st.caption("Detect data issues, clean your dataset, and export reliable results.")

if uploaded_file is None:
    st.info("Upload a **CSV** or **Excel** file in the sidebar to get started.")
    st.stop()

try:
    original_df = load_data(uploaded_file)
except Exception as error:
    st.error(f"Could not read the file: {error}")
    st.stop()

if original_df.empty:
    st.warning("The uploaded file has no rows.")
    st.stop()

if original_df.columns.duplicated().any():
    st.error(
        "Your dataset has duplicate column names. "
        "Rename them before cleaning."
    )
    st.stop()

with st.spinner("Analyzing and cleaning your data…"):

    cleaned_df = original_df.copy()
    change_log: list[dict] = []
    issue_records: list[dict] = []

    if standardize_col_names:
        new_names = {
            c: str(c).strip().lower().replace(" ", "_") for c in cleaned_df.columns
        }
        renamed = {k: v for k, v in new_names.items() if k != v}
        if renamed:
            cleaned_df = cleaned_df.rename(columns=new_names)
            change_log.append({
                "Action": "Standardize column names",
                "Column": "All",
                "Items changed": len(renamed),
                "Reason": "Lowercased and replaced spaces with underscores",
            })

    if trim_spaces:
        cleaned_df, trim_changes = trim_text(cleaned_df)
        change_log.extend(trim_changes)

    if collapse_multi_spaces:
        cleaned_df, collapse_changes = collapse_spaces(cleaned_df)
        change_log.extend(collapse_changes)

    if remove_duplicates:
        before = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates().copy()
        removed = before - len(cleaned_df)
        if removed:
            change_log.append({
                "Action": "Remove duplicates",
                "Column": "Entire row",
                "Items changed": removed,
                "Reason": "Exact duplicate rows",
            })

    if drop_col_threshold < 100:
        cols_to_drop = []
        for col in cleaned_df.columns:
            pct_missing = cleaned_df[col].isna().mean() * 100
            if pct_missing > drop_col_threshold:
                cols_to_drop.append(col)
        if cols_to_drop:
            cleaned_df = cleaned_df.drop(columns=cols_to_drop)
            for col in cols_to_drop:
                change_log.append({
                    "Action": "Drop column",
                    "Column": col,
                    "Items changed": len(original_df),
                    "Reason": f"More than {drop_col_threshold}% missing values",
                })

    column_types: dict[str, str] = {}

    with st.sidebar:
        with st.expander("🔍 Column Types", expanded=False):
            st.caption(
                "Auto detection is a suggestion. Override when a column "
                "contains mixed or unusual data."
            )
            for column in cleaned_df.columns:
                detected = detect_type(cleaned_df[column], column)
                selected_type = st.selectbox(
                    f"{column}  _(suggested: {detected})_",
                    TYPE_OPTIONS,
                    index=0,
                    key=f"type_{column}",
                )
                column_types[column] = (
                    detected if selected_type == "Auto detect" else selected_type
                )

    age_columns = [
        c for c in cleaned_df.columns if str(c).strip().lower() == "age"
    ]
    marks_columns = [
        c
        for c in cleaned_df.columns
        if str(c).strip().lower() in ["marks", "score", "percentage"]
    ]

    for column in cleaned_df.columns:
        expected_type = column_types.get(column, "Text")
        series = cleaned_df[column]

        if expected_type == "Number":
            converted = pd.to_numeric(series, errors="coerce")
            invalid = series.notna() & converted.isna()

            for idx in cleaned_df.index[invalid]:
                issue_records.append({
                    "Row": row_label(idx),
                    "Column": column,
                    "Value": str(cleaned_df.at[idx, column]),
                    "Issue": "Expected a number",
                })

            if repair_invalid and invalid.any():
                cleaned_df[column] = converted
                change_log.append({
                    "Action": "Convert invalid values to missing",
                    "Column": column,
                    "Items changed": int(invalid.sum()),
                    "Reason": "Expected numeric data",
                })
            elif pd.api.types.is_numeric_dtype(series):
                cleaned_df[column] = converted

            numeric_values = pd.to_numeric(cleaned_df[column], errors="coerce")

            if validate_age and column in age_columns:
                invalid_age = numeric_values.notna() & (numeric_values < 0)
                for idx in cleaned_df.index[invalid_age]:
                    issue_records.append({
                        "Row": row_label(idx),
                        "Column": column,
                        "Value": str(cleaned_df.at[idx, column]),
                        "Issue": "Age cannot be negative",
                    })
                if repair_invalid and invalid_age.any():
                    cleaned_df[column] = numeric_values.astype(float)
                    cleaned_df.loc[invalid_age, column] = float("nan")
                    change_log.append({
                        "Action": "Repair invalid Age",
                        "Column": column,
                        "Items changed": int(invalid_age.sum()),
                        "Reason": "Age cannot be negative",
                    })

            if validate_marks and column in marks_columns:
                invalid_marks = numeric_values.notna() & (
                    (numeric_values < 0) | (numeric_values > 100)
                )
                for idx in cleaned_df.index[invalid_marks]:
                    issue_records.append({
                        "Row": row_label(idx),
                        "Column": column,
                        "Value": str(cleaned_df.at[idx, column]),
                        "Issue": "Value must be between 0 and 100",
                    })
                if repair_invalid and invalid_marks.any():
                    cleaned_df[column] = pd.to_numeric(
                        cleaned_df[column], errors="coerce"
                    ).astype(float)
                    cleaned_df.loc[invalid_marks, column] = float("nan")
                    change_log.append({
                        "Action": "Repair out-of-range values",
                        "Column": column,
                        "Items changed": int(invalid_marks.sum()),
                        "Reason": "Value must be between 0 and 100",
                    })

        elif expected_type == "Date":
            converted = pd.to_datetime(series, errors="coerce", format="mixed")
            invalid = series.notna() & converted.isna()

            for idx in cleaned_df.index[invalid]:
                issue_records.append({
                    "Row": row_label(idx),
                    "Column": column,
                    "Value": str(cleaned_df.at[idx, column]),
                    "Issue": "Invalid date or date format",
                })

            if repair_invalid and invalid.any():
                cleaned_df[column] = converted
                change_log.append({
                    "Action": "Repair invalid dates",
                    "Column": column,
                    "Items changed": int(invalid.sum()),
                    "Reason": "Invalid dates converted to missing values",
                })

        elif expected_type == "Email":
            str_series = series.astype(str).where(series.notna(), other=pd.NA)
            invalid = series.notna() & ~str_series.map(
                lambda v: is_valid_email(v) if pd.notna(v) else True
            )

            for idx in cleaned_df.index[invalid]:
                issue_records.append({
                    "Row": row_label(idx),
                    "Column": column,
                    "Value": str(cleaned_df.at[idx, column]),
                    "Issue": "Invalid email address",
                })

            if repair_invalid and invalid.any():
                cleaned_df.loc[invalid, column] = float("nan")
                change_log.append({
                    "Action": "Repair invalid emails",
                    "Column": column,
                    "Items changed": int(invalid.sum()),
                    "Reason": "Invalid email addresses converted to missing values",
                })

        elif expected_type == "Phone":
            str_series = series.astype(str).where(series.notna(), other=pd.NA)
            invalid = series.notna() & ~str_series.map(
                lambda v: is_valid_phone(v) if pd.notna(v) else True
            )

            for idx in cleaned_df.index[invalid]:
                issue_records.append({
                    "Row": row_label(idx),
                    "Column": column,
                    "Value": str(cleaned_df.at[idx, column]),
                    "Issue": "Invalid phone number",
                })

            if repair_invalid and invalid.any():
                cleaned_df.loc[invalid, column] = float("nan")
                change_log.append({
                    "Action": "Repair invalid phones",
                    "Column": column,
                    "Items changed": int(invalid.sum()),
                    "Reason": "Invalid phone numbers converted to missing values",
                })

        elif expected_type == "URL":
            str_series = series.astype(str).where(series.notna(), other=pd.NA)
            invalid = series.notna() & ~str_series.map(
                lambda v: is_valid_url(v) if pd.notna(v) else True
            )

            for idx in cleaned_df.index[invalid]:
                issue_records.append({
                    "Row": row_label(idx),
                    "Column": column,
                    "Value": str(cleaned_df.at[idx, column]),
                    "Issue": "Invalid URL",
                })

            if repair_invalid and invalid.any():
                cleaned_df.loc[invalid, column] = float("nan")
                change_log.append({
                    "Action": "Repair invalid URLs",
                    "Column": column,
                    "Items changed": int(invalid.sum()),
                    "Reason": "Invalid URLs converted to missing values",
                })

        elif expected_type == "Category":
            non_missing = series.dropna().astype(str)
            grouped: dict[str, list[str]] = {}

            for value in non_missing.unique():
                grouped.setdefault(value.strip().casefold(), []).append(value)

            for variants in grouped.values():
                if len(variants) > 1:
                    for value in variants:
                        issue_records.append({
                            "Row": "Multiple",
                            "Column": column,
                            "Value": value,
                            "Issue": "Inconsistent category spelling or capitalization",
                        })

            if normalize_categories:
                normalized = series.copy()
                replacements = 0

                for variants in grouped.values():
                    if len(variants) > 1:
                        counts = non_missing[
                            non_missing.isin(variants)
                        ].value_counts()
                        preferred = counts.index[0]

                        for variant in variants:
                            if variant != preferred:
                                mask = series.astype("string").eq(variant)
                                normalized.loc[mask] = preferred
                                replacements += int(mask.sum())

                cleaned_df[column] = normalized

                if replacements:
                    change_log.append({
                        "Action": "Normalize categories",
                        "Column": column,
                        "Items changed": replacements,
                        "Reason": "Matched capitalization and surrounding spaces to the most common variant",
                    })

    if flag_outliers:
        cleaned_df, outlier_issues, outlier_changes = flag_outliers_iqr(
            cleaned_df, column_types, repair_invalid
        )
        issue_records.extend(outlier_issues)
        change_log.extend(outlier_changes)

    cleaned_df, fill_changes = fill_missing_values(cleaned_df, missing_strategy)
    change_log.extend(fill_changes)

st.subheader("📊 Original Dataset")

c1, c2, c3 = st.columns(3)
c1.metric("Rows", len(original_df))
c2.metric("Columns", len(original_df.columns))
c3.metric("Missing Cells", int(original_df.isna().sum().sum()))

st.dataframe(original_df, use_container_width=True, height=400)

st.subheader("🔎 Data Quality Overview")

missing = original_df.isna().sum()
missing = missing[missing > 0]

if missing.empty:
    st.success("No missing values found in the original dataset.")
else:
    missing_report = pd.DataFrame({
        "Missing Cells": missing,
        "Missing (%)": (missing / len(original_df) * 100).round(2),
    })
    st.dataframe(missing_report, use_container_width=True)

dup_count = int(original_df.duplicated().sum())
st.write(f"**Duplicate rows:** {dup_count}")

st.subheader("📋 Column Statistics")

col_stats_df = compute_column_stats(cleaned_df)
st.dataframe(col_stats_df, use_container_width=True, hide_index=True)

st.subheader("⚠️ Validation Report")

if issue_records:
    issues_df = pd.DataFrame(issue_records)
    st.warning(f"Found **{len(issues_df)}** potential data quality issue(s).")
    st.dataframe(issues_df, use_container_width=True, hide_index=True)
else:
    st.success("No issues found by the selected validation rules.")

st.subheader("✅ Cleaning Summary")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Original Rows", len(original_df))
c2.metric("Cleaned Rows", len(cleaned_df))
c3.metric("Missing Cells Remaining", int(cleaned_df.isna().sum().sum()))
c4.metric("Issues Found", len(issue_records))

if change_log:
    st.subheader("📝 Change Log")
    st.dataframe(
        pd.DataFrame(change_log),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No changes were made.")

st.subheader("🔄 Before & After")

original_tab, cleaned_tab = st.tabs(["Original Data", "Cleaned Data"])

with original_tab:
    st.dataframe(original_df, use_container_width=True, height=500)

with cleaned_tab:
    st.dataframe(cleaned_df, use_container_width=True, height=500)

st.subheader("📥 Download Results")

dl_cols = st.columns(4)

with dl_cols[0]:
    st.download_button(
        "⬇ Cleaned CSV",
        data=cleaned_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="cleaned_data.csv",
        mime="text/csv",
    )

with dl_cols[1]:
    st.download_button(
        "⬇ Cleaned Excel",
        data=to_excel_bytes(cleaned_df),
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

with dl_cols[2]:
    st.download_button(
        "⬇ Validation Report",
        data=pd.DataFrame(
            issue_records,
            columns=["Row", "Column", "Value", "Issue"],
        ).to_csv(index=False).encode("utf-8-sig"),
        file_name="validation_report.csv",
        mime="text/csv",
    )

with dl_cols[3]:
    st.download_button(
        "⬇ Change Log",
        data=pd.DataFrame(
            change_log,
            columns=["Action", "Column", "Items changed", "Reason"],
        ).to_csv(index=False).encode("utf-8-sig"),
        file_name="cleaning_report.csv",
        mime="text/csv",
    )

st.caption(
    "Automatic type detection is a best-effort suggestion. "
    "Review validation issues and cleaned data before using or sharing the output."
)
