import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(
    page_title="Financial Fraud Detection Dashboard",
    layout="wide"
)

st.title("🚨 Financial Fraud Detection Dashboard")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="fraud_detection"
)

query = """
SELECT *
FROM transactions
ORDER BY id DESC
"""

df = pd.read_sql_query(query, db)

selected_risk = st.selectbox(
    "Filter by Risk Level",
    ["All", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
)

if selected_risk != "All":
    df = df[df["risk_level"] == selected_risk]

fraud_count = len(df[df["prediction"] == "Fraud"])

avg_risk = round(df["risk_score"].mean(), 2)

fraud_rate = round(
    (fraud_count / len(df)) * 100,
    2
) if len(df) > 0 else 0

critical_count = len(
    df[df["risk_level"] == "CRITICAL"]
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Transactions",
    len(df)
)

col2.metric(
    "Fraud Transactions",
    fraud_count
)

col3.metric(
    "Average Risk Score",
    avg_risk
)

col4.metric(
    "Fraud Rate (%)",
    f"{fraud_rate}%"
)

col5.metric(
    "Critical Risks",
    critical_count
)

st.divider()

st.subheader("📋 Recent Transactions")

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    risk_counts = df["risk_level"].value_counts()

    fig1 = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        title="Risk Level Distribution"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    fraud_counts = df["prediction"].value_counts()

    fig2 = px.pie(
        values=fraud_counts.values,
        names=fraud_counts.index,
        title="Fraud vs Genuine Transactions"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

col1, col2 = st.columns(2)

with col1:

    fig3 = px.histogram(
        df,
        x="transaction_type",
        title="Transaction Type Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col2:

    fig4 = px.line(
        df.head(300),
        x="id",
        y="risk_score",
        title="Risk Score Trend"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.divider()

st.subheader("🚨 Latest Fraud Transactions")

fraud_df = df[
    df["prediction"] == "Fraud"
]

st.dataframe(
    fraud_df.head(20),
    use_container_width=True
)

st.divider()

st.subheader("🔥 Top Risk Transactions")

top_risk = df.sort_values(
    by="risk_score",
    ascending=False
)

st.dataframe(
    top_risk.head(20),
    use_container_width=True
)

st.divider()

st.subheader("🚨 High Risk Transactions")

high_risk = df[
    df["risk_level"].isin(
        ["HIGH", "CRITICAL"]
    )
]

st.dataframe(
    high_risk,
    use_container_width=True
)

st.divider()

st.subheader("📢 Latest Fraud Alerts")

try:

    alerts_query = """
    SELECT *
    FROM fraud_alerts
    ORDER BY alert_id DESC
    LIMIT 10
    """

    alerts_df = pd.read_sql_query(
        alerts_query,
        db
    )

    st.dataframe(
        alerts_df,
        use_container_width=True
    )

except:

    st.warning(
        "No alerts available"
    )

st.divider()

st.subheader("📊 Risk Level Summary")

risk_summary = (
    df.groupby("risk_level")
    .size()
    .reset_index(name="Count")
)

st.dataframe(
    risk_summary,
    use_container_width=True
)

st.markdown("---")

st.markdown(
    """
    ### Financial Fraud Detection System

    **Technologies Used**
    - Apache Kafka
    - Machine Learning (Random Forest)
    - Customer Behavior Analysis
    - MySQL Database
    - FastAPI
    - Streamlit
    - Power BI

    Developed for Real-Time Financial Fraud Detection and Risk Analytics.
    """
)