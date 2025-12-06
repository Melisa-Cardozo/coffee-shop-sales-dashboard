import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Coffee Shop Sales Dashboard",
    layout="wide",
    page_icon="☕",
)

# --------------------------------------------------
# GLOBAL STYLES (AgTech / dark blue + green)
# --------------------------------------------------
AGTECH_COLORS = {
    "bg_dark": "#06131f",      # fondo principal (azul muy oscuro)
    "bg_card": "#071e2b",      # tarjetas / contenedores
    "accent_green": "#9ADc3f", # verde lima
    "accent_line": "#2e5e2a",  # verde más oscuro
    "text_main": "#F5F7FA",    # blanco suave
    "text_muted": "#A0AEC0",   # gris claro
}

st.markdown(
    f"""
    <style>
        /* Fondo general */
        [data-testid="stAppViewContainer"] {{
            background: radial-gradient(circle at top left, #0f2b46 0, {AGTECH_COLORS['bg_dark']} 40%, #020712 100%);
            color: {AGTECH_COLORS['text_main']};
        }}
        /* 🔹 NUEVO: Header (franja de arriba) */
        header[data-testid="stHeader"] {{
            background-color: transparent;
            box-shadow: none;
        }}
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: #020b16;
            color: {AGTECH_COLORS['text_main']};
        }}

        /* Contenido principal */
        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }}

        /* Títulos */
        h1, h2, h3, h4 {{
            color: {AGTECH_COLORS['text_main']};
        }}

        /* Texto secundario */
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

        /* Separadores sutiles */
        hr {{
            border: none;
            border-top: 1px solid rgba(255,255,255,0.08);
            margin: 1.5rem 0;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 1. LOAD DATA + FEATURE ENGINEERING
# --------------------------------------------------


@st.cache_data
def load_data():
    #df = pd.read_excel(
    #     r"C:\Users\melic\OneDrive\Escritorio\coffee_streamlit_dashboard\coffee_shop_sales.xlsx"
    # )
    df = pd.read_excel("coffee_shop_sales.xlsx")

    # Ensure datetime formats
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["transaction_time"] = pd.to_datetime(df["transaction_time"], format="%H:%M:%S")

    # --- Feature engineering (same logic as in Colab) ---
    df["total_sales"] = df["unit_price"] * df["transaction_qty"]
    df["hour"] = df["transaction_time"].dt.hour
    df["day"] = df["transaction_date"].dt.day
    df["day_of_week"] = df["transaction_date"].dt.day_name()
    df["week_of_month"] = df["transaction_date"].dt.day.apply(lambda x: (x - 1) // 7 + 1)
    df["month"] = df["transaction_date"].dt.to_period("M").astype(str)
    df["month_name"] = df["transaction_date"].dt.month_name()

    def get_day_part(h):
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

# --------------------------------------------------
# 2. SIDEBAR FILTERS
# --------------------------------------------------

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

# --------------------------------------------------
# 3. HEADER
# --------------------------------------------------

st.markdown(
    f"""
    <h1>☕ Coffee Shop Sales Dashboard</h1>
    <p>Interactive sales analytics dashboard built with <b>Python, Streamlit and Plotly</b>.</p>
    """,
    unsafe_allow_html=True,
)

if selected_store != "All stores" or selected_month != "All months":
    active_filters = []
    if selected_store != "All stores":
        active_filters.append(f"Store: <b>{selected_store}</b>")
    if selected_month != "All months":
        active_filters.append(f"Month: <b>{selected_month}</b>")
    st.markdown(
        "Active filters: " + " &nbsp;|&nbsp; ".join(active_filters),
        unsafe_allow_html=True,
    )
else:
    st.markdown("Showing **all stores** and **all months**.")

st.markdown("---")

# --------------------------------------------------
# 4. MAIN KPIs (BUSINESS)
# --------------------------------------------------

total_revenue = filtered_df["total_sales"].sum()
total_tickets = filtered_df["transaction_id"].nunique()
aov = filtered_df["total_sales"].mean()

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total revenue</div>
            <div class="kpi-value">${total_revenue:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total tickets</div>
            <div class="kpi-value">{total_tickets:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Average order value (AOV)</div>
            <div class="kpi-value">${aov:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# --------------------------------------------------
# 5. MAIN BUSINESS CHARTS
# --------------------------------------------------

left_col, right_col = st.columns(2)

# --- Revenue by store ---
with left_col:
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
        color="store_location",
        color_discrete_sequence=[AGTECH_COLORS["accent_green"], "#1f9e5a", "#0a4b60"],
        labels={"store_location": "Store", "total_sales": "Revenue"},
    )
    fig_store.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    st.plotly_chart(fig_store, use_container_width=True)

# --- Revenue by month ---
with right_col:
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
        color_discrete_sequence=[AGTECH_COLORS["accent_green"]],
        labels={"month": "Month", "total_sales": "Revenue"},
    )
    fig_month.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_month, use_container_width=True)

# --- Revenue by day of week ---
st.subheader("Revenue by day of week")
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
    color="day_of_week",
    color_discrete_sequence=px.colors.sequential.YlGnBu,
    labels={"day_of_week": "Day", "total_sales": "Revenue"},
)
fig_dow.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
)
st.plotly_chart(fig_dow, use_container_width=True)

# --- Revenue by hour ---
st.subheader("Revenue by hour of day")
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
    color="hour",
    color_continuous_scale="YlGnBu",
    labels={"hour": "Hour", "total_sales": "Revenue"},
)
fig_hour.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    coloraxis_showscale=False,
)
st.plotly_chart(fig_hour, use_container_width=True)

st.markdown("---")

# --------------------------------------------------
# 6. SUPPORTING INSIGHTS (using engineered features)
# --------------------------------------------------

sup_left, sup_right = st.columns(2)

# --- Tickets by day part ---
with sup_left:
    st.subheader("Tickets by day part")
    tickets_by_part = (
        filtered_df.groupby("day_part")["transaction_id"]
        .count()
        .reset_index()
        .rename(columns={"transaction_id": "tickets"})
    )
    order_parts = ["Morning", "Lunch", "Afternoon", "Evening", "Late Night"]
    tickets_by_part["day_part"] = pd.Categorical(
        tickets_by_part["day_part"], categories=order_parts, ordered=True
    )
    tickets_by_part = tickets_by_part.sort_values("day_part")

    fig_part = px.bar(
        tickets_by_part,
        x="day_part",
        y="tickets",
        color="day_part",
        color_discrete_sequence=px.colors.sequential.Greens,
        labels={"day_part": "Day part", "tickets": "Number of tickets"},
    )
    fig_part.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    st.plotly_chart(fig_part, use_container_width=True)

# --- Top 10 products by revenue ---
with sup_right:
    st.subheader("Top 10 products by revenue")
    top_products = (
        filtered_df.groupby("product_type")["total_sales"]
        .sum()
        .reset_index()
        .sort_values("total_sales", ascending=False)
        .head(10)
    )
    fig_products = px.bar(
        top_products,
        x="total_sales",
        y="product_type",
        orientation="h",
        color="total_sales",
        color_continuous_scale="YlGnBu",
        labels={"product_type": "Product", "total_sales": "Revenue"},
    )
    fig_products.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_products, use_container_width=True)

st.markdown("---")
# --------------------------------------------------
# 6. SUPPORTING METRICS – HEATMAP & DAY PART
# --------------------------------------------------

st.markdown("### Supporting metrics")

# 6.1 Heatmap: Revenue by day of week and hour
st.subheader("Revenue heatmap by day of week and hour")

pivot = (
    filtered_df
    .pivot_table(
        values="total_sales",
        index="day_of_week",
        columns="hour",
        aggfunc="sum"
    )
)

# Ordenar días correctamente
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot = pivot.reindex(order)

heatmap_colors = ["#020B10", "#0A4B60", "#2E5E2A", "#A6CE39"]

fig_heatmap = px.imshow(
    pivot,
    aspect="auto",
    color_continuous_scale=heatmap_colors,
    labels={"x": "Hour of day", "y": "Day of week", "color": "Revenue"},
)

fig_heatmap.update_layout(
    xaxis_title="Hour of day",
    yaxis_title="Day of week",
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# 6.2 Revenue by day part (Morning, Lunch, Afternoon...)
st.subheader("Revenue by day part")

day_part_order = ["Morning", "Lunch", "Afternoon", "Evening", "Late Night"]

revenue_by_day_part = (
    filtered_df
    .groupby("day_part")["total_sales"]
    .sum()
    .reindex(day_part_order)
    .reset_index()
)

fig_day_part = px.bar(
    revenue_by_day_part,
    x="day_part",
    y="total_sales",
    title="Revenue by day part",
    labels={"day_part": "Day part", "total_sales": "Revenue"},
    color="day_part",
    color_discrete_sequence=["#0A4B60", "#2E5E2A", "#355E12", "#A6CE39", "#0A1F1A"],
)

st.plotly_chart(fig_day_part, use_container_width=True)

# --------------------------------------------------
# 7. DETAILED TABLE
# --------------------------------------------------

st.subheader("Detailed transactions table")
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

# --------------------------------------------------
# 8. FOOTER
# --------------------------------------------------

st.markdown(
    f"""
    <hr>
    <div style="text-align: center; font-size: 0.85rem; color: {AGTECH_COLORS['text_muted']}; margin-top: 0.5rem;">
        Built by <b>Melisa Cardozo</b> · Data Analyst / Data Scientist (AgTech)
    </div>
    """,
    unsafe_allow_html=True,
)
```python
st.markdown(
    f"""
    <div style="text-align:center; font-size:0.8rem; color:{AGTECH_COLORS['text_muted']}; margin-top:0.5rem;">
        View source code on <a href="https://github.com/Melisa-Cardozo/coffee-shop-sales-dashboard" target="_blank">GitHub</a>.
    </div>
    """,
    unsafe_allow_html=True,
)

