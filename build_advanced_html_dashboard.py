
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = Path(".").resolve()
SYNTHETIC_DIR = BASE_DIR / "data" / "synthetic"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "docs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_HTML = OUTPUT_DIR / "advanced_dashboard.html"

required_files = {
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

missing = [str(path) for path in required_files.values() if not path.exists()]
if missing:
    raise FileNotFoundError(
        "Missing required CSV files:\n" + "\n".join(missing) +
        "\n\nRun this first if needed:\npython pipelines/01_generate_demo_data.py"
    )

metadata = pd.read_csv(required_files["metadata"])
quality = pd.read_csv(required_files["quality"])
ai = pd.read_csv(required_files["ai"])
issues = pd.read_csv(required_files["issues"])
access = pd.read_csv(required_files["access"])
lineage = pd.read_csv(required_files["lineage"])
assets = pd.read_csv(required_files["assets"])
requests = pd.read_csv(required_files["requests"])
districts = pd.read_csv(required_files["districts"])

combined = (
    metadata
    .merge(quality[["dataset_id", "data_quality_score", "failed_checks", "open_critical_issues"]], on="dataset_id", how="left")
    .merge(ai[["dataset_id", "ai_readiness_score", "ai_readiness_category"]], on="dataset_id", how="left")
)

def kpi_card(label, value, subtext=""):
    sub = f'<div class="kpi-sub">{subtext}</div>' if subtext else ""
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub}
    </div>
    """

risk_color_map = {
    "Critical": "#ff5a5f",
    "High": "#ff9f43",
    "Moderate": "#ffd166",
    "Low": "#4cd137",
}

map_sample = assets.sample(min(500, len(assets)), random_state=42).copy()

fig_map = px.scatter_mapbox(
    map_sample,
    lat="latitude",
    lon="longitude",
    color="risk_tier",
    size="risk_index",
    hover_name="asset_id",
    hover_data={
        "asset_type": True,
        "service_district": True,
        "neighbourhood": True,
        "risk_index": ":.1f",
        "service_pressure_score": True,
        "data_quality_risk_score": True,
        "governance_maturity_score": True,
        "latitude": False,
        "longitude": False,
    },
    color_discrete_map=risk_color_map,
    zoom=9.6,
    center={"lat": 43.705, "lon": -79.39},
    height=560,
)
fig_map.update_layout(
    template="plotly_dark",
    margin=dict(l=10, r=10, t=50, b=10),
    title="Operational Risk Map",
    mapbox_style="carto-darkmatter",
    legend_title_text="Risk Tier",
)

fig_3d = px.scatter_3d(
    map_sample.sort_values("risk_index", ascending=False),
    x="longitude",
    y="latitude",
    z="risk_index",
    color="risk_tier",
    size="service_pressure_score",
    hover_name="asset_id",
    hover_data={
        "asset_type": True,
        "service_district": True,
        "neighbourhood": True,
        "risk_index": ":.1f",
        "service_pressure_score": True,
        "data_quality_risk_score": True,
        "governance_maturity_score": True,
    },
    color_discrete_map=risk_color_map,
    height=560,
)
fig_3d.update_layout(
    template="plotly_dark",
    title="3D Digital Twin Risk Landscape",
    margin=dict(l=10, r=10, t=50, b=10),
    scene=dict(
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        zaxis_title="Risk Index",
        bgcolor="#0b1020",
    ),
)

districts_sorted = districts.sort_values("avg_risk_index", ascending=False).copy()
fig_district = px.bar(
    districts_sorted,
    x="service_district",
    y="avg_risk_index",
    color="avg_risk_index",
    text="avg_risk_index",
    hover_data=[
        "assets_monitored", "avg_service_pressure", "avg_data_quality_risk",
        "avg_governance_maturity", "avg_ai_readiness", "critical_assets",
        "open_asset_issues"
    ],
    height=420,
    title="Risk by Service District",
    color_continuous_scale="Turbo",
)
fig_district.update_layout(
    template="plotly_dark",
    margin=dict(l=10, r=10, t=50, b=10),
    showlegend=False,
    coloraxis_showscale=False,
)
fig_district.update_traces(texttemplate="%{text:.1f}", textposition="outside")

ai_counts = ai["ai_readiness_category"].value_counts().reset_index()
ai_counts.columns = ["category", "count"]
fig_ai = px.pie(
    ai_counts,
    names="category",
    values="count",
    hole=0.62,
    title="AI Readiness Portfolio",
    height=420,
    color="category",
    color_discrete_map={
        "Ready": "#00d1b2",
        "Needs Remediation": "#ffb020",
        "Not Ready": "#7c83fd",
        "Restricted": "#ff5a5f",
    }
)
fig_ai.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=50, b=10))

fig_bubble = px.scatter(
    ai,
    x="metadata_completeness_score",
    y="ai_readiness_score",
    size="data_quality_score",
    color="ai_readiness_category",
    hover_name="dataset_name",
    hover_data=["lineage_status", "business_definition_status", "access_risk_level", "data_classification"],
    title="Metadata Completeness vs AI Readiness",
    height=480,
    color_discrete_map={
        "Ready": "#00d1b2",
        "Needs Remediation": "#ffb020",
        "Not Ready": "#7c83fd",
        "Restricted": "#ff5a5f",
    }
)
fig_bubble.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=50, b=10))

score_cols = ["completeness_score", "validity_score", "uniqueness_score", "consistency_score", "timeliness_score"]
matrix = quality.set_index("dataset_name")[score_cols]
fig_heat = px.imshow(
    matrix,
    aspect="auto",
    color_continuous_scale="Viridis",
    title="Data Quality Heatmap",
    height=480,
)
fig_heat.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=50, b=10))

req_summary = requests.groupby(["category", "status"]).size().reset_index(name="requests")
fig_req = px.bar(
    req_summary,
    x="category",
    y="requests",
    color="status",
    barmode="stack",
    title="Service Demand by Category and Status",
    height=430,
)
fig_req.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=50, b=90))

acc_summary = access.groupby(["risk_level", "decision"]).size().reset_index(name="requests")
fig_access = px.bar(
    acc_summary,
    x="risk_level",
    y="requests",
    color="decision",
    barmode="group",
    title="Access Decisions by Risk Level",
    height=430,
)
fig_access.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=50, b=10))

src = lineage["source_dataset"].astype(str)
mid = lineage["dashboard_layer"].astype(str)
end = lineage["reporting_output"].astype(str)
labels = list(pd.Index(src).append(pd.Index(mid)).append(pd.Index(end)).unique())
label_to_idx = {label: i for i, label in enumerate(labels)}

flow_sm = lineage.groupby(["source_dataset", "dashboard_layer"]).size().reset_index(name="value")
flow_me = lineage.groupby(["dashboard_layer", "reporting_output"]).size().reset_index(name="value")

source_idx = flow_sm["source_dataset"].map(label_to_idx).tolist() + flow_me["dashboard_layer"].map(label_to_idx).tolist()
target_idx = flow_sm["dashboard_layer"].map(label_to_idx).tolist() + flow_me["reporting_output"].map(label_to_idx).tolist()
values = flow_sm["value"].tolist() + flow_me["value"].tolist()

fig_sankey = go.Figure(
    data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=18,
            line=dict(color="rgba(255,255,255,0.15)", width=0.5),
            label=labels,
            color="rgba(120,180,255,0.8)",
        ),
        link=dict(
            source=source_idx,
            target=target_idx,
            value=values,
            color="rgba(255,255,255,0.12)",
        )
    )]
)
fig_sankey.update_layout(
    template="plotly_dark",
    title="Lineage Flow: Source → Dashboard Layer → Reporting Output",
    height=520,
    margin=dict(l=10, r=10, t=50, b=10),
)

top_assets = assets.sort_values("risk_index", ascending=False).head(15)[[
    "asset_id", "asset_type", "service_district", "neighbourhood", "risk_tier",
    "risk_index", "service_pressure_score", "data_quality_risk_score",
    "governance_maturity_score", "ai_readiness_score", "open_issue_count", "stale_days"
]].copy()

fig_table = go.Figure(
    data=[go.Table(
        header=dict(
            values=list(top_assets.columns),
            fill_color="#1f2a44",
            line_color="rgba(255,255,255,0.08)",
            align="left",
            font=dict(color="white", size=12)
        ),
        cells=dict(
            values=[top_assets[col] for col in top_assets.columns],
            fill_color="#0f172a",
            line_color="rgba(255,255,255,0.06)",
            align="left",
            font=dict(color="white", size=11),
            height=28
        )
    )]
)
fig_table.update_layout(template="plotly_dark", title="Highest-Risk Assets", height=500, margin=dict(l=10, r=10, t=50, b=10))

include_once = "cdn"
html_map = fig_map.to_html(full_html=False, include_plotlyjs=include_once)
html_3d = fig_3d.to_html(full_html=False, include_plotlyjs=False)
html_district = fig_district.to_html(full_html=False, include_plotlyjs=False)
html_ai = fig_ai.to_html(full_html=False, include_plotlyjs=False)
html_bubble = fig_bubble.to_html(full_html=False, include_plotlyjs=False)
html_heat = fig_heat.to_html(full_html=False, include_plotlyjs=False)
html_req = fig_req.to_html(full_html=False, include_plotlyjs=False)
html_access = fig_access.to_html(full_html=False, include_plotlyjs=False)
html_sankey = fig_sankey.to_html(full_html=False, include_plotlyjs=False)
html_table = fig_table.to_html(full_html=False, include_plotlyjs=False)

datasets_governed = len(metadata)
assets_monitored = len(assets)
service_requests = len(requests)
avg_dq = combined["data_quality_score"].mean()
avg_ai = combined["ai_readiness_score"].mean()
open_issues = int((issues["status"] != "Resolved").sum())
critical_assets = int((assets["risk_tier"] == "Critical").sum())
high_risk_datasets = int((ai["ai_readiness_category"].isin(["Restricted", "Not Ready"])).sum())

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Urban Data Governance Digital Twin | Advanced HTML Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #060b16;
  --panel: #0f172a;
  --text: #edf2ff;
  --muted: #93a4c7;
  --border: rgba(255,255,255,0.08);
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: "Inter", system-ui, sans-serif;
  background:
    radial-gradient(circle at top left, rgba(124,131,253,0.20), transparent 22%),
    radial-gradient(circle at top right, rgba(0,209,178,0.10), transparent 18%),
    linear-gradient(180deg, #04070f 0%, #08101f 100%);
  color: var(--text);
}}
.container {{
  max-width: 1600px;
  margin: 0 auto;
  padding: 28px 22px 40px;
}}
.hero {{
  background:
    linear-gradient(135deg, rgba(18,28,54,0.96), rgba(6,11,22,0.98));
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 25px 70px rgba(0,0,0,0.32);
  margin-bottom: 20px;
}}
.eyebrow {{
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(124,131,253,0.14);
  color: #cfd4ff;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}}
h1 {{
  margin: 14px 0 8px;
  font-size: clamp(32px, 4vw, 58px);
  letter-spacing: -0.04em;
  line-height: 1.02;
}}
.hero p {{
  max-width: 1100px;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.7;
}}
.badges {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
}}
.badge {{
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border);
  padding: 8px 12px;
  border-radius: 999px;
  color: #dbe6ff;
  font-size: 13px;
}}
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(8, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}}
.kpi-card {{
  background: linear-gradient(180deg, rgba(17,28,54,0.92), rgba(9,16,33,0.96));
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px 16px;
  min-height: 116px;
}}
.kpi-label {{
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 12px;
  font-weight: 700;
}}
.kpi-value {{
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.03em;
}}
.kpi-sub {{
  color: #bcd0ff;
  font-size: 12px;
  margin-top: 8px;
}}
.section {{ margin-top: 18px; }}
.section-title {{
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.03em;
}}
.section-sub {{
  margin-top: 4px;
  margin-bottom: 10px;
  color: var(--muted);
}}
.grid-2 {{
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 16px;
}}
.grid-2-even {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}}
.card {{
  background: linear-gradient(180deg, rgba(14,22,42,0.98), rgba(9,14,28,0.98));
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 10px;
  overflow: hidden;
}}
.note {{
  margin-top: 10px;
  padding: 14px 16px;
  border-left: 4px solid #00d1b2;
  background: rgba(255,255,255,0.03);
  border-radius: 12px;
  color: #d9e6ff;
  line-height: 1.6;
}}
.footer {{
  margin-top: 22px;
  padding-top: 18px;
  color: var(--muted);
  font-size: 13px;
  border-top: 1px solid var(--border);
}}
@media (max-width: 1280px) {{
  .kpi-grid {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
  .grid-2, .grid-2-even {{ grid-template-columns: 1fr; }}
}}
@media (max-width: 760px) {{
  .kpi-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
}}
</style>
</head>
<body>
<div class="container">
  <div class="hero">
    <div class="eyebrow">Enterprise Municipal Intelligence Dashboard</div>
    <h1>Urban Data Governance Digital Twin</h1>
    <p>
      An interactive municipal intelligence dashboard for operational oversight, governance controls, and executive decision support.
      It combines municipal service analytics, operational risk, data quality controls, metadata completeness,
      access governance, lineage visibility, and AI-readiness into one decision-support environment.
    </p>
    <div class="badges">
      <div class="badge">3D Visualization</div>
      <div class="badge">Interactive Analytics</div>
      <div class="badge">Operational Risk</div>
      <div class="badge">Data Quality</div>
      <div class="badge">Metadata + Lineage</div>
      <div class="badge">AI Readiness</div>
      <div class="badge">Public Sector Analytics</div>
      <div class="badge">Executive Dashboard</div>
    </div>
  </div>

  <div class="kpi-grid">
    {kpi_card("Datasets Governed", f"{datasets_governed:,}", "Governed datasets across metadata, quality, access, lineage, and AI scoring")}
    {kpi_card("Assets Monitored", f"{assets_monitored:,}", "Municipal asset risk layer")}
    {kpi_card("Service Requests", f"{service_requests:,}", "Service-demand signals")}
    {kpi_card("Average Data Quality", f"{avg_dq:.1f}%", "Cross-dataset quality score")}
    {kpi_card("Average AI Readiness", f"{avg_ai:.1f}%", "Dataset readiness average")}
    {kpi_card("Open Governance Issues", f"{open_issues:,}", "All non-resolved issues")}
    {kpi_card("Critical Assets", f"{critical_assets:,}", "Highest operational risk tier")}
    {kpi_card("High-Risk Datasets", f"{high_risk_datasets:,}", "Restricted or not-ready datasets")}
  </div>

  <div class="section">
    <div class="section-title">Spatial Operations Control Centre</div>
    <div class="section-sub">Interactive map view and 3D risk landscape for operational risk monitoring.</div>
    <div class="grid-2">
      <div class="card">{html_map}</div>
      <div class="card">{html_3d}</div>
    </div>
    <div class="note">
      The left view shows geospatial operational exposure across the city. The right view converts the same asset layer into a
      3D risk landscape, where elevation reflects risk intensity and point size reflects service pressure.
    </div>
  </div>

  <div class="section">
    <div class="section-title">Executive Governance and Operations Layer</div>
    <div class="section-sub">District-level risk, AI-readiness status, and dataset-level governance performance.</div>
    <div class="grid-2-even">
      <div class="card">{html_district}</div>
      <div class="card">{html_ai}</div>
    </div>
    <div class="grid-2-even" style="margin-top:16px;">
      <div class="card">{html_bubble}</div>
      <div class="card">{html_heat}</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Operational Demand and Governance Controls</div>
    <div class="section-sub">Service demand patterns, access approvals, risk gating, and approval behaviour.</div>
    <div class="grid-2-even">
      <div class="card">{html_req}</div>
      <div class="card">{html_access}</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Lineage and Priority Action View</div>
    <div class="section-sub">Trace how data flows into reporting outputs and identify the highest-priority operational records.</div>
    <div class="grid-2">
      <div class="card">{html_sankey}</div>
      <div class="card">{html_table}</div>
    </div>
  </div>

  <div class="footer">
    Built from governed municipal demonstration layers, data quality controls, access-risk logic, lineage mapping, and AI-readiness scoring.
  </div>
</div>
</body>
</html>
"""

OUTPUT_HTML.write_text(html, encoding="utf-8")

print(f"Created: {OUTPUT_HTML}")
print("Run this locally from your repo root with:")
print("python build_advanced_html_dashboard.py")
print("Then open: docs/advanced_dashboard.html")
