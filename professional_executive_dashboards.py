# -*- coding: utf-8 -*-

import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Executive KPI Dashboards", layout="wide")

st.title("Executive KPI Dashboards")

# =====================================================
# LOAD DATASETS
# =====================================================
@st.cache_data
def load_data():
    """
    Load CSV files from the current directory.
    If files are missing (common on Streamlit Cloud), show a clear error message.
    """
    import os

    required_files = [
        "Manufacturing_Smart_Factory.csv",
        "UX_Digital_Experience.csv",
        "E_commerce_Sales.csv",
        "IoT_Building_Energy.csv",
        "Healthcare_Analytics.csv",
        "Telecom_Churn.csv",
        "Banking_Transactions.csv",
        "Education_Performance.csv",
        "Logistics_Supply_Chain.csv",
        "Social_Media_Performance.csv",
        "HR_Analytics.csv",
        "Climate_Weather.csv",
        "Stock_Market.csv",
        "Smart_Traffic_Analytics.csv",
    ]

    missing = [f for f in required_files if not os.path.exists(f)]

    if missing:
        st.error("❌ Missing dataset files in repository:")
        st.code("".join(missing))
        st.info("Upload these CSV files to your GitHub repo (same folder as this script) and redeploy.")
        st.stop()

    manufacturing = pd.read_csv("Manufacturing_Smart_Factory.csv")
    ux = pd.read_csv("UX_Digital_Experience.csv")
    ecom = pd.read_csv("E_commerce_Sales.csv")
    iot = pd.read_csv("IoT_Building_Energy.csv")
    health = pd.read_csv("Healthcare_Analytics.csv")
    telecom = pd.read_csv("Telecom_Churn.csv")
    bank = pd.read_csv("Banking_Transactions.csv")
    edu = pd.read_csv("Education_Performance.csv")
    logistics = pd.read_csv("Logistics_Supply_Chain.csv")
    social = pd.read_csv("Social_Media_Performance.csv")
    hr = pd.read_csv("HR_Analytics.csv")
    weather = pd.read_csv("Climate_Weather.csv")
    stock = pd.read_csv("Stock_Market.csv")
    traffic = pd.read_csv("Smart_Traffic_Analytics.csv")

    # Convert dates safely
    for df, col in [
        (manufacturing, "timestamp"),
        (ux, "timestamp"),
        (iot, "timestamp"),
        (health, "admission_date"),
        (bank, "transaction_date"),
        (logistics, "ship_date"),
        (social, "date"),
        (weather, "date"),
        (stock, "date"),
        (traffic, "timestamp"),
    ]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return (
        manufacturing,
        ux,
        ecom,
        iot,
        health,
        telecom,
        bank,
        edu,
        logistics,
        social,
        hr,
        weather,
        stock,
        traffic,
    )

(manufacturing, ux, ecom, iot, health, telecom,
 bank, edu, logistics, social, hr, weather, stock, traffic) = load_data()

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
question = st.sidebar.selectbox(
    "Select Dashboard Question",
    [f"Question {i}" for i in range(1, 29)]
)

# =====================================================
# KPI HELPER
# =====================================================
def show_kpis(kpis):
    cols = st.columns(len(kpis))
    for col, (title, value) in zip(cols, kpis.items()):
        col.metric(title, value)

# =====================================================
# DASHBOARDS
# =====================================================

# ---------------- Manufacturing ----------------
if question in ["Question 1", "Question 15"]:
    kpis = {
        "Total Production": f"{manufacturing['production_units'].sum():,.0f}",
        "Avg Efficiency %": f"{manufacturing['efficiency_pct'].mean():.1f}%",
        "Defect Rate": f"{manufacturing['defect_rate'].mean():.2%}",
        "Downtime Hours": f"{manufacturing['downtime_min'].sum()/60:,.1f}"
    }
    show_kpis(kpis)

    fig = px.line(manufacturing, x="timestamp", y="efficiency_pct", title="Efficiency Trend")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- UX ----------------
elif question in ["Question 2", "Question 16"]:
    kpis = {
        "Total Sessions": len(ux),
        "Conversion Rate": f"{ux['conversion'].mean():.2%}",
        "Avg Session Duration": f"{ux['session_duration'].mean():.1f}s",
        "Bounce Rate": f"{ux['bounce'].mean():.2%}"
    }
    show_kpis(kpis)

    fig = px.histogram(ux, x="device", color="bounce", title="Bounce Rate by Device")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Ecommerce ----------------
elif question in ["Question 3", "Question 17"]:
    kpis = {
        "Revenue": f"${ecom['revenue'].sum():,.0f}",
        "Profit": f"${ecom['profit'].sum():,.0f}",
        "Profit Margin": f"{ecom['profit_margin'].mean():.2%}",
        "Avg Discount": f"{ecom['discount'].mean():.2%}"
    }
    show_kpis(kpis)

    fig = px.scatter(ecom, x="revenue", y="profit", color="category", title="Revenue vs Profit")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- IoT ----------------
elif question in ["Question 4", "Question 18"]:
    kpis = {
        "Total Power": f"{iot['power_kw'].sum():,.0f} kW",
        "Avg Temperature": f"{iot['temperature'].mean():.1f}°C",
        "Energy Cost": f"${iot['energy_cost'].sum():,.0f}",
        "Anomalies": int(iot['anomaly'].sum())
    }
    show_kpis(kpis)

    fig = px.line(iot, x="timestamp", y="power_kw", title="Power Consumption Trend")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Healthcare ----------------
elif question in ["Question 5", "Question 19"]:
    kpis = {
        "Total Admissions": len(health),
        "Avg Length of Stay": f"{health['length_of_stay'].mean():.1f} days",
        "Avg Treatment Cost": f"${health['treatment_cost'].mean():,.0f}",
        "Readmission Rate": f"{health['readmission_flag'].mean():.2%}"
    }
    show_kpis(kpis)

    fig = px.box(health, x="department", y="length_of_stay", title="Stay by Department")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Telecom ----------------
elif question in ["Question 6", "Question 20"]:
    kpis = {
        "Total Customers": len(telecom),
        "Total Revenue": f"${telecom['revenue'].sum():,.0f}",
        "Avg Monthly Fee": f"${telecom['monthly_fee'].mean():.1f}",
        "Churn Rate": f"{telecom['churn'].mean():.2%}"
    }
    show_kpis(kpis)

    fig = px.scatter(telecom, x="tenure", y="revenue", color="churn", title="Revenue vs Tenure")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Banking ----------------
elif question in ["Question 7", "Question 21"]:
    kpis = {
        "Transactions": len(bank),
        "Total Value": f"${bank['amount'].sum():,.0f}",
        "Fraud Rate": f"{bank['fraud'].mean():.2%}",
        "Avg Risk Score": f"{bank['risk_score'].mean():.2f}"
    }
    show_kpis(kpis)

    fig = px.histogram(bank, x="amount", color="fraud", title="Fraud Distribution")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Education ----------------
elif question in ["Question 8", "Question 22"]:
    kpis = {
        "Avg Final Score": f"{edu['final'].mean():.1f}",
        "Pass Rate": f"{(edu['final']>=50).mean():.2%}",
        "Avg Attendance": f"{edu['attendance'].mean():.1f}%"
    }
    show_kpis(kpis)

    fig = px.histogram(edu, x="grade", title="Grade Distribution")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Logistics ----------------
elif question in ["Question 9", "Question 23"]:
    kpis = {
        "Total Shipments": len(logistics),
        "Avg Delivery Time": f"{logistics['delivery_hours'].mean():.1f}h",
        "Late Delivery Rate": f"{logistics['late'].mean():.2%}",
        "Cost per KM": f"{logistics['cost_per_km'].mean():.2f}"
    }
    show_kpis(kpis)

    fig = px.bar(logistics, x="region", y="late", title="Late Deliveries by Region")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Social ----------------
elif question in ["Question 10", "Question 24", "Question 25"]:
    kpis = {
        "Total Posts": len(social),
        "Total Engagement": f"{(social['likes']+social['comments']+social['shares']).sum():,.0f}",
        "Avg Engagement Rate": f"{social['engagement_rate'].mean():.2%}",
        "Top Platform": social.groupby('platform')['engagement_rate'].mean().idxmax()
    }
    show_kpis(kpis)

    fig = px.line(social, x="date", y="engagement_rate", title="Engagement Trend")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- HR ----------------
elif question == "Question 11":
    kpis = {
        "Employees": len(hr),
        "Avg Salary": f"${hr['salary'].mean():,.0f}",
        "Avg Performance": f"{hr['performance'].mean():.2f}",
        "Attrition Rate": f"{hr['attrition'].mean():.2%}"
    }
    show_kpis(kpis)

    fig = px.bar(hr, x="department", y="attrition", title="Attrition by Department")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Weather ----------------
elif question in ["Question 12", "Question 26"]:
    kpis = {
        "Avg Temperature": f"{weather['temperature'].mean():.1f}°C",
        "Total Rainfall": f"{weather['rainfall'].sum():.1f}",
        "Max Wind": f"{weather['wind'].max():.1f}",
        "Storm Rate": f"{weather['storm'].mean():.2%}"
    }
    show_kpis(kpis)

    fig = px.line(weather, x="date", y="temperature", title="Temperature Trend")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Stock ----------------
elif question in ["Question 13", "Question 27"]:
    kpis = {
        "Avg Open": f"{stock['open'].mean():.2f}",
        "Avg Close": f"{stock['close'].mean():.2f}",
        "Total Volume": f"{stock['volume'].sum():,.0f}",
        "Avg Daily Return": f"{stock['daily_return'].mean():.2%}"
    }
    show_kpis(kpis)

    fig = px.scatter(stock, x="close", y="volume", color="daily_return", title="Price vs Volume")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Traffic ----------------
elif question in ["Question 14", "Question 28"]:
    kpis = {
        "Total Vehicles": f"{traffic['vehicles'].sum():,.0f}",
        "Avg Speed": f"{traffic['avg_speed'].mean():.1f}",
        "Congestion Rate": f"{traffic['congestion'].mean():.2%}",
        "Flow Index": f"{traffic['flow_index'].mean():,.0f}"
    }
    show_kpis(kpis)

    fig = px.line(traffic, x="timestamp", y="vehicles", title="Traffic Volume Trend")
    st.plotly_chart(fig, use_container_width=True)

st.info("Dashboard not implemented for this selection.")
