from pathlib import Path

import pandas as pd
import plotly.express as px
import pydeck as pdk
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
SYNTHETIC_DIR = BASE_DIR / "data" / "synthetic"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

st.set_page_config(
    page_title="Urban Data Governance Digital Twin",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.7rem 1.8rem;
        border-radius: 1.4rem;
        background:
            radial-gradient(circle at top left, rgba(255, 75, 75, 0.28), transparent 32%),
            linear-gradient(135deg, rgba(31, 41, 55, 0.95), rgba(8, 13, 23, 0.98));
        border: 1px solid rgba(255,255,255,0.11);
        box-shadow: 0 20px 60px rgba(0,0,0,0.28);
        margin-bottom: 1.2rem;
    }

    .hero h1 {
        font-size: 3.2rem;
        line-height: 1.02;
        letter-spacing: -0.05em;
        margin-bottom: 0.55rem;
    }

    .hero p {
        color: rgba(255,255,255,0.76);
        font-size: 1.02rem;
        max-width: 1180px;
    }

    .badge-row {
        margin-top: 0.9rem;
    }

    .badge {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
        color: rgba(255,255,255,0.86);
        font-size: 0.78rem;
    }

    div[data-testid="stMetric"] {
        padding: 1rem 1rem;
        border-radius: 1rem;
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.09);
    }

    .insight-box {
        padding: 1rem 1.1rem;
        border-radius: 1rem;
        background: rgba(255,255,255,0.045);
        border-left: 4px solid #ff4b4b;
        color: rgba(255,255,255,0.88);
        margin-top: 0.7rem;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .section-caption {
        color: rgba(255,255,255,0.62);
        margin-bottom: 0.7rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    required = {
        "metadata": SYNTHETIC_DIR / "metadata_catalog.csv",
        "quality": SYNTHETIC_DIR / "data_quality_results.csv",
        "ai": SYNTHETIC_DIR / "ai_readiness_scores.csv",
        "issues": SYNTHETIC_DIR / "data_issue_log.csv",
        "access": SYNTHETIC_DIR / "access_decision_log.csv",
        "lineage": SYNTHETIC_DIR / "lineage_map.csv",
        "assets": PROCESSED_DIR / "municipal_asset_risk_layer.csv",
        "requests": PROCESSED_DIR / "service_request_demand_layer.csv",
        "districts": PROCESSED_DIR / "district_governance_summary.csv",
    }

    missing = [str(path) for path in required.values() if not path.exists()]
    if missing:
        st.error("Advanced demo data is missing. Run this command first:")
        st.code("python pipelines/01_generate_demo_data.py")
        st.stop()

    return {name: pd.read_csv(path) for name, path in required.items()}


data = load_data()

metadata = data["metadata"]
quality = data["quality"]
ai = data["ai"]
issues = data["issues"]
access = data["access"]
lineage = data["lineage"]
assets = data["assets"]
requests = data["requests"]
districts = data["districts"]

combined = (
    metadata
    .merge(
        quality[["dataset_id", "data_quality_score", "failed_checks", "open_critical_issues"]],
        on="dataset_id",
        how="left",
    )
    .merge(
        ai[["dataset_id", "ai_readiness_score", "ai_readiness_category"]],
        on="dataset_id",
        how="left",
    )
)

st.sidebar.title("Digital Twin Controls")
st.sidebar.caption("Filter the 3D operational and governance layers.")

district_filter = st.sidebar.multiselect(
    "Service district",
    sorted(assets["service_district"].unique()),
    default=sorted(assets["service_district"].unique()),
)

risk_filter = st.sidebar.multiselect(
    "Risk tier",
    ["Critical", "High", "Moderate", "Low"],
    default=["Critical", "High", "Moderate", "Low"],
)

elevation_choice = st.sidebar.radio(
    "3D column height",
    [
        "Operational Risk",
        "Service Pressure",
        "Data Quality Risk",
        "Governance Maturity",
        "AI Readiness",
    ],
)

minimum_risk = st.sidebar.slider("Minimum risk index", 0, 100, 20)

metric_map = {
    "Operational Risk": ("risk_index", "Operational risk index"),
    "Service Pressure": ("service_pressure_score", "Service pressure score"),
    "Data Quality Risk": ("data_quality_risk_score", "Data quality risk score"),
    "Governance Maturity": ("governance_maturity_score", "Governance maturity score"),
    "AI Readiness": ("ai_readiness_score", "AI-readiness score"),
}

metric_col, metric_label = metric_map[elevation_choice]

filtered_assets = assets[
    assets["service_district"].isin(district_filter)
    & assets["risk_tier"].isin(risk_filter)
    & (assets["risk_index"] >= minimum_risk)
].copy()

filtered_assets["map_elevation"] = filtered_assets[metric_col] * 13

st.markdown(
    """
    <div class="hero">
        <h1>Urban Data Governance Digital Twin</h1>
        <p>
        A 3D interactive municipal operations dashboard showing service performance,
        data quality risk, metadata completeness, access governance, lineage, and AI-readiness.
        Designed as a senior-level data governance and analytics engineering portfolio product.
        </p>
        <div class="badge-row">
            <span class="badge">3D GIS</span>
            <span class="badge">Data Governance</span>
            <span class="badge">Data Quality Controls</span>
            <span class="badge">Access Risk</span>
            <span class="badge">Metadata + Lineage</span>
            <span class="badge">AI Readiness</span>
            <span class="badge">Executive KPIs</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Datasets Governed", f"{len(metadata):,}")
k2.metric("Assets Monitored", f"{len(assets):,}")
k3.metric("Service Requests", f"{len(requests):,}")
k4.metric("Avg Data Quality", f"{combined['data_quality_score'].mean():.1f}%")
k5.metric("Avg AI Readiness", f"{combined['ai_readiness_score'].mean():.1f}%")
k6.metric("Open Issues", f"{int((issues['status'] != 'Resolved').sum()):,}")

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Executive Control Panel",
        "3D Digital Twin",
        "Service Performance",
        "Data Quality Risk",
        "Access + Privacy",
        "Metadata, Lineage + AI",
    ]
)

with tab1:
    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.markdown('<div class="section-title">Operational Risk by Service District</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">Risk combines service pressure, stale records, data-quality exposure, access risk, and governance maturity.</div>', unsafe_allow_html=True)

        fig = px.bar(
            districts.sort_values("avg_risk_index", ascending=False),
            x="service_district",
            y="avg_risk_index",
            text="avg_risk_index",
            hover_data=[
                "assets_monitored",
                "avg_service_pressure",
                "avg_data_quality_risk",
                "avg_governance_maturity",
                "avg_ai_readiness",
                "critical_assets",
                "open_asset_issues",
            ],
            template="plotly_dark",
            labels={"service_district": "District", "avg_risk_index": "Average risk index"},
        )
        fig.update_layout(height=430, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-title">AI-Readiness Portfolio</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">Datasets are scored based on quality, metadata, lineage, definitions, classification, and access risk.</div>', unsafe_allow_html=True)

        readiness = ai["ai_readiness_category"].value_counts().reset_index()
        readiness.columns = ["category", "count"]

        fig = px.pie(
            readiness,
            names="category",
            values="count",
            hole=0.56,
            template="plotly_dark",
        )
        fig.update_layout(height=430, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Priority Operational + Governance Queue</div>', unsafe_allow_html=True)
    priority = assets.sort_values("risk_index", ascending=False).head(18)[
        [
            "asset_id",
            "asset_type",
            "service_district",
            "neighbourhood",
            "risk_tier",
            "risk_index",
            "service_pressure_score",
            "data_quality_risk_score",
            "governance_maturity_score",
            "ai_readiness_score",
            "open_issue_count",
            "stale_days",
        ]
    ]
    st.dataframe(priority, use_container_width=True, hide_index=True)

    st.markdown(
        """
        <div class="insight-box">
        <b>Executive interpretation:</b> this dashboard does not only show where service pressure is high.
        It shows whether the data behind those operational decisions is trusted, documented, governed,
        access-controlled, and ready for advanced analytics or AI.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab2:
    st.markdown('<div class="section-title">3D Municipal Operations and Governance Control Map</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-caption">Column height currently represents: <b>{metric_label}</b>. Colours represent operational risk tier.</div>',
        unsafe_allow_html=True,
    )

    map_left, map_right = st.columns([1.75, 0.85])

    with map_left:
        if filtered_assets.empty:
            st.warning("No assets match the current filters.")
        else:
            column_layer = pdk.Layer(
                "ColumnLayer",
                data=filtered_assets,
                get_position="[longitude, latitude]",
                get_elevation="map_elevation",
                elevation_scale=1,
                radius=85,
                get_fill_color="[color_r, color_g, color_b, color_a]",
                pickable=True,
                auto_highlight=True,
            )

            request_sample = requests.sample(min(450, len(requests)), random_state=42)

            request_layer = pdk.Layer(
                "ScatterplotLayer",
                data=request_sample,
                get_position="[longitude, latitude]",
                get_radius=35,
                get_fill_color=[80, 180, 255, 90],
                pickable=True,
            )

            view_state = pdk.ViewState(
                latitude=43.705,
                longitude=-79.39,
                zoom=10.2,
                pitch=55,
                bearing=-18,
            )

            deck = pdk.Deck(
                layers=[request_layer, column_layer],
                initial_view_state=view_state,
                map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
                tooltip={
                    "html": """
                    <b>{asset_id}</b><br/>
                    Type: {asset_type}<br/>
                    District: {service_district}<br/>
                    Neighbourhood: {neighbourhood}<br/>
                    Risk tier: {risk_tier}<br/>
                    Risk index: {risk_index}<br/>
                    Service pressure: {service_pressure_score}<br/>
                    Data quality risk: {data_quality_risk_score}<br/>
                    Governance maturity: {governance_maturity_score}<br/>
                    AI readiness: {ai_readiness_score}
                    """,
                    "style": {"backgroundColor": "#111827", "color": "white"},
                },
            )

            st.pydeck_chart(deck, use_container_width=True)

    with map_right:
        st.metric("Filtered assets", f"{len(filtered_assets):,}")
        st.metric("Critical assets", f"{int((filtered_assets['risk_tier'] == 'Critical').sum()):,}")
        st.metric("Average risk", f"{filtered_assets['risk_index'].mean():.1f}")
        st.metric("Average stale days", f"{filtered_assets['stale_days'].mean():.1f}")
        st.metric("Open asset issues", f"{int(filtered_assets['open_issue_count'].sum()):,}")

        st.markdown(
            """
            <div class="insight-box">
            Blue dots represent synthetic 311-style service demand.
            3D columns represent governed operational assets.
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab3:
    st.markdown('<div class="section-title">Service Performance and Demand Signals</div>', unsafe_allow_html=True)

    s1, s2 = st.columns(2)

    with s1:
        req_summary = requests.groupby(["category", "status"]).size().reset_index(name="requests")
        fig = px.bar(
            req_summary,
            x="category",
            y="requests",
            color="status",
            barmode="stack",
            template="plotly_dark",
            title="Service Requests by Category and Status",
        )
        fig.update_layout(height=470, margin=dict(l=10, r=10, t=45, b=130))
        st.plotly_chart(fig, use_container_width=True)

    with s2:
        district_demand = requests.groupby(["service_district", "priority"]).size().reset_index(name="requests")
        fig = px.bar(
            district_demand,
            x="service_district",
            y="requests",
            color="priority",
            barmode="group",
            template="plotly_dark",
            title="Demand by District and Priority",
        )
        fig.update_layout(height=470, margin=dict(l=10, r=10, t=45, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        requests.sort_values(["status", "priority", "days_open"], ascending=[True, True, False]).head(100),
        use_container_width=True,
        hide_index=True,
    )

with tab4:
    st.markdown('<div class="section-title">Data Quality Risk Layer</div>', unsafe_allow_html=True)

    q1, q2 = st.columns([1.1, 1])

    with q1:
        score_cols = [
            "completeness_score",
            "validity_score",
            "uniqueness_score",
            "consistency_score",
            "timeliness_score",
        ]
        matrix = quality.set_index("dataset_name")[score_cols]
        fig = px.imshow(
            matrix,
            aspect="auto",
            template="plotly_dark",
            labels=dict(x="Quality Dimension", y="Dataset", color="Score"),
            title="Data Quality Dimension Heatmap",
        )
        fig.update_layout(height=540, margin=dict(l=10, r=10, t=45, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with q2:
        issue_summary = issues.groupby(["severity", "status"]).size().reset_index(name="issues")
        fig = px.bar(
            issue_summary,
            x="severity",
            y="issues",
            color="status",
            barmode="group",
            template="plotly_dark",
            title="Issue Status by Severity",
        )
        fig.update_layout(height=540, margin=dict(l=10, r=10, t=45, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(issues.sort_values(["status", "severity", "created_date"]), use_container_width=True, hide_index=True)

with tab5:
    st.markdown('<div class="section-title">Access Governance and Privacy Risk</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)

    with a1:
        access_matrix = access.groupby(["risk_level", "decision"]).size().reset_index(name="requests")
        fig = px.bar(
            access_matrix,
            x="risk_level",
            y="requests",
            color="decision",
            barmode="group",
            template="plotly_dark",
            title="Access Decisions by Risk Level",
        )
        fig.update_layout(height=470, margin=dict(l=10, r=10, t=45, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with a2:
        minimum = access.groupby(["sensitive_data_involved", "minimum_necessary_checked"]).size().reset_index(name="requests")
        fig = px.bar(
            minimum,
            x="sensitive_data_involved",
            y="requests",
            color="minimum_necessary_checked",
            barmode="group",
            template="plotly_dark",
            title="Minimum Necessary Review",
        )
        fig.update_layout(height=470, margin=dict(l=10, r=10, t=45, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(access, use_container_width=True, hide_index=True)

with tab6:
    st.markdown('<div class="section-title">Metadata, Lineage, and AI-Readiness Layer</div>', unsafe_allow_html=True)

    l1, l2 = st.columns([1.15, 1])

    with l1:
        fig = px.scatter(
            ai,
            x="metadata_completeness_score",
            y="ai_readiness_score",
            size="data_quality_score",
            color="ai_readiness_category",
            hover_name="dataset_name",
            hover_data=[
                "lineage_status",
                "business_definition_status",
                "access_risk_level",
                "data_classification",
            ],
            template="plotly_dark",
            title="AI Readiness by Metadata Completeness",
            labels={
                "metadata_completeness_score": "Metadata completeness",
                "ai_readiness_score": "AI-readiness score",
            },
        )
        fig.update_layout(height=480, margin=dict(l=10, r=10, t=45, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with l2:
        lineage_counts = lineage.groupby(["dashboard_layer", "lineage_status"]).size().reset_index(name="datasets")
        fig = px.bar(
            lineage_counts,
            x="dashboard_layer",
            y="datasets",
            color="lineage_status",
            template="plotly_dark",
            title="Lineage Coverage by Dashboard Layer",
        )
        fig.update_layout(height=480, margin=dict(l=10, r=10, t=45, b=120))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Metadata Catalog")
    st.dataframe(metadata.sort_values("metadata_completeness_score", ascending=False), use_container_width=True, hide_index=True)

    st.subheader("Lineage Map")
    st.dataframe(lineage, use_container_width=True, hide_index=True)

st.divider()

st.caption(
    "Portfolio note: this dashboard uses public-data architecture and synthetic governance records only. "
    "It is not an official City of Toronto system and does not use confidential project data."
)
