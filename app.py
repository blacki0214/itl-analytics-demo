import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="ITL Logistics Analytics", layout="wide")

st.title("ITL Predictive Fleet Maintenance Demo")
st.write("This demo shows how ITL's analytics consultancy can ingest fleet data, clean it, score maintenance risk, and visualize it for the client.")

# 1. Load data
df = pd.read_csv("./data/fleet_data_large.csv")
df["last_service_date"] = pd.to_datetime(df["last_service_date"])
# compute days since last service per-row to avoid Timestamp - Series typing issues and handle missing dates
df["days_since_service"] = df["last_service_date"].apply(lambda d: (pd.Timestamp.now() - d).days if pd.notna(d) else None)
df["breakdown_rate"] = df["breakdowns_last_6m"] / df["engine_hours"]

def risk_row(r):
    if r["days_since_service"] > 90 or r["breakdown_rate"] > 0.002:
        return "High"
    elif r["days_since_service"] > 60:
        return "Medium"
    else:
        return "Low"

df["risk_level"] = df.apply(risk_row, axis=1)

# sidebar filters
depots = ["All"] + sorted(df["depot"].unique().tolist())
selected_depot = st.sidebar.selectbox("Filter by depot", depots)

if selected_depot != "All":
    df = df[df["depot"] == selected_depot]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Vehicles", len(df))
col2.metric("High Risk Vehicles", (df["risk_level"] == "High").sum())
col3.metric("Average Days Since Service", int(df["days_since_service"].mean()))

# charts
colA, colB = st.columns(2)

with colA:
    fig = px.bar(df, x="vehicle_id", y="days_since_service", color="risk_level",
                 title="Days Since Last Service by Vehicle")
    st.plotly_chart(fig, use_container_width=True)

with colB:
    risk_counts = df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]
    fig2 = px.pie(risk_counts, names="risk_level", values="count",
                  title="Fleet Risk Distribution")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(df)
