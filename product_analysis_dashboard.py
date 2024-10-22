import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('Superstore Dataset.csv')
    return data

data = load_data()

# Convert the 'Order Date' column to datetime
data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y', errors='coerce')

# Set the title of the dashboard
st.title("Product Analysis Dashboard")

# Create a sub-category filter
sub_categories = data['Sub-Category'].unique()
selected_sub_category = st.selectbox("Select a Sub-Category", sub_categories)

# Filter data by selected sub-category
filtered_data = data[data['Sub-Category'] == selected_sub_category]

# Display products in the selected sub-category
st.subheader(f'{selected_sub_category}')
products = filtered_data['Product Name'].unique()
selected_product = st.selectbox("Select a Product", products)

# Filter data by selected product
product_data = filtered_data[filtered_data['Product Name'] == selected_product]

# Date range filter with an option for "No Filter"
date_filter = st.selectbox("Filter by", ["No Filter", "Days", "Weeks", "Months", "Years"])

# Initialize a variable to track if any information should be displayed
display_info = False

if date_filter != "No Filter":
    product_data.set_index('Order Date', inplace=True)
    if date_filter == "Days":
        product_data = product_data.resample('D').sum().reset_index()
    elif date_filter == "Weeks":
        product_data = product_data.resample('W').sum().reset_index()
    elif date_filter == "Months":
        product_data = product_data.resample('M').sum().reset_index()
    elif date_filter == "Years":
        product_data = product_data.resample('Y').sum().reset_index()
        
    # Filter out rows where Sales are zero or NaN
    filtered_output = product_data[['Order Date', 'Ship Mode', 'Segment', 'Country', 'City', 'State', 'Sales']]
    filtered_output = filtered_output[filtered_output['Sales'] > 0].dropna()  # Only keep rows where Sales > 0 and remove NaNs

    # Set to True since we are displaying filtered data
    display_info = not filtered_output.empty

# Display product details only if there is data to show
if display_info:
    st.subheader(f'{selected_product}')
    st.write(filtered_output)
else:
    if date_filter == "No Filter":
        st.subheader("No Filter Selected")
        st.write("No information to display. Please select a filter to view the details.")
    else:
        st.subheader("No Available Data")
        st.write(f"No available data for '{selected_product}' with the selected filter '{date_filter}'.")

