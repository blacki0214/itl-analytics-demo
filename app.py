import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

st.set_page_config(page_title="ITL Logistics Analytics", layout="wide")

st.title("ITL Predictive Fleet Maintenance Dashboard")
st.markdown("**Advanced analytics for proactive fleet management and maintenance optimization**")

# 1. Load data
@st.cache_data
def load_data():
    df = pd.read_csv("./data/fleet_data_large.csv")
    df["last_service_date"] = pd.to_datetime(df["last_service_date"])
    df["days_since_service"] = df["last_service_date"].apply(
        lambda d: (pd.Timestamp.now() - d).days if pd.notna(d) else None
    )
    df["breakdown_rate"] = df["breakdowns_last_6m"] / df["engine_hours"]
    return df

df = load_data()

def risk_row(r):
    if r["days_since_service"] > 90 or r["breakdown_rate"] > 0.002:
        return "High"
    elif r["days_since_service"] > 60:
        return "Medium"
    else:
        return "Low"

df["risk_level"] = df.apply(risk_row, axis=1)

# Sidebar filters
st.sidebar.header("🔍 Filters")
depots = ["All"] + sorted(df["depot"].unique().tolist())
selected_depot = st.sidebar.selectbox("Filter by Depot", depots)

risk_filter = st.sidebar.multiselect(
    "Filter by Risk Level",
    options=["High", "Medium", "Low"],
    default=["High", "Medium", "Low"]
)

if selected_depot != "All":
    df = df[df["depot"] == selected_depot]

df = df[df["risk_level"].isin(risk_filter)]

# KPIs
st.subheader("📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Vehicles", len(df), delta=None)
with col2:
    high_risk = (df["risk_level"] == "High").sum()
    st.metric("High Risk Vehicles", high_risk, delta=f"{high_risk/len(df)*100:.1f}%")
with col3:
    avg_days = int(df["days_since_service"].mean())
    st.metric("Avg Days Since Service", avg_days)
with col4:
    total_breakdowns = df["breakdowns_last_6m"].sum()
    st.metric("Total Breakdowns (6M)", int(total_breakdowns))

st.divider()

# Main Charts Section
st.subheader("📈 Fleet Analytics")

# Row 1: Two columns
col_left, col_right = st.columns(2)

with col_left:
    # Get a balanced sample across all risk levels
    high_risk_sample = df[df["risk_level"] == "High"].nlargest(10, "days_since_service")
    medium_risk_sample = df[df["risk_level"] == "Medium"].nlargest(5, "days_since_service")
    low_risk_sample = df[df["risk_level"] == "Low"].nlargest(5, "days_since_service")
    
    mixed_sample = pd.concat([high_risk_sample, medium_risk_sample, low_risk_sample])
    
    fig1 = px.bar(
        mixed_sample.sort_values("days_since_service", ascending=False),
        x="vehicle_id",
        y="days_since_service",
        color="risk_level",
        title="Top Vehicles by Risk Level - Days Since Last Service",
        color_discrete_map={"High": "#FF4B4B", "Medium": "#FFA500", "Low": "#00CC66"},
        labels={"days_since_service": "Days", "vehicle_id": "Vehicle ID"}
    )
    fig1.update_layout(showlegend=True, xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    # Risk Distribution Pie Chart
    risk_counts = df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]
    fig2 = px.pie(
        risk_counts,
        names="risk_level",
        values="count",
        title="Fleet Risk Distribution",
        color="risk_level",
        color_discrete_map={"High": "#FF4B4B", "Medium": "#FFA500", "Low": "#00CC66"},
        hole=0.4
    )
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Three columns
col_a, col_b, col_c = st.columns(3)

with col_a:
    # Breakdown Rate Distribution
    fig3 = px.histogram(
        df,
        x="breakdown_rate",
        nbins=30,
        title="Breakdown Rate Distribution",
        labels={"breakdown_rate": "Breakdown Rate"},
        color_discrete_sequence=["#636EFA"]
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_b:
    # Depot-wise Risk Analysis
    depot_risk = df.groupby(["depot", "risk_level"]).size().reset_index(name="count")
    fig4 = px.bar(
        depot_risk,
        x="depot",
        y="count",
        color="risk_level",
        title="Risk Level by Depot",
        color_discrete_map={"High": "#FF4B4B", "Medium": "#FFA500", "Low": "#00CC66"},
        barmode="stack"
    )
    st.plotly_chart(fig4, use_container_width=True)

with col_c:
    # Engine Hours vs Breakdowns Scatter
    fig5 = px.scatter(
        df,
        x="engine_hours",
        y="breakdowns_last_6m",
        color="risk_level",
        title="Engine Hours vs Breakdowns",
        color_discrete_map={"High": "#FF4B4B", "Medium": "#FFA500", "Low": "#00CC66"},
        hover_data=["vehicle_id", "depot"],
        size="days_since_service",
        labels={"engine_hours": "Engine Hours", "breakdowns_last_6m": "Breakdowns (6M)"}
    )
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# Row 3: Full-width advanced charts
tab1, tab2 = st.tabs(["📅 Service Timeline", "🔧 Detailed Analytics"])

with tab1:
    # Service Timeline Gantt-style Chart
    fig6 = px.scatter(
        df.sort_values("days_since_service", ascending=False),
        x="days_since_service",
        y="vehicle_id",
        color="risk_level",
        title="Vehicle Service Status Timeline",
        color_discrete_map={"High": "#FF4B4B", "Medium": "#FFA500", "Low": "#00CC66"},
        hover_data=["depot", "breakdowns_last_6m"],
        height=600
    )
    fig6.add_vline(x=60, line_dash="dash", line_color="orange", annotation_text="Medium Risk Threshold")
    fig6.add_vline(x=90, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
    st.plotly_chart(fig6, use_container_width=True)

with tab2:
    # Multi-metric correlation heatmap
    col_heat1, col_heat2 = st.columns(2)
    
    with col_heat1:
        # Box plot for breakdown distribution by depot
        fig7 = px.box(
            df,
            x="depot",
            y="breakdowns_last_6m",
            color="risk_level",
            title="Breakdown Distribution by Depot",
            color_discrete_map={"High": "#FF4B4B", "Medium": "#FFA500", "Low": "#00CC66"}
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    with col_heat2:
        # Violin plot for engine hours distribution
        fig8 = px.violin(
            df,
            x="risk_level",
            y="engine_hours",
            color="risk_level",
            title="Engine Hours Distribution by Risk Level",
            color_discrete_map={"High": "#FF4B4B", "Medium": "#FFA500", "Low": "#00CC66"},
            box=True
        )
        st.plotly_chart(fig8, use_container_width=True)

st.divider()

# Data Table Section
st.subheader("📋 Detailed Fleet Data")

# Add search and filtering
search = st.text_input("🔍 Search by Vehicle ID", "")
if search:
    df = df[df["vehicle_id"].str.contains(search, case=False)]

# Color-code the dataframe
def color_risk(val):
    color_map = {"High": "background-color: #ffcccc", 
                 "Medium": "background-color: #fff4cc",
                 "Low": "background-color: #ccffcc"}
    return color_map.get(val, "")

styled_df = df.style.applymap(color_risk, subset=["risk_level"])
st.dataframe(styled_df, use_container_width=True, height=400)

# Download button
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name=f"fleet_data_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# Footer
st.divider()
st.markdown("**ITL Logistics Analytics** | Powered by Advanced Predictive Maintenance")
