import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Data Insights Dashboard", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Replace 'your_data.csv' with your actual filename
    df = pd.read_csv('your_data.csv') 
    return df

try:
    df = load_data()

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Options")
    # Example: filtering by a category column
    category = st.sidebar.multiselect(
        "Select Category:",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    df_selection = df.query("Category == @category")

    # --- MAIN PAGE ---
    st.title("📊 Business Intelligence Dashboard")
    st.markdown("##")

    # TOP KPI METRICS
    total_sales = int(df_selection["Sales"].sum())
    average_rating = round(df_selection["Rating"].mean(), 1)
    
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"US $ {total_sales:,}")
    with right_column:
        st.subheader("Average Rating:")
        st.subheader(f"{average_rating} ⭐")

    st.markdown("---")

    # CHARTS
    # 1. Bar Chart
    sales_by_product = df_selection.groupby(by=["Product"]).sum()[["Sales"]].sort_values(by="Sales")
    fig_product_sales = px.bar(
        sales_by_product,
        x="Sales",
        y=sales_by_product.index,
        orientation="h",
        title="<b>Sales by Product</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product),
        template="plotly_white",
    )
    
    st.plotly_chart(fig_product_sales, use_container_width=True)

    # 2. Data Table
    with st.expander("View Raw Filtered Data"):
        st.dataframe(df_selection)

except Exception as e:
    st.error(f"Please upload a valid data file. Error: {e}")
