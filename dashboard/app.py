import os

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv


# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "supply_chain"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


# --------------------------------------------------
# Database connection
# --------------------------------------------------

@st.cache_resource
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# --------------------------------------------------
# Query helper
# --------------------------------------------------

@st.cache_data(ttl=300)
def run_query(query):
    conn = get_connection()
    return pd.read_sql_query(query, conn)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Supply Chain Analytics",
    page_icon="📦",
    layout="wide",
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📦 Supply Chain Analytics Dashboard")
st.caption("PostgreSQL Gold Layer")


# --------------------------------------------------
# KPI queries
# --------------------------------------------------

kpi_query = """
SELECT
    COUNT(*) AS total_orders,
    SUM(total_order_value) AS total_order_value,
    AVG(total_order_value) AS avg_order_value,
    COUNT(DISTINCT supplier_id) AS active_suppliers
FROM gold_supply_chain;
"""

kpi = run_query(kpi_query).iloc[0]


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Orders",
    f"{int(kpi['total_orders']):,}"
)

col2.metric(
    "Total Order Value",
    f"₹{kpi['total_order_value']:,.0f}"
)

col3.metric(
    "Average Order Value",
    f"₹{kpi['avg_order_value']:,.0f}"
)

col4.metric(
    "Active Suppliers",
    f"{int(kpi['active_suppliers']):,}"
)


st.divider()


# --------------------------------------------------
# Order Status
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Orders by Status")

    status_query = """
    SELECT
        status,
        COUNT(*) AS order_count
    FROM gold_supply_chain
    GROUP BY status
    ORDER BY order_count DESC;
    """

    status_df = run_query(status_query)

    st.bar_chart(
        status_df.set_index("status")
    )


# --------------------------------------------------
# Inventory Status
# --------------------------------------------------

with col2:

    st.subheader("Inventory Status")

    inventory_query = """
    SELECT
        stock_status,
        COUNT(*) AS record_count
    FROM gold_supply_chain
    GROUP BY stock_status
    ORDER BY record_count DESC;
    """

    inventory_df = run_query(inventory_query)

    st.bar_chart(
        inventory_df.set_index("stock_status")
    )


st.divider()


# --------------------------------------------------
# Supplier Performance
# --------------------------------------------------

st.subheader("Top 10 Suppliers by Order Value")

supplier_query = """
SELECT
    supplier_id,
    supplier_name,
    COUNT(*) AS order_count,
    ROUND(SUM(total_order_value), 2) AS total_order_value
FROM gold_supply_chain
GROUP BY supplier_id, supplier_name
ORDER BY total_order_value DESC
LIMIT 10;
"""

supplier_df = run_query(supplier_query)

st.dataframe(
    supplier_df,
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Country Performance
# --------------------------------------------------

st.subheader("Country Performance")

country_query = """
SELECT
    country,
    COUNT(*) AS order_count,
    ROUND(SUM(total_order_value), 2) AS total_order_value,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days
FROM gold_supply_chain
GROUP BY country
ORDER BY total_order_value DESC;
"""

country_df = run_query(country_query)

st.dataframe(
    country_df,
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Low Stock Products
# --------------------------------------------------

st.subheader("⚠️ Low Stock Products")

low_stock_query = """
SELECT DISTINCT
    product_id,
    stock_quantity,
    reorder_level,
    stock_status
FROM gold_supply_chain
WHERE stock_status = 'LOW_STOCK'
ORDER BY stock_quantity ASC;
"""

low_stock_df = run_query(low_stock_query)

st.dataframe(
    low_stock_df,
    use_container_width=True,
    hide_index=True,
)


st.caption("Data source: PostgreSQL → gold_supply_chain")