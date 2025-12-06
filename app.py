import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================
# 0. THEME (AgTech: dark blue + green accents)
# ============================================
AGTECH_COLORS = {
    "bg_dark": "#06131f",      # main background (very dark blue)
    "bg_card": "#071e2b",      # cards / containers
    "accent_green": "#9ADC3F", # lime green
    "accent_line": "#2e5e2a",  # darker green
    "text_main": "#F5F7FA",    # soft white
    "text_muted": "#A0AEC0",   # light gray
}

st.set_page_config(
    page_title="Coffee Shop Sales Dashboard",
    layout="wide",
    page_icon="☕",
)

# Global CSS styling
st.markdown(
    f"""
    <style>
        /* Main background */
        [data-testid="stAppViewContainer"] {{
            background: radial-gradient(circle at top left, #0f2b46 0, {AGTECH_COLORS['bg_dark']} 40%, #020712 100%);
            color: {AGTECH_COLORS['text_main']};
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: #020b16;
            color: {AGTECH_COLORS['text_main']};
        }}

        /* Main content padding */
        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }}

        /* Titles */
        h1, h2, h3, h4 {{
            color: {AGTECH_COLORS['text_main']};
        }}

        /* Secondary text */
        p, span, label {{
            color: {AGTECH_COLORS['text_muted']};
        }}

        /* KPI cards */
        .kpi-card {{
            background: {AGTECH_COLORS['bg_card']};
            padding: 1rem 1.25rem;
            border-radius: 1rem;
            border: 1px solid {AGTECH_COLORS['accent_line']};
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        }}
        .kpi-label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {AGTECH_COLORS['text_muted']};
        }}
        .kpi-value {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {AGTECH_COLORS['accent_green']};
        }}

        /* Thin separators */
        hr {{
            border: none;
            border-top: 1px solid rgba(255,255,255,0.08);
            margin: 1.5rem 0;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================
# 1. LOAD DATA + FEATURE ENGINEERING
# ============================================

@st.cache_data
def load_data() -> pd.DataFrame:
    # IMPORTANT: relative path (file in the same repo/folder as app.py)
    df = pd.read_excel("coffee_shop_sales.xlsx")

    # Ensure proper date/time formats
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["transaction_time"] = pd.to_datetime(df["transaction_time"], format="%H:%M:%S")

    # Core feature engineering
    df["total_sales"] = df["unit_price"] * df["transaction_qty"]
    df["hour"] = df["transaction_time"].dt.hour
    df["day"] = df["transaction_date"].dt.day
    df["day_of_week"] = df["transaction_date"].dt.day_name()
    df["week_of_month"] = df["transaction_date"].dt.day.apply(lambda x: (x - 1) // 7 + 1)
    df["month"] = df["transaction_date"].dt.to_period("M").astype(str)
    df["month_name"] = df["transaction_date"].dt.month_name()

    def get_day_part(h: int) -> str:
        if 6 <= h < 11:
            return "Morning"
        elif 11 <= h < 15:
            return "Lunch"
        elif 15 <= h < 18:
            return "Afternoon"
        elif 18 <= h < 22:
            return "Evening"
        else:
            return "Late Night"

    df["day_part"] = df["hour"].apply(get_day_part)

    return df


df = load_data()

# ============================================
# 2. SIDEBAR FILTERS
# ============================================

st.sidebar.header("Filters")

stores = ["All stores"] + sorted(df["store_location"].unique().tolist())
selected_store = st.sidebar.selectbox("Store", stores)

months = ["All months"] + sorted(df["month"].unique().tolist())
selected_month = st.sidebar.selectbox("Month (YYYY-MM)", months)

# Apply filters
filtered_df = df.copy()

if selected_store != "All stores":
    filtered_df = filtered_df[filtered_df["store_location"] == selected_store]

if selected_month != "All months":
    filtered_df = filtered_df[filtered_df["month"] == selected_month]

# ============================================
# 3. HEADER
# ============================================

st.title("☕ Coffee Shop Sales Dashboard")

st.write(
    "Interactive sales analytics dashboard built with **Python, Streamlit and Plotly**."
)

if selected_store != "All stores" or selected_month != "All months":
    text_parts = []
    if selected_store != "All stores":
        text_parts.append(f"Store: **{selected_store}**")
    if selected_month != "All months":
        text_parts.append(f"Month: **{selected_month}**")
    st.write("Active filters: " + " | ".join(text_parts))
else:
    st.write("Showing **all stores** and **all months**.")

st.markdown("---")

# ============================================
# 4. MAIN KPIs / BUSINESS METRICS
# ============================================

total_revenue = filtered_df["total_sales"].sum()
total_tickets = filtered_df["transaction_id"].nunique()
aov = filtered_df["total_sales"].mean()

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-label">TOTAL REVENUE</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi-value">${total_revenue:,.0f}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with kpi_col2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-label">TOTAL TICKETS</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi-value">{total_tickets:,}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with kpi_col3:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-label">AVERAGE ORDER VALUE (AOV)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi-value">${aov:,.2f}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# 5. CORE CHARTS
# ============================================

col_left, col_right = st.columns(2)

# Revenue by store
with col_left:
    st.subheader("Revenue by store")
    revenue_by_store = (
        filtered_df.groupby("store_location")["total_sales"]
        .sum()
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )
    fig_store = px.bar(
        revenue_by_store,
        x="store_location",
        y="total_sales",
        title="",
        labels={"store_location": "Store", "total_sales": "Revenue"},
        color_discrete_sequence=[AGTECH_COLORS["accent_green"]],
    )
    st.plotly_chart(fig_store, use_container_width=True)

# Revenue by month
with col_right:
    st.subheader("Revenue by month")
    sales_by_month = (
        filtered_df.groupby("month")["total_sales"]
        .sum()
        .reset_index()
        .sort_values("month")
    )
    fig_month = px.line(
        sales_by_month,
        x="month",
        y="total_sales",
        markers=True,
        labels={"month": "Month", "total_sales": "Revenue"},
        color_discrete_sequence=[AGTECH_COLORS["accent_green"]],
    )
    st.plotly_chart(fig_month, use_container_width=True)

# Revenue by day of week
st.subheader("Revenue by day of the week")
sales_by_dow = (
    filtered_df.groupby("day_of_week")["total_sales"]
    .sum()
    .reset_index()
)

order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
sales_by_dow["day_of_week"] = pd.Categorical(
    sales_by_dow["day_of_week"], categories=order, ordered=True
)
sales_by_dow = sales_by_dow.sort_values("day_of_week")

fig_dow = px.bar(
    sales_by_dow,
    x="day_of_week",
    y="total_sales",
    labels={"day_of_week": "Day of week", "total_sales": "Revenue"},
    color_discrete_sequence=[AGTECH_COLORS["accent_green"]],
)
st.plotly_chart(fig_dow, use_container_width=True)

# Revenue by hour
st.subheader("Revenue by hour of the day")
sales_by_hour = (
    filtered_df.groupby("hour")["total_sales"]
    .sum()
    .reset_index()
    .sort_values("hour")
)
fig_hour = px.bar(
    sales_by_hour,
    x="hour",
    y="total_sales",
    labels={"hour": "Hour", "total_sales": "Revenue"},
    color_discrete_sequence=[AGTECH_COLORS["accent_green"]],
)
st.plotly_chart(fig_hour, use_container_width=True)

# ============================================
# 6. SUPPORTING METRICS / ADDITIONAL VIEWS
# ============================================

st.markdown("---")
st.subheader("Supporting metrics")

sup_col1, sup_col2 = st.columns(2)

# Tickets by day part
with sup_col1:
    st.markdown("**Ticket distribution by day part**")
    tickets_by_part = (
        filtered_df.groupby("day_part")["transaction_id"]
        .count()
        .reset_index()
        .rename(columns={"transaction_id": "tickets"})
    )
    day_part_order = ["Morning", "Lunch", "Afternoon", "Evening", "Late Night"]
    tickets_by_part["day_part"] = pd.Categorical(
        tickets_by_part["day_part"], categories=day_part_order, ordered=True
    )
    tickets_by_part = tickets_by_part.sort_values("day_part")

    fig_part = px.bar(
        tickets_by_part,
        x="day_part",
        y="tickets",
        labels={"day_part": "Day part", "tickets": "Tickets"},
        color_discrete_sequence=[AGTECH_COLORS["accent_green"]],
    )
    st.plotly_chart(fig_part, use_container_width=True)

# Heatmap: revenue by day of week and hour
with sup_col2:
    st.markdown("**Heatmap – revenue by hour and day of week**")
    heatmap_data = (
        filtered_df.groupby(["day_of_week", "hour"])["total_sales"]
        .sum()
        .reset_index()
    )
    heatmap_data["day_of_week"] = pd.Categorical(
        heatmap_data["day_of_week"], categories=order, ordered=True
    )
    heatmap_data = heatmap_data.sort_values(["day_of_week", "hour"])

    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="hour",
        y="day_of_week",
        z="total_sales",
        labels={"hour": "Hour", "day_of_week": "Day of week", "total_sales": "Revenue"},
        color_continuous_scale="Greens",
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ============================================
# 7. DETAILED TABLE
# ============================================

st.markdown("---")
st.subheader("Detailed transactions")

st.dataframe(
    filtered_df[
        [
            "transaction_date",
            "store_location",
            "product_type",
            "transaction_qty",
            "unit_price",
            "total_sales",
            "day_of_week",
            "hour",
            "day_part",
        ]
    ].sort_values("transaction_date", ascending=False),
    use_container_width=True,
)

