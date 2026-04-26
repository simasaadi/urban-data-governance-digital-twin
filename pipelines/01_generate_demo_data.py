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
    {"dataset_id": "DS-001", "dataset_name": "Toronto 3D Massing", "source_type": "Toronto Open Data", "business_function": "3D Urban Context", "data_owner": "Open Data Team", "data_steward": "Assigned", "refresh_frequency": "Periodic", "data_classification": "Public", "access_risk_level": "Low"},
    {"dataset_id": "DS-002", "dataset_name": "Neighbourhoods", "source_type": "Toronto Open Data", "business_function": "Geographic Reporting", "data_owner": "Open Data Team", "data_steward": "Assigned", "refresh_frequency": "Periodic", "data_classification": "Public", "access_risk_level": "Low"},
    {"dataset_id": "DS-003", "dataset_name": "City Wards and Ward Profiles", "source_type": "Toronto Open Data", "business_function": "Council and Executive Reporting", "data_owner": "Open Data Team", "data_steward": "Assigned", "refresh_frequency": "Council Term", "data_classification": "Public", "access_risk_level": "Low"},
    {"dataset_id": "DS-004", "dataset_name": "Toronto Centreline", "source_type": "Toronto Open Data", "business_function": "Transportation and Routing Context", "data_owner": "Transportation Data Team", "data_steward": "Assigned", "refresh_frequency": "Monthly", "data_classification": "Public", "access_risk_level": "Low"},
    {"dataset_id": "DS-005", "dataset_name": "Solid Waste Management Districts", "source_type": "Toronto Open Data", "business_function": "Solid Waste Operations", "data_owner": "Operations", "data_steward": "Assigned", "refresh_frequency": "Periodic", "data_classification": "Public", "access_risk_level": "Low"},
    {"dataset_id": "DS-006", "dataset_name": "Solid Waste In-Park Assets", "source_type": "Toronto Open Data", "business_function": "Asset Management", "data_owner": "Operations", "data_steward": "Assigned", "refresh_frequency": "Ad hoc", "data_classification": "Public", "access_risk_level": "Low"},
    {"dataset_id": "DS-007", "dataset_name": "Litter Bin Collection Frequency", "source_type": "Toronto Open Data", "business_function": "Collection Operations", "data_owner": "Operations", "data_steward": "Assigned", "refresh_frequency": "Monthly", "data_classification": "Public", "access_risk_level": "Low"},
    {"dataset_id": "DS-008", "dataset_name": "311 Service Requests", "source_type": "Toronto Open Data", "business_function": "Service Demand Monitoring", "data_owner": "Customer Experience", "data_steward": "Assigned", "refresh_frequency": "Daily", "data_classification": "Public Aggregated", "access_risk_level": "Medium"},
    {"dataset_id": "DS-009", "dataset_name": "Road Restrictions", "source_type": "Toronto Open Data", "business_function": "Operational Disruption Monitoring", "data_owner": "Transportation Services", "data_steward": "Assigned", "refresh_frequency": "Daily", "data_classification": "Public", "access_risk_level": "Low"},
    {"dataset_id": "DS-010", "dataset_name": "Synthetic Metadata Catalog", "source_type": "Synthetic Governance Layer", "business_function": "Data Governance Controls", "data_owner": "Data Governance Office", "data_steward": "Assigned", "refresh_frequency": "Monthly", "data_classification": "Internal", "access_risk_level": "Medium"},
    {"dataset_id": "DS-011", "dataset_name": "Synthetic Access Decision Log", "source_type": "Synthetic Governance Layer", "business_function": "Access Governance", "data_owner": "Data Governance Office", "data_steward": "Assigned", "refresh_frequency": "Monthly", "data_classification": "Internal", "access_risk_level": "High"},
    {"dataset_id": "DS-012", "dataset_name": "Synthetic AI Readiness Scores", "source_type": "Synthetic Governance Layer", "business_function": "AI Readiness Assessment", "data_owner": "Analytics", "data_steward": "Assigned", "refresh_frequency": "Monthly", "data_classification": "Internal", "access_risk_level": "Medium"},
]

metadata_rows = []
for d in datasets:
    if d["source_type"] == "Toronto Open Data":
        metadata_base = random.randint(78, 98)
        lineage = random.choice(["Documented", "Documented", "Partially Documented"])
        definition = random.choice(["Complete", "Complete", "Partial"])
    else:
        metadata_base = random.randint(70, 95)
        lineage = random.choice(["Documented", "Partially Documented"])
        definition = random.choice(["Complete", "Partial"])

    metadata_rows.append({
        **d,
        "lineage_status": lineage,
        "business_definition_status": definition,
        "metadata_completeness_score": metadata_base,
        "system_of_record": random.choice(["Open Data Portal", "Operational Source System", "Governance Control Register", "Analytics Mart"]),
        "last_reviewed_date": today - timedelta(days=random.randint(5, 220)),
    })

metadata_catalog = pd.DataFrame(metadata_rows)
metadata_catalog.to_csv(SYNTHETIC_DIR / "metadata_catalog.csv", index=False)

quality_rows = []
for _, row in metadata_catalog.iterrows():
    if row["source_type"] == "Toronto Open Data":
        completeness = random.randint(78, 98)
        validity = random.randint(76, 98)
        uniqueness = random.randint(80, 99)
        consistency = random.randint(72, 96)
        timeliness = random.randint(65, 96)
    else:
        completeness = random.randint(65, 92)
        validity = random.randint(68, 95)
        uniqueness = random.randint(72, 98)
        consistency = random.randint(62, 93)
        timeliness = random.randint(60, 90)

    total_score = round((completeness + validity + uniqueness + consistency + timeliness) / 5, 1)
    failed_checks = int(max(0, round((100 - total_score) / 7 + random.randint(0, 3))))
    open_critical = random.choice([0, 0, 0, 1]) if total_score >= 75 else random.choice([0, 1, 1, 2])

    quality_rows.append({
        "dataset_id": row["dataset_id"],
        "dataset_name": row["dataset_name"],
        "completeness_score": completeness,
        "validity_score": validity,
        "uniqueness_score": uniqueness,
        "consistency_score": consistency,
        "timeliness_score": timeliness,
        "data_quality_score": total_score,
        "failed_checks": failed_checks,
        "open_critical_issues": open_critical,
        "last_quality_check_date": today,
    })

data_quality_results = pd.DataFrame(quality_rows)
data_quality_results.to_csv(SYNTHETIC_DIR / "data_quality_results.csv", index=False)

ai_rows = []
for _, row in metadata_catalog.iterrows():
    dq_score = float(data_quality_results.loc[data_quality_results["dataset_id"] == row["dataset_id"], "data_quality_score"].iloc[0])
    lineage_score = 100 if row["lineage_status"] == "Documented" else 65
    definition_score = 100 if row["business_definition_status"] == "Complete" else 65
    access_penalty = {"Low": 0, "Medium": 8, "High": 18}[row["access_risk_level"]]

    ai_score = round(
        dq_score * 0.35
        + row["metadata_completeness_score"] * 0.25
        + lineage_score * 0.20
        + definition_score * 0.20
        - access_penalty,
        1,
    )
    ai_score = max(0, min(100, ai_score))

    if row["access_risk_level"] == "High" and row["data_classification"] != "Public":
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
        "data_quality_score": dq_score,
        "metadata_completeness_score": row["metadata_completeness_score"],
        "lineage_status": row["lineage_status"],
        "business_definition_status": row["business_definition_status"],
        "access_risk_level": row["access_risk_level"],
        "data_classification": row["data_classification"],
        "ai_readiness_score": ai_score,
        "ai_readiness_category": category,
    })

ai_readiness_scores = pd.DataFrame(ai_rows)
ai_readiness_scores.to_csv(SYNTHETIC_DIR / "ai_readiness_scores.csv", index=False)

neighbourhoods = [
    "Downtown Yonge East", "Waterfront Communities", "Annex", "Kensington Chinatown",
    "High Park North", "Danforth East York", "Scarborough Village", "Agincourt South",
    "North York Centre", "Etobicoke Centre", "York University Heights", "Flemingdon Park",
]

districts = ["District 1 West", "District 2 North", "District 3 East", "District 4 South"]
asset_types = ["Litter Bin", "Recycling Bin", "Park Waste Bin", "Container", "Public Realm Asset"]
service_levels = ["Daily", "3x weekly", "2x weekly", "Weekly", "On demand"]

asset_rows = []
for i in range(1, 701):
    lat = np.random.uniform(43.59, 43.82)
    lon = np.random.uniform(-79.62, -79.16)
    neighbourhood = random.choice(neighbourhoods)
    district = random.choice(districts)
    asset_type = random.choice(asset_types)
    service_frequency = random.choice(service_levels)

    service_pressure = int(np.clip(np.random.normal(62, 22), 5, 100))
    data_quality_risk = int(np.clip(np.random.normal(38, 22), 0, 100))
    governance_maturity = int(np.clip(np.random.normal(72, 18), 10, 100))
    access_risk = random.choice(["Low", "Low", "Medium", "Medium", "High"])
    ai_score = int(np.clip((100 - data_quality_risk) * 0.38 + governance_maturity * 0.42 + random.randint(-10, 12), 0, 100))
    stale_days = int(np.clip(np.random.normal(45, 35), 0, 240))

    risk_index = round(
        service_pressure * 0.35
        + data_quality_risk * 0.30
        + (100 - governance_maturity) * 0.20
        + (20 if access_risk == "High" else 8 if access_risk == "Medium" else 0)
        + min(stale_days / 6, 15),
        1,
    )
    risk_index = max(0, min(100, risk_index))

    if risk_index >= 75:
        risk_tier = "Critical"
        color = [214, 39, 40, 190]
    elif risk_index >= 55:
        risk_tier = "High"
        color = [255, 127, 14, 180]
    elif risk_index >= 35:
        risk_tier = "Moderate"
        color = [255, 193, 7, 165]
    else:
        risk_tier = "Low"
        color = [44, 160, 44, 150]

    asset_rows.append({
        "asset_id": f"ASSET-{i:05d}",
        "asset_type": asset_type,
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "neighbourhood": neighbourhood,
        "ward": f"Ward {random.randint(1, 25)}",
        "service_district": district,
        "service_frequency": service_frequency,
        "service_pressure_score": service_pressure,
        "data_quality_risk_score": data_quality_risk,
        "governance_maturity_score": governance_maturity,
        "access_risk_level": access_risk,
        "ai_readiness_score": ai_score,
        "stale_days": stale_days,
        "open_issue_count": random.choice([0, 0, 0, 1, 1, 2, 3]),
        "risk_index": risk_index,
        "risk_tier": risk_tier,
        "risk_color": color,
        "radius_m": 45 + risk_index * 2.2,
        "elevation_m": max(30, risk_index * 12),
        "last_updated": today - timedelta(days=stale_days),
    })

municipal_assets = pd.DataFrame(asset_rows)
municipal_assets.to_csv(PROCESSED_DIR / "municipal_asset_risk_layer.csv", index=False)

request_categories = [
    "Missed Collection", "Overflowing Litter Bin", "Illegal Dumping",
    "Damaged Bin", "Public Realm Cleanliness", "Collection Schedule Inquiry",
]

request_rows = []
for i in range(1, 1201):
    status = random.choice(["Open", "Open", "In Progress", "Closed", "Closed", "Closed"])
    request_rows.append({
        "request_id": f"SR-{i:06d}",
        "category": random.choice(request_categories),
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

service_requests = pd.DataFrame(request_rows)
service_requests.to_csv(PROCESSED_DIR / "service_request_demand_layer.csv", index=False)

district_summary = (
    municipal_assets.groupby("service_district")
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

for col in ["avg_risk_index", "avg_service_pressure", "avg_data_quality_risk", "avg_governance_maturity", "avg_ai_readiness"]:
    district_summary[col] = district_summary[col].round(1)

district_summary.to_csv(PROCESSED_DIR / "district_governance_summary.csv", index=False)

lineage_rows = []
for _, row in metadata_catalog.iterrows():
    lineage_rows.append({
        "dataset_id": row["dataset_id"],
        "source_dataset": row["dataset_name"],
        "transformation_step": random.choice([
            "Standardize schema and data types",
            "Validate required fields and coordinates",
            "Join to district and ward reference layers",
            "Calculate governance and AI readiness score",
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

pd.DataFrame(lineage_rows).to_csv(SYNTHETIC_DIR / "lineage_map.csv", index=False)

issue_rows = []
root_causes = [
    "Missing owner assignment", "Unclear business definition", "Duplicate operational record",
    "Stale source extract", "Manual transformation risk", "Incomplete lineage",
    "Access approval gap", "Invalid coordinate value",
]

for i in range(1, 46):
    dataset = metadata_catalog.sample(1, random_state=100 + i).iloc[0]
    issue_rows.append({
        "issue_id": f"DQI-{i:03d}",
        "dataset_id": dataset["dataset_id"],
        "dataset_name": dataset["dataset_name"],
        "issue_title": random.choice(root_causes),
        "severity": random.choice(["Low", "Medium", "High", "Critical"]),
        "status": random.choice(["Open", "In Review", "Resolved", "Deferred"]),
        "assigned_owner": random.choice(["Operations", "Analytics", "Technology Services", "Data Governance Office", "Unassigned"]),
        "root_cause_category": random.choice(root_causes),
        "created_date": today - timedelta(days=random.randint(1, 180)),
        "target_resolution_date": today + timedelta(days=random.randint(7, 90)),
    })

pd.DataFrame(issue_rows).to_csv(SYNTHETIC_DIR / "data_issue_log.csv", index=False)

access_rows = []
for i in range(1, 36):
    dataset = metadata_catalog.sample(1, random_state=200 + i).iloc[0]
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

pd.DataFrame(access_rows).to_csv(SYNTHETIC_DIR / "access_decision_log.csv", index=False)

print("Generated flagship demo datasets successfully.")
