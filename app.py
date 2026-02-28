import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Data Dashboard")

# Load Data
dataset = pd.read_csv("superstore.csv",encoding='latin1')
dataset['Order Date'] = pd.to_datetime(dataset['Order Date'])

# Sidebar Filters
st.sidebar.header("Filter Options")

region = st.sidebar.multiselect(
    "Select Region",
    options=dataset['Region'].unique(),
    default=dataset['Region'].unique()
)



category = st.sidebar.multiselect(
    "Select Category",
    options=dataset['Category'].unique(),
    default=dataset['Category'].unique()
)

# Date Filter
min_date = dataset['Order Date'].min()
max_date = dataset['Order Date'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

filtered_data = dataset[
    (dataset['Region'].isin(region)) &
    (dataset['Category'].isin(category)) &
    (dataset['Order Date'] >= pd.to_datetime(date_range[0])) &
    (dataset['Order Date'] <= pd.to_datetime(date_range[1]))
]

# KPI Section
total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
total_orders = filtered_data['Order ID'].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", round(total_sales, 2))
col2.metric("Total Profit", round(total_profit, 2))
col3.metric("Total Orders", total_orders)
col4.metric("Profit Margin (%)", round(profit_margin, 2))
st.markdown("---")

# Row 1 Graphs
col4, col5 = st.columns(2)

with col4:
    st.subheader("Profit by Category")
    fig1, ax1 = plt.subplots()
    filtered_data.groupby('Category')['Profit'].sum().plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

with col5:
    st.subheader("Sales by Region")
    fig2, ax2 = plt.subplots()
    filtered_data.groupby('Region')['Sales'].sum().plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

# Row 2 Graphs
col6, col7 = st.columns(2)

with col6:
    st.subheader("Top 5 Products")
    top_products = filtered_data.groupby('Product Name')['Sales'].sum() \
        .sort_values(ascending=False).head(5).sort_values()
    fig3, ax3 = plt.subplots()
    top_products.plot(kind='barh', ax=ax3)
    st.pyplot(fig3)

with col7:
    st.subheader("Monthly Sales Trend")
    monthly_sales = filtered_data.groupby(
        filtered_data['Order Date'].dt.to_period('M')
    )['Sales'].sum()
    fig4, ax4 = plt.subplots()
    monthly_sales.plot(ax=ax4)
    st.pyplot(fig4)


    st.markdown("---")
st.subheader("🔴 Top 5 Loss Making Products")

loss_products = filtered_data.groupby('Product Name')['Profit'].sum() \
    .sort_values().head(5)

st.dataframe(loss_products)

st.subheader("🟢 Top 5 Profitable Products")

top_profit_products = filtered_data.groupby('Product Name')['Profit'].sum() \
    .sort_values(ascending=False).head(5)

st.dataframe(top_profit_products)


st.markdown("---")
st.subheader("📌 Business Summary")

category_profit = filtered_data.groupby('Category')['Profit'].sum()

best_category = category_profit.idxmax()
worst_category = category_profit.idxmin()

st.write(f"✅ Most Profitable Category: **{best_category}**")
st.write(f"⚠️ Least Profitable Category: **{worst_category}**")

st.markdown("---")
st.subheader("📥 Download Filtered Data")

csv = filtered_data.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)