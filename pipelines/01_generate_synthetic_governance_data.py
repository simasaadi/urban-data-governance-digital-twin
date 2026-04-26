import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import random

BASE_DIR = Path(__file__).resolve().parents[1]
SYNTHETIC_DIR = BASE_DIR / "data" / "synthetic"
SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

datasets = [
    "Toronto 3D Massing",
    "Neighbourhoods",
    "City Wards",
    "Toronto Centreline",
    "Solid Waste Management Districts",
    "Solid Waste In-Park Assets",
    "Litter Bin Collection Frequency",
    "311 Service Requests",
    "Road Restrictions",
    "Building Permits",
    "Traffic Movement Counts",
    "Cycling Network"
]

business_functions = [
    "Public Realm Operations",
    "Solid Waste Collection",
    "Asset Management",
    "Service Request Management",
    "Transportation Planning",
    "Urban Growth Monitoring",
    "Executive Reporting"
]

classifications = ["Public", "Internal", "Confidential"]
lineage_statuses = ["Documented", "Partially Documented", "Not Documented"]
definition_statuses = ["Complete", "Partial", "Missing"]
refresh_frequencies = ["Daily", "Weekly", "Monthly", "Quarterly", "Ad hoc"]

metadata_rows = []

for i, dataset in enumerate(datasets, start=1):
    metadata_rows.append({
        "dataset_id": f"DS-{i:03d}",
        "dataset_name": dataset,
        "data_owner": random.choice(["Operations", "Analytics", "Technology Services", "Policy & Planning", "Open Data Team", "Unassigned"]),
        "data_steward": random.choice(["Assigned", "Assigned", "Unassigned"]),
        "business_function": random.choice(business_functions),
        "source_type": random.choice(["Toronto Open Data", "Synthetic Governance Layer"]),
        "refresh_frequency": random.choice(refresh_frequencies),
        "data_classification": random.choice(classifications),
        "lineage_status": random.choice(lineage_statuses),
        "business_definition_status": random.choice(definition_statuses),
        "metadata_completeness_score": random.randint(45, 100),
        "access_risk_level": random.choice(["Low", "Medium", "High"]),
        "last_reviewed_date": (datetime.today() - timedelta(days=random.randint(1, 365))).date()
    })

metadata_catalog = pd.DataFrame(metadata_rows)
metadata_catalog.to_csv(SYNTHETIC_DIR / "metadata_catalog.csv", index=False)

quality_rows = []

for _, row in metadata_catalog.iterrows():
    completeness = random.randint(60, 100)
    validity = random.randint(55, 100)
    uniqueness = random.randint(70, 100)
    consistency = random.randint(50, 100)
    timeliness = random.randint(45, 100)
    total_score = round((completeness + validity + uniqueness + consistency + timeliness) / 5, 1)

    quality_rows.append({
        "dataset_id": row["dataset_id"],
        "dataset_name": row["dataset_name"],
        "completeness_score": completeness,
        "validity_score": validity,
        "uniqueness_score": uniqueness,
        "consistency_score": consistency,
        "timeliness_score": timeliness,
        "data_quality_score": total_score,
        "failed_checks": random.randint(0, 12),
        "open_critical_issues": random.randint(0, 3),
        "last_quality_check_date": datetime.today().date()
    })

data_quality_results = pd.DataFrame(quality_rows)
data_quality_results.to_csv(SYNTHETIC_DIR / "data_quality_results.csv", index=False)

issue_rows = []
root_causes = [
    "Missing required field",
    "Unclear business definition",
    "Duplicate record",
    "Stale extract",
    "Manual transformation error",
    "Unassigned data owner",
    "Incomplete lineage",
    "Access approval missing"
]

statuses = ["Open", "In Review", "Resolved", "Deferred"]
severities = ["Low", "Medium", "High", "Critical"]

for i in range(1, 31):
    dataset = metadata_catalog.sample(1, random_state=42 + i).iloc[0]
    issue_rows.append({
        "issue_id": f"DQI-{i:03d}",
        "dataset_id": dataset["dataset_id"],
        "dataset_name": dataset["dataset_name"],
        "issue_title": random.choice(root_causes),
        "severity": random.choice(severities),
        "status": random.choice(statuses),
        "assigned_owner": random.choice(["Operations", "Analytics", "Technology Services", "Policy & Planning", "Unassigned"]),
        "root_cause_category": random.choice(root_causes),
        "created_date": (datetime.today() - timedelta(days=random.randint(1, 180))).date(),
        "target_resolution_date": (datetime.today() + timedelta(days=random.randint(5, 90))).date()
    })

data_issue_log = pd.DataFrame(issue_rows)
data_issue_log.to_csv(SYNTHETIC_DIR / "data_issue_log.csv", index=False)

access_rows = []
decisions = ["Approved", "Approved with Conditions", "Denied", "Pending Review"]

for i in range(1, 26):
    dataset = metadata_catalog.sample(1, random_state=100 + i).iloc[0]
    access_rows.append({
        "request_id": f"ADL-{i:03d}",
        "dataset_id": dataset["dataset_id"],
        "dataset_name": dataset["dataset_name"],
        "requester_role": random.choice(["Analyst", "Manager", "External Partner", "Operations Lead", "Researcher"]),
        "requested_access": random.choice(["Read Only", "Download", "Dashboard Access", "External Sharing", "Temporary Access"]),
        "business_need": random.choice([
            "Operational reporting",
            "Service planning",
            "Executive briefing",
            "Research and analysis",
            "Cross-divisional coordination"
        ]),
        "minimum_necessary_checked": random.choice(["Yes", "No"]),
        "sensitive_data_involved": "Yes" if dataset["data_classification"] == "Confidential" else random.choice(["No", "No", "Yes"]),
        "risk_level": dataset["access_risk_level"],
        "decision": random.choice(decisions),
        "decision_date": (datetime.today() - timedelta(days=random.randint(1, 90))).date(),
        "review_date": (datetime.today() + timedelta(days=random.randint(30, 365))).date(),
        "decision_rationale": random.choice([
            "Business need confirmed",
            "Access limited to aggregated output",
            "Requires additional approval",
            "Insufficient justification",
            "Temporary access approved with review date"
        ])
    })

access_decision_log = pd.DataFrame(access_rows)
access_decision_log.to_csv(SYNTHETIC_DIR / "access_decision_log.csv", index=False)

ai_rows = []

for _, row in metadata_catalog.iterrows():
    dq_score = data_quality_results.loc[
        data_quality_results["dataset_id"] == row["dataset_id"], "data_quality_score"
    ].iloc[0]

    metadata_score = row["metadata_completeness_score"]
    lineage_score = 100 if row["lineage_status"] == "Documented" else 60 if row["lineage_status"] == "Partially Documented" else 25
    definition_score = 100 if row["business_definition_status"] == "Complete" else 60 if row["business_definition_status"] == "Partial" else 25
    access_penalty = 0 if row["access_risk_level"] == "Low" else 10 if row["access_risk_level"] == "Medium" else 25

    ai_score = round((dq_score * 0.35) + (metadata_score * 0.25) + (lineage_score * 0.2) + (definition_score * 0.2) - access_penalty, 1)
    ai_score = max(0, min(100, ai_score))

    if row["data_classification"] == "Confidential" and row["access_risk_level"] == "High":
        readiness = "Restricted"
    elif ai_score >= 80:
        readiness = "Ready"
    elif ai_score >= 50:
        readiness = "Needs Remediation"
    else:
        readiness = "Not Ready"

    ai_rows.append({
        "dataset_id": row["dataset_id"],
        "dataset_name": row["dataset_name"],
        "data_quality_score": dq_score,
        "metadata_completeness_score": metadata_score,
        "lineage_status": row["lineage_status"],
        "business_definition_status": row["business_definition_status"],
        "access_risk_level": row["access_risk_level"],
        "data_classification": row["data_classification"],
        "ai_readiness_score": ai_score,
        "ai_readiness_category": readiness
    })

ai_readiness_scores = pd.DataFrame(ai_rows)
ai_readiness_scores.to_csv(SYNTHETIC_DIR / "ai_readiness_scores.csv", index=False)

lineage_rows = []

for _, row in metadata_catalog.iterrows():
    lineage_rows.append({
        "dataset_id": row["dataset_id"],
        "source_dataset": row["dataset_name"],
        "transformation_step": "Data quality validation and governance scoring",
        "dashboard_layer": random.choice([
            "3D City View",
            "Asset Risk Layer",
            "Service Demand Layer",
            "Data Quality Layer",
            "Governance Maturity Layer",
            "AI-Readiness Layer"
        ]),
        "reporting_output": random.choice([
            "Executive Control Panel",
            "Operational Risk View",
            "Governance Scorecard",
            "AI Readiness Summary",
            "Access Risk Register"
        ]),
        "lineage_status": row["lineage_status"]
    })

lineage_map = pd.DataFrame(lineage_rows)
lineage_map.to_csv(SYNTHETIC_DIR / "lineage_map.csv", index=False)

print("Synthetic governance datasets created successfully:")
print(f"- {SYNTHETIC_DIR / 'metadata_catalog.csv'}")
print(f"- {SYNTHETIC_DIR / 'data_quality_results.csv'}")
print(f"- {SYNTHETIC_DIR / 'data_issue_log.csv'}")
print(f"- {SYNTHETIC_DIR / 'access_decision_log.csv'}")
print(f"- {SYNTHETIC_DIR / 'ai_readiness_scores.csv'}")
print(f"- {SYNTHETIC_DIR / 'lineage_map.csv'}")
