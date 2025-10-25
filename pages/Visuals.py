# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Screen Time Visualizations")
st.write("This page displays graphs based on the Screen Time Survey.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")
try:
    if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
        csv_data = pd.read_csv("data.csv")
        st.success("CSV file loaded successfully!")
    else:
        csv_data = pd.DataFrame()
        st.warning("'data.csv' not found or empty.")
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    csv_data = pd.DataFrame()

try:
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            json_data = json.load(f)
        st.success("JSON file loaded successfully!")
    else:
        json_data = {}
        st.warning("'data.json' not found.")
except Exception as e:
    st.error(f"Error loading JSON: {e}")
    json_data = {}

st.divider()
st.header("Graphs")

# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Average Screen Time (Static)")
if not csv_data.empty:
    try:
        # Only use numeric columns for chart
        numeric_df = csv_data.select_dtypes(include='number')
        if not numeric_df.empty:
            st.bar_chart(numeric_df)
            st.write("This bar chart shows your collected numeric data, such as hours on phone, focus, and productivity levels.")
        else:
            st.warning("No numeric data to display yet, please fill out the survey to collect more!")
    except Exception as e:
        st.error(f"Error displaying static graph: {e}")
else:
    st.warning("No data available in CSV for this chart yet.")
    
# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Focus Level by Productivity (Dynamic)")
if not csv_data.empty:
    numeric_cols = csv_data.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        x_axis = st.selectbox("Select X-axis", numeric_cols, key="x_axis_select")
        y_axis = st.selectbox("Select Y-axis", numeric_cols, key="y_axis_select")
        st.line_chart(csv_data[[x_axis, y_axis]])
        st.write(f"This line chart shows the relationship between **{x_axis}** and **{y_axis}**.")
    else:
        st.warning("Not enough numeric columns in CSV for dynamic comparison.")
else:
    st.warning("No CSV data found for this graph.")
    

# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Average Metrics from JSON (Dynamic)")
if json_data:
    try:
        json_df = pd.DataFrame(json_data["data_points"])
        st.dataframe(json_df)
        chart_type = st.radio("Choose chart type:", ["Bar Chart", "Line Chart"], key="chart_type")
        if chart_type == "Bar Chart":
            st.bar_chart(json_df.set_index("label"))
        else:
            st.line_chart(json_df.set_index("label"))
        st.write("This chart displays your average metrics stored in the JSON file.")
    except Exception as e:
        st.error(f"Error displaying JSON chart: {e}")
else:
    st.warning("No JSON data found for this chart.")
