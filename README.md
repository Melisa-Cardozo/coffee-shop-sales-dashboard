# ☕ Coffee Shop Sales Dashboard (Python + Streamlit)

Interactive sales analytics dashboard for a coffee shop chain.  
Built with **Python, Streamlit, Plotly and Pandas**, focused on clear business KPIs and supporting insights.

🔗 **Live app:**https://coffee-shop-sales-dashboard.streamlit.app/
💻 **Tech stack:** Python · Pandas · Plotly · Streamlit

---

## 🔍 Project overview

This project simulates the work of a **Data Analyst / BI Developer** building a dashboard for a coffee shop chain that operates multiple stores.

The goal is to help business stakeholders answer questions such as:

- Which **store** generates the highest revenue?
- How does **revenue evolve by month**?
- What are the **busiest days and hours**?
- Which **products** drive most revenue?
- How do **day parts** (morning, lunch, afternoon, evening) impact sales?

---

## 📊 Main features

- Global interactive filters:
  - Filter by **store**
  - Filter by **month (YYYY-MM)**
- Business KPIs:
  - **Total revenue**
  - **Total tickets**
  - **Average order value (AOV)**
- Main charts:
  - Revenue by **store**
  - Revenue by **month**
  - Revenue by **day of week**
  - Revenue by **hour of day**
- Supporting insights:
  - Tickets by **day part** (Morning / Lunch / Afternoon / Evening / Late Night)
  - Top 10 products by revenue
  - **Heatmap**: revenue by day of week × hour
  - Revenue by day part
- Detailed transactions table with:
  - Date, store, product type, quantity, unit price, total sales, weekday, hour, day part.

---

## 🧮 Data & feature engineering

The dataset comes from a public **coffee shop sales** dataset (Kaggle style, transactional format).

On top of the raw data, I engineered:

- `total_sales` = `unit_price` × `transaction_qty`
- `hour` (from transaction time)
- `day`, `day_of_week`, `week_of_month`
- `month` (YYYY-MM) and `month_name`
- `day_part` (Morning, Lunch, Afternoon, Evening, Late Night)

These features are used both in the **KPIs** and in the **supporting charts**.

---

## 🛠 Tech stack

- **Python 3**
- **Pandas** for data manipulation
- **Plotly Express** for interactive charts
- **Streamlit** for the web app
- **openpyxl** to read the Excel file

---

## 🚀 How to run locally

```bash
# 1. Clone this repo
git clone https://github.com/Melisa-Cardozo/coffee-shop-sales-dashboard.git
cd coffee-shop-sales-dashboard

# 2. (Optional) Create and activate a virtual environment

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py

👩‍💻 About me

I’m Melisa Cardozo, an Economist and Data Science Master’s student transitioning into Data Analytics / Data Science roles, with a strong interest in AgTech, sustainability and business analytics.
h, sustainability and business analytics.

🌐 LinkedIn: https://www.linkedin.com/in/melisacardozo/
