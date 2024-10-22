import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('Superstore Sales Dataset.csv')
    return data

data = load_data()

# Set the title of the dashboard
st.title("Product Analysis Dashboard")

# Create a sub-category filter
sub_categories = data['Sub-Category'].unique()
selected_sub_category = st.selectbox("Select a Sub-Category", sub_categories)

# Filter data by selected sub-category
filtered_data = data[data['Sub-Category'] == selected_sub_category]

# Display products in the selected sub-category
st.subheader(f"Products in '{selected_sub_category}'")
products = filtered_data['Product Name'].unique()
selected_product = st.selectbox("Select a Product", products)

# Filter data by selected product
product_data = filtered_data[filtered_data['Product Name'] == selected_product]

# Display product details
st.subheader(f"Details for '{selected_product}'")

# Date range filter
date_filter = st.selectbox("Filter by", ["Days", "Weeks", "Months", "Years"])
product_data['Order Date'] = pd.to_datetime(product_data['Order Date'])
product_data.set_index('Order Date', inplace=True)

if date_filter == "Days":
    product_data = product_data.resample('D').sum().reset_index()
elif date_filter == "Weeks":
    product_data = product_data.resample('W').sum().reset_index()
elif date_filter == "Months":
    product_data = product_data.resample('M').sum().reset_index()
elif date_filter == "Years":
    product_data = product_data.resample('Y').sum().reset_index()

# Display filtered data
st.write(product_data)

# Display transaction details
st.subheader(f"Transaction Details for '{selected_product}'")
st.write(product_data[['Order Date', 'Ship Date', 'Ship Mode', 'City', 'State', 'Postal Code', 'Region', 'Category', 'Sales']])
