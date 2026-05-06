import streamlit as st
import plotly.graph_objects as go
from analysis import *

st.set_page_config(page_title="Admission Analytics Dashboard", layout="wide")

st.title("🎓 Admission & Enrollment Analytics Dashboard")

# =========================
# FILE UPLOAD SECTION
# =========================
st.sidebar.header("📂 Upload Dataset Files")

leads_file = st.sidebar.file_uploader("Upload Leads File", type=["csv", "xlsx"])
counselling_file = st.sidebar.file_uploader("Upload Counselling File", type=["csv", "xlsx"])
applications_file = st.sidebar.file_uploader("Upload Applications File", type=["csv", "xlsx"])
enrollment_file = st.sidebar.file_uploader("Upload Enrollment File", type=["csv", "xlsx"])

# =========================
# MAIN LOGIC
# =========================
if leads_file and counselling_file and applications_file and enrollment_file:

    try:
        df = load_and_merge(leads_file, counselling_file, applications_file, enrollment_file)

        st.subheader("📄 Combined Dataset")
        st.dataframe(df, use_container_width=True)

        # =========================
        # FUNNEL METRICS
        # =========================
        total, counselling, application, enrolled = funnel_metrics(df)

        st.subheader("📊 Key Metrics")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Leads", total)
        col2.metric("Counselling", counselling)
        col3.metric("Applications", application)
        col4.metric("Enrolled", enrolled)

        # =========================
        # FUNNEL CHART
        # =========================
        st.subheader("📉 Admission Funnel")

        fig = go.Figure(go.Funnel(
            y=["Leads", "Counselling", "Application", "Enrollment"],
            x=[total, counselling, application, enrolled]
        ))

        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # CONVERSION RATES
        # =========================
        st.subheader("📈 Conversion Rates")

        rates = conversion_rates(total, counselling, application, enrolled)

        for k, v in rates.items():
            st.write(f"**{k}** : {round(v * 100, 2)}%")

        # =========================
        # DROP-OFF ANALYSIS
        # =========================
        st.subheader("⚠️ Drop-off Analysis")

        drop = drop_off_analysis(total, counselling, application, enrolled)

        for k, v in drop.items():
            st.write(f"{k}: {v} students dropped")

        # =========================
        # CHANNEL ANALYSIS
        # =========================
        st.subheader("📢 Channel Performance")

        channel_df = channel_analysis(df)
        st.dataframe(channel_df)
        st.bar_chart(channel_df["enrolled"])

        # =========================
        # CITY ANALYSIS
        # =========================
        st.subheader("🌍 City-wise Enrollment")

        city_df = city_analysis(df)
        st.bar_chart(city_df)

        # =========================
        # COUNSELLOR PERFORMANCE
        # =========================
        st.subheader("👨‍💼 Counsellor Performance")

        counsellor_df = counsellor_performance(df)
        st.dataframe(counsellor_df)
        st.bar_chart(counsellor_df["enrolled"])

        # =========================
        # FINAL INSIGHTS
        # =========================
        st.subheader("🔍 Key Insights")

        best_channel = channel_df["enrolled"].idxmax()
        best_city = city_df.idxmax()
        best_counsellor = counsellor_df["enrolled"].idxmax()

        st.success(f"🏆 Best Channel: {best_channel}")
        st.success(f"🏙️ Top City: {best_city}")
        st.success(f"👨‍💼 Best Counsellor: {best_counsellor}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("👈 Please upload all 4 datasets (CSV or Excel) to begin analysis")
