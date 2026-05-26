import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Pump Kiraya App", page_icon="🚜", layout="centered")

DATA_FILE = "pump_data.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Tariqh", "Kisan_Nam", "Ghante", "Rate", "Kul_Kiraya", "Mila_Paisa", "Baki_Paisa", "Note"])
    df.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.title("🚜 सबमर्सिबल पंप किराया खाता")
st.write("अपने पंप के किराये और उधारी का हिसाब यहाँ रखें।")

st.header("➕ नई एंट्री जोड़ें")
with st.form("entry_form", clear_on_submit=True):
    tariqh = st.date_input("तारीख (Date)", datetime.now())
    kisan_nam = st.text_input("किसान का नाम (Farmer Name)")
    ghante = st.number_input("कुल कितने घंटे चला? (Hours)", min_value=0.1, step=0.5, value=1.0)
    rate = st.number_input("रेट (प्रति घंटा ₹)", value=150, disabled=True)
    mila_paisa = st.number_input("कितने पैसे मिले? (Received)", min_value=0, value=0)
    note = st.text_input("कोई नोट या पेमेंट का तरीका (UPI/Cash)")
    
    submitted = st.form_submit_button("हिसाब सेव करें")
    
    if submitted:
        if kisan_nam == "":
            st.error("कृपया किसान का नाम ज़रूर लिखें!")
        else:
            kul_kiraya = ghante * rate
            baki_paisa = kul_kiraya - mila_paisa
            
            df = load_data()
            new_row = {
                "Tariqh": tariqh.strftime("%Y-%m-%d"),
                "Kisan_Nam": kisan_nam,
                "Ghante": ghante,
                "Rate": rate,
                "Kul_Kiraya": kul_kiraya,
                "Mila_Paisa": mila_paisa,
                "Baki_Paisa": baki_paisa,
                "Note": note
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success(f"✅ {kisan_nam} का हिसाब सेव हो गया!")

df = load_data()

if not df.empty:
    st.header("📊 कुल जमा-पूंजी का हिसाब")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("कुल कमाई", f"₹{df['Kul_Kiraya'].sum():,}")
    with col2:
        st.metric("कुल मिला पैसा", f"₹{df['Mila_Paisa'].sum():,}")
    with col3:
        st.metric("कुल बाकी उधारी", f"₹{df['Baki_Paisa'].sum():,}")

    st.header("👥 किसान अनुसार उधारी (Summary)")
    summary = df.groupby("Kisan_Nam").agg(
        कुल_घंटे=("Ghante", "sum"),
        कुल_किराया=("Kul_Kiraya", "sum"),
        कुल_मिला=("Mila_Paisa", "sum"),
        अभी_बाकी_उधारी=("Baki_Paisa", "sum")
    ).reset_index()
    st.dataframe(summary, use_container_width=True)

    st.header("📜 रोज़ाना की पूरी लिस्ट")
    st.dataframe(df, use_container_width=True)
