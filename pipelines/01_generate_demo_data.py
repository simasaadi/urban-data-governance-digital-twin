from pathlib import Path
from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
SYNTHETIC_DIR = BASE_DIR / "data" / "synthetic"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)
np.random.seed(42)

today = datetime.today().date()

datasets = [
    ("DS-001", "Toronto 3D Massing", "Toronto Open Data", "3D Urban Context", "Open Data Team", "Public", "Low"),
    ("DS-002", "Neighbourhoods", "Toronto Open Data", "Geographic Reporting", "Open Data Team", "Public", "Low"),
    ("DS-003", "City Wards and Ward Profiles", "Toronto Open Data", "Council Reporting", "Open Data Team", "Public", "Low"),
    ("DS-004", "Toronto Centreline", "Toronto Open Data", "Transportation Context", "Transportation Data Team", "Public", "Low"),
    ("DS-005", "Solid Waste Management Districts", "Toronto Open Data", "Solid Waste Operations", "Operations", "Public", "Low"),
    ("DS-006", "Solid Waste In-Park Assets", "Toronto Open Data", "Asset Management", "Operations", "Public", "Low"),
    ("DS-007", "Litter Bin Collection Frequency", "Toronto Open Data", "Collection Operations", "Operations", "Public", "Low"),
    ("DS-008", "311 Service Requests", "Toronto Open Data", "Service Demand Monitoring", "Customer Experience", "Public Aggregated", "Medium"),
    ("DS-009", "Road Restrictions", "Toronto Open Data", "Disruption Monitoring", "Transportation Services", "Public", "Low"),
    ("DS-010", "Metadata Catalog", "Synthetic Governance Layer", "Data Governance Controls", "Data Governance Office", "Internal", "Medium"),
    ("DS-011", "Access Decision Log", "Synthetic Governance Layer", "Access Governance", "Data Governance Office", "Internal", "High"),
    ("DS-012", "AI Readiness Scores", "Synthetic Governance Layer", "AI Governance", "Analytics", "Internal", "Medium"),
]

metadata_rows = []
for dataset_id, name, source, function, owner, classification, access_risk in datasets:
    metadata_score = random.randint(72, 98) if source == "Toronto Open Data" else random.randint(65, 94)
    lineage_status = random.choice(["Documented", "Documented", "Partially Documented"])
    definition_status = random.choice(["Complete", "Complete", "Partial"])

    metadata_rows.append({
        "dataset_id": dataset_id,
        "dataset_name": name,
        "source_type": source,
        "business_function": function,
        "data_owner": owner,
        "data_steward": random.choice(["Assigned", "Assigned", "Assigned", "Unassigned"]),
        "refresh_frequency": random.choice(["Daily", "Weekly", "Monthly", "Periodic", "Ad hoc"]),
        "data_classification": classification,
        "access_risk_level": access_risk,
        "lineage_status": lineage_status,
        "business_definition_status": definition_status,
        "metadata_completeness_score": metadata_score,
        "last_reviewed_date": today - timedelta(days=random.randint(5, 220)),
    })

metadata = pd.DataFrame(metadata_rows)
metadata.to_csv(SYNTHETIC_DIR / "metadata_catalog.csv", index=False)

quality_rows = []
for _, row in metadata.iterrows():
    completeness = random.randint(70, 99)
    validity = random.randint(68, 99)
    uniqueness = random.randint(75, 99)
    consistency = random.randint(65, 98)
    timeliness = random.randint(60, 96)
    dq_score = round((completeness + validity + uniqueness + consistency + timeliness) / 5, 1)

    quality_rows.append({
        "dataset_id": row["dataset_id"],
        "dataset_name": row["dataset_name"],
        "completeness_score": completeness,
        "validity_score": validity,
        "uniqueness_score": uniqueness,
        "consistency_score": consistency,
        "timeliness_score": timeliness,
        "data_quality_score": dq_score,
        "failed_checks": max(0, int((100 - dq_score) / 7) + random.randint(0, 3)),
        "open_critical_issues": random.choice([0, 0, 1, 1, 2]) if dq_score < 80 else random.choice([0, 0, 0, 1]),
        "last_quality_check_date": today,
    })

quality = pd.DataFrame(quality_rows)
quality.to_csv(SYNTHETIC_DIR / "data_quality_results.csv", index=False)

ai_rows = []
for _, row in metadata.iterrows():
    dq = float(quality.loc[quality["dataset_id"] == row["dataset_id"], "data_quality_score"].iloc[0])
    lineage_score = 100 if row["lineage_status"] == "Documented" else 65
    definition_score = 100 if row["business_definition_status"] == "Complete" else 65
    access_penalty = {"Low": 0, "Medium": 8, "High": 20}[row["access_risk_level"]]

    ai_score = round(
        dq * 0.35
        + row["metadata_completeness_score"] * 0.25
        + lineage_score * 0.20
        + definition_score * 0.20
        - access_penalty,
        1,
    )
    ai_score = max(0, min(100, ai_score))

    if row["access_risk_level"] == "High":
        category = "Restricted"
    elif ai_score >= 80:
        category = "Ready"
    elif ai_score >= 60:
        category = "Needs Remediation"
    else:
        category = "Not Ready"

    ai_rows.append({
        "dataset_id": row["dataset_id"],
        "dataset_name": row["dataset_name"],
        "data_quality_score": dq,
        "metadata_completeness_score": row["metadata_completeness_score"],
        "lineage_status": row["lineage_status"],
        "business_definition_status": row["business_definition_status"],
        "access_risk_level": row["access_risk_level"],
        "data_classification": row["data_classification"],
        "ai_readiness_score": ai_score,
        "ai_readiness_category": category,
    })

ai = pd.DataFrame(ai_rows)
ai.to_csv(SYNTHETIC_DIR / "ai_readiness_scores.csv", index=False)

neighbourhoods = [
    "Waterfront Communities", "Downtown Yonge East", "Annex", "Kensington Chinatown",
    "High Park North", "Danforth East York", "Scarborough Village", "Agincourt South",
    "North York Centre", "Etobicoke Centre", "York University Heights", "Flemingdon Park",
]

districts = ["West District", "North District", "East District", "South District"]
asset_types = ["Litter Bin", "Recycling Bin", "Park Waste Bin", "Public Realm Asset", "Container"]

asset_rows = []
for i in range(1, 801):
    service_pressure = int(np.clip(np.random.normal(62, 21), 5, 100))
    data_quality_risk = int(np.clip(np.random.normal(38, 22), 0, 100))
    governance_maturity = int(np.clip(np.random.normal(74, 17), 10, 100))
    access_risk = random.choice(["Low", "Low", "Medium", "Medium", "High"])
    stale_days = int(np.clip(np.random.normal(45, 38), 0, 240))
    open_issues = random.choice([0, 0, 0, 1, 1, 2, 3])

    risk_index = round(
        service_pressure * 0.35
        + data_quality_risk * 0.30
        + (100 - governance_maturity) * 0.20
        + (18 if access_risk == "High" else 8 if access_risk == "Medium" else 0)
        + min(stale_days / 8, 14)
        + open_issues * 2,
        1,
    )
    risk_index = max(0, min(100, risk_index))

    if risk_index >= 75:
        tier = "Critical"
        color = (214, 39, 40, 210)
    elif risk_index >= 55:
        tier = "High"
        color = (255, 127, 14, 190)
    elif risk_index >= 35:
        tier = "Moderate"
        color = (255, 193, 7, 170)
    else:
        tier = "Low"
        color = (44, 160, 44, 160)

    ai_ready = int(np.clip((100 - data_quality_risk) * 0.35 + governance_maturity * 0.45 + random.randint(-8, 12), 0, 100))

    asset_rows.append({
        "asset_id": f"ASSET-{i:05d}",
        "asset_type": random.choice(asset_types),
        "latitude": round(np.random.uniform(43.59, 43.82), 6),
        "longitude": round(np.random.uniform(-79.62, -79.16), 6),
        "neighbourhood": random.choice(neighbourhoods),
        "ward": f"Ward {random.randint(1, 25)}",
        "service_district": random.choice(districts),
        "service_frequency": random.choice(["Daily", "3x weekly", "2x weekly", "Weekly", "On demand"]),
        "service_pressure_score": service_pressure,
        "data_quality_risk_score": data_quality_risk,
        "governance_maturity_score": governance_maturity,
        "access_risk_level": access_risk,
        "ai_readiness_score": ai_ready,
        "stale_days": stale_days,
        "open_issue_count": open_issues,
        "risk_index": risk_index,
        "risk_tier": tier,
        "color_r": color[0],
        "color_g": color[1],
        "color_b": color[2],
        "color_a": color[3],
        "last_updated": today - timedelta(days=stale_days),
    })

assets = pd.DataFrame(asset_rows)
assets.to_csv(PROCESSED_DIR / "municipal_asset_risk_layer.csv", index=False)

request_rows = []
categories = ["Missed Collection", "Overflowing Litter Bin", "Illegal Dumping", "Damaged Bin", "Public Realm Cleanliness"]
for i in range(1, 1401):
    status = random.choice(["Open", "Open", "In Progress", "Closed", "Closed", "Closed"])
    request_rows.append({
        "request_id": f"SR-{i:06d}",
        "category": random.choice(categories),
        "status": status,
        "priority": random.choice(["Low", "Medium", "High", "Urgent"]),
        "latitude": round(np.random.uniform(43.59, 43.82), 6),
        "longitude": round(np.random.uniform(-79.62, -79.16), 6),
        "neighbourhood": random.choice(neighbourhoods),
        "ward": f"Ward {random.randint(1, 25)}",
        "service_district": random.choice(districts),
        "created_date": today - timedelta(days=random.randint(0, 180)),
        "days_open": 0 if status == "Closed" else random.randint(1, 45),
    })

requests = pd.DataFrame(request_rows)
requests.to_csv(PROCESSED_DIR / "service_request_demand_layer.csv", index=False)

district_summary = (
    assets.groupby("service_district")
    .agg(
        assets_monitored=("asset_id", "count"),
        avg_risk_index=("risk_index", "mean"),
        avg_service_pressure=("service_pressure_score", "mean"),
        avg_data_quality_risk=("data_quality_risk_score", "mean"),
        avg_governance_maturity=("governance_maturity_score", "mean"),
        avg_ai_readiness=("ai_readiness_score", "mean"),
        critical_assets=("risk_tier", lambda s: int((s == "Critical").sum())),
        open_asset_issues=("open_issue_count", "sum"),
    )
    .reset_index()
)

for col in district_summary.columns:
    if col.startswith("avg_"):
        district_summary[col] = district_summary[col].round(1)

district_summary.to_csv(PROCESSED_DIR / "district_governance_summary.csv", index=False)

issue_rows = []
for i in range(1, 56):
    dataset = metadata.sample(1, random_state=100 + i).iloc[0]
    issue_rows.append({
        "issue_id": f"DQI-{i:03d}",
        "dataset_id": dataset["dataset_id"],
        "dataset_name": dataset["dataset_name"],
        "issue_title": random.choice([
            "Missing owner assignment", "Unclear business definition", "Duplicate record",
            "Stale source extract", "Manual transformation risk", "Incomplete lineage",
            "Access approval gap", "Invalid coordinate value",
        ]),
        "severity": random.choice(["Low", "Medium", "High", "Critical"]),
        "status": random.choice(["Open", "In Review", "Resolved", "Deferred"]),
        "assigned_owner": random.choice(["Operations", "Analytics", "Technology Services", "Data Governance Office", "Unassigned"]),
        "created_date": today - timedelta(days=random.randint(1, 180)),
        "target_resolution_date": today + timedelta(days=random.randint(7, 90)),
    })

issues = pd.DataFrame(issue_rows)
issues.to_csv(SYNTHETIC_DIR / "data_issue_log.csv", index=False)

access_rows = []
for i in range(1, 46):
    dataset = metadata.sample(1, random_state=200 + i).iloc[0]
    access_rows.append({
        "request_id": f"ADL-{i:03d}",
        "dataset_id": dataset["dataset_id"],
        "dataset_name": dataset["dataset_name"],
        "requester_role": random.choice(["Analyst", "Manager", "External Partner", "Operations Lead", "Researcher"]),
        "requested_access": random.choice(["Read Only", "Download", "Dashboard Access", "External Sharing", "Temporary Access"]),
        "business_need": random.choice([
            "Operational reporting", "Service planning", "Executive briefing",
            "Research and analysis", "Cross-divisional coordination",
        ]),
        "minimum_necessary_checked": random.choice(["Yes", "Yes", "No"]),
        "sensitive_data_involved": "Yes" if dataset["access_risk_level"] == "High" else random.choice(["No", "No", "Yes"]),
        "risk_level": dataset["access_risk_level"],
        "decision": random.choice(["Approved", "Approved with Conditions", "Denied", "Pending Review"]),
        "decision_date": today - timedelta(days=random.randint(1, 90)),
        "review_date": today + timedelta(days=random.randint(30, 365)),
        "decision_rationale": random.choice([
            "Business need confirmed", "Access limited to aggregated output",
            "Requires additional approval", "Insufficient justification",
            "Temporary access approved with review date",
        ]),
    })

access = pd.DataFrame(access_rows)
access.to_csv(SYNTHETIC_DIR / "access_decision_log.csv", index=False)

lineage_rows = []
for _, row in metadata.iterrows():
    lineage_rows.append({
        "dataset_id": row["dataset_id"],
        "source_dataset": row["dataset_name"],
        "transformation_step": random.choice([
            "Standardize schema and data types",
            "Validate required fields and coordinates",
            "Join to district and ward reference layers",
            "Calculate governance and AI-readiness score",
            "Aggregate into executive dashboard mart",
        ]),
        "dashboard_layer": random.choice([
            "3D City View", "Asset Risk Layer", "Service Demand Layer",
            "Data Quality Layer", "Governance Maturity Layer", "AI Readiness Layer",
        ]),
        "reporting_output": random.choice([
            "Executive Control Panel", "Operational Risk View", "Governance Scorecard",
            "AI Readiness Summary", "Access Risk Register",
        ]),
        "lineage_status": row["lineage_status"],
    })

lineage = pd.DataFrame(lineage_rows)
lineage.to_csv(SYNTHETIC_DIR / "lineage_map.csv", index=False)

print("Advanced demo data generated successfully.")
print(f"Assets: {len(assets):,}")
print(f"Service requests: {len(requests):,}")
print(f"Datasets governed: {len(metadata):,}")
