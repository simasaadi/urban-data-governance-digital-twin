import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SYNTHETIC_DIR = BASE_DIR / "data" / "synthetic"

st.set_page_config(
    page_title="Urban Data Governance Digital Twin",
    page_icon="🏙️",
    layout="wide"
)

st.title("Urban Data Governance Digital Twin")
st.caption(
    "3D municipal analytics, data quality controls, metadata scoring, access governance, and AI-readiness indicators."
)

metadata_path = SYNTHETIC_DIR / "metadata_catalog.csv"
quality_path = SYNTHETIC_DIR / "data_quality_results.csv"
ai_path = SYNTHETIC_DIR / "ai_readiness_scores.csv"
issues_path = SYNTHETIC_DIR / "data_issue_log.csv"
access_path = SYNTHETIC_DIR / "access_decision_log.csv"

if not metadata_path.exists():
    st.warning("Synthetic data has not been generated yet. Run: python pipelines/01_generate_synthetic_governance_data.py")
    st.stop()

metadata = pd.read_csv(metadata_path)
quality = pd.read_csv(quality_path)
ai = pd.read_csv(ai_path)
issues = pd.read_csv(issues_path)
access = pd.read_csv(access_path)

combined = (
    metadata
    .merge(quality[["dataset_id", "data_quality_score", "failed_checks", "open_critical_issues"]], on="dataset_id", how="left")
    .merge(ai[["dataset_id", "ai_readiness_score", "ai_readiness_category"]], on="dataset_id", how="left")
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Datasets Monitored", len(metadata))
kpi2.metric("Average Data Quality", f"{combined['data_quality_score'].mean():.1f}%")
kpi3.metric("Average AI Readiness", f"{combined['ai_readiness_score'].mean():.1f}%")
kpi4.metric("Open Data Issues", int((issues["status"] != "Resolved").sum()))

st.divider()

left, right = st.columns([1.3, 1])

with left:
    st.subheader("Governance and AI-Readiness Scorecard")
    fig = px.scatter(
        combined,
        x="metadata_completeness_score",
        y="data_quality_score",
        size="ai_readiness_score",
        color="ai_readiness_category",
        hover_name="dataset_name",
        hover_data=[
            "data_owner",
            "data_steward",
            "business_function",
            "data_classification",
            "access_risk_level",
            "lineage_status"
        ],
        labels={
            "metadata_completeness_score": "Metadata Completeness Score",
            "data_quality_score": "Data Quality Score",
            "ai_readiness_category": "AI Readiness"
        },
        title="Data Quality vs Metadata Completeness"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("AI-Readiness Categories")
    readiness_counts = ai["ai_readiness_category"].value_counts().reset_index()
    readiness_counts.columns = ["category", "count"]
    fig2 = px.bar(
        readiness_counts,
        x="category",
        y="count",
        title="Dataset AI-Readiness Status",
        text="count"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "Metadata Catalog",
    "Data Quality Results",
    "Access Decisions",
    "Issue Log"
])

with tab1:
    st.dataframe(metadata, use_container_width=True)

with tab2:
    st.dataframe(quality, use_container_width=True)

with tab3:
    st.dataframe(access, use_container_width=True)

with tab4:
    st.dataframe(issues, use_container_width=True)

st.divider()

st.subheader("Interpretation")
st.write(
    """
    This dashboard demonstrates how municipal open data can be governed as an operational intelligence product.
    The current version uses synthetic governance records to show metadata completeness, data quality results,
    access-risk decisions, lineage status, and AI-readiness indicators. Future versions will connect these controls
    to Toronto Open Data geospatial layers such as 3D Massing, Neighbourhoods, Wards, Solid Waste Districts,
    Litter Bin Collection Frequency, In-Park Assets, and 311 Service Requests.
    """
)
