import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# Connect to the SQLite database
def get_data():
    conn = sqlite3.connect("flight_prices.db")
    df = pd.read_sql("SELECT * FROM flight_prices", conn)
    conn.close()
    return df

# Streamlit UI
st.title("Japan Domestic Flight Price Tracker ✈️")

data = get_data()

if not data.empty:
    # Display raw data
    st.subheader("📊 Raw Data")
    st.dataframe(data)
    
    # Filter options
    origin = st.selectbox("Select Origin Airport:", sorted(data["origin"].unique()))
    destination = st.selectbox("Select Destination Airport:", sorted(data[data["origin"] == origin]["destination"].unique()))
    
    # Filter data based on selection
    filtered_data = data[(data["origin"] == origin) & (data["destination"] == destination)]
    
    if not filtered_data.empty:
        # Line Chart of Prices Over Time
        st.subheader("📈 Price Trends Over Time")
        fig = px.line(filtered_data, x="date", y="price", markers=True, title=f"Ticket Prices: {origin} to {destination}")
        st.plotly_chart(fig)
        
        # Summary statistics
        st.subheader("📌 Statistics")
        st.write(filtered_data[["price"]].describe())
    else:
        st.warning("No data available for the selected route.")
else:
    st.warning("No flight price data available yet. Please wait for the next scheduled update.")

st.write("Powered by Skyscanner API 🚀")