import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import streamlit as st

# Load Firebase credentials
cred = credentials.Certificate("C:\Users\zpson\OneDrive\Desktop\APNG Project\price-optimization-9a019-firebase-adminsdk-fbsvc-fc5b4ca96a.json")  # Replace with your file
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to upload data to Firestore
def save_to_firebase(origin, destination, date, price):
    doc_ref = db.collection("flight_prices").document(f"{origin}_{destination}_{date}")
    doc_ref.set({
        "origin": origin,
        "destination": destination,
        "date": date,
        "price": price
    })
    print("✅ Data saved to Firebase!")

# Function to fetch data from Firestore
def get_data():
    flights_ref = db.collection("flight_prices")
    docs = flights_ref.stream()
    
    data = []
    for doc in docs:
        data.append(doc.to_dict())

    return pd.DataFrame(data)

# Streamlit UI
st.title("Japan Domestic Flight Price Tracker ✈️")

data = get_data()

if not data.empty:
    st.subheader("📊 Raw Data")
    st.dataframe(data)

    # Filter and visualize
    origin = st.selectbox("Select Origin Airport:", sorted(data['origin'].unique()))
    destination = st.selectbox("Select Destination Airport:", sorted(data[data['origin'] == origin]['destination'].unique()))
    
    filtered_data = data[(data['origin'] == origin) & (data['destination'] == destination)]

    if not filtered_data.empty:
        st.subheader("📈 Price Trends Over Time")
        st.line_chart(filtered_data.set_index("date")["price"])
    else:
        st.warning("No data available for this route.")
else:
    st.warning("No flight price data available yet.")
