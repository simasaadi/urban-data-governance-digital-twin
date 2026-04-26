@'
# Urban Data Governance Digital Twin

<p align="center">
  <a href="https://urban-data-governance-digital-twin.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/Launch%20Interactive%20Dashboard-Urban%20Data%20Governance%20Digital%20Twin-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Launch Interactive Dashboard"/>
  </a>
</p>

<p align="center">
  <b>3D municipal operations dashboard with data quality, access risk, metadata completeness, service performance, lineage, and AI-readiness indicators.</b>
</p>

---

## Project Overview

The **Urban Data Governance Digital Twin** is an interactive 3D municipal analytics and data governance dashboard. It demonstrates how operational data can be transformed into a decision-support product that supports service monitoring, data quality control, access governance, metadata management, lineage visibility, and AI-readiness assessment.

This project shows how data governance can move beyond policy documents into practical, measurable, operational tools.

The dashboard combines:

- 3D geospatial visualization
- Municipal service performance monitoring
- Data quality risk scoring
- Metadata completeness tracking
- Access and privacy risk controls
- Issue management
- Lineage mapping
- AI-readiness scoring
- Executive-level KPIs

---

## Live Dashboard

<p align="center">
  <a href="https://urban-data-governance-digital-twin.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/Open%20Dashboard-Click%20Here-0E1117?style=for-the-badge&logo=streamlit&logoColor=white" alt="Open Dashboard"/>
  </a>
</p>

---

## Why This Project Matters

Many organizations want to use analytics, automation, and AI, but their operational data is often not ready. Common issues include incomplete metadata, unclear ownership, inconsistent definitions, weak lineage, unresolved data quality issues, unclear access rules, and limited visibility into whether datasets are fit for reporting or advanced analytics.

This project demonstrates a practical model for answering questions such as:

- Which datasets are trusted enough for reporting?
- Which assets or service areas have the highest operational risk?
- Where are data quality problems concentrated?
- Which datasets are ready for AI or automation?
- Which datasets require access restrictions or approval?
- Which reports depend on weak lineage or incomplete metadata?
- Where should governance remediation start first?

---

## Dashboard Modules

| Module | What it Shows |
|---|---|
| **Executive Control Panel** | Overall operational and governance risk position, key KPIs, highest-risk assets, and service districts |
| **3D Digital Twin** | Interactive 3D municipal asset and service-demand map with risk-based columns |
| **Service Performance** | Synthetic service demand by category, status, district, priority, and days open |
| **Data Quality Risk** | Completeness, validity, uniqueness, consistency, timeliness, and issue severity |
| **Access and Privacy** | Access requests, risk level, sensitive-data flags, minimum necessary review, and decisions |
| **Metadata, Lineage, and AI-Readiness** | Metadata completeness, lineage coverage, AI-readiness categories, and governed dataset status |

---

## Data Sources and Design

This repository is designed around a safe public/synthetic data model.

### Planned Public Data Layers

The project is structured to support Toronto Open Data layers such as:

- Toronto 3D Massing
- Neighbourhoods
- City Wards and Ward Profiles
- Toronto Centreline
- Solid Waste Management Districts
- Solid Waste In-Park Assets
- Litter Bin Collection Frequency
- 311 Service Requests
- Road Restrictions
- Building Permits
- Traffic Movement Counts
- Cycling Network

### Synthetic Governance Layers

The current version uses synthetic governance and operational records for demonstration.

Synthetic datasets include:

- Metadata catalog
- Data quality results
- Data issue log
- Access decision log
- AI-readiness scores
- Lineage map
- Municipal asset risk layer
- Service request demand layer
- District governance summary

No confidential, private, employer-owned, client-owned, or internal project data is used.

---

## Technical Stack

| Layer | Tools |
|---|---|
| Dashboard | Streamlit |
| 3D Mapping | PyDeck / deck.gl |
| Charts | Plotly |
| Data Processing | Python, pandas, NumPy |
| Data Storage | CSV demo marts |
| Governance Logic | Synthetic scoring rules |
| Deployment | Streamlit Cloud |
| Version Control | GitHub |

---

## Repository Structure

```text
urban-data-governance-digital-twin/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   │   ├── municipal_asset_risk_layer.csv
│   │   ├── service_request_demand_layer.csv
│   │   └── district_governance_summary.csv
│   ├── synthetic/
│   │   ├── metadata_catalog.csv
│   │   ├── data_quality_results.csv
│   │   ├── data_issue_log.csv
│   │   ├── access_decision_log.csv
│   │   ├── ai_readiness_scores.csv
│   │   └── lineage_map.csv
│   └── external/
│
├── governance/
│   ├── business_rules.yml
│   └── dq_rules.yml
│
├── pipelines/
│   ├── 01_generate_demo_data.py
│   └── 01_generate_synthetic_governance_data.py
│
├── docs/
│   └── screenshots/
│
├── notebooks/
├── tests/
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Governance Scoring Logic

The project uses governance-oriented scoring to connect operational analytics with data management controls.

### Data Quality Score

Calculated from:

- Completeness
- Validity
- Uniqueness
- Consistency
- Timeliness

### Governance Maturity Score

Based on:

- Assigned data owner
- Assigned data steward
- Metadata completeness
- Classification status
- Business definition status
- Lineage status

### AI-Readiness Score

Based on:

- Data quality score
- Metadata completeness
- Lineage documentation
- Business definition status
- Data classification
- Access risk

### Operational Risk Index

The synthetic operational risk index combines:

- Service pressure
- Data quality risk
- Governance maturity
- Stale records
- Access risk
- Open issues

---

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/simasaadi/urban-data-governance-digital-twin.git
cd urban-data-governance-digital-twin
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the demo data:

```bash
python pipelines/01_generate_demo_data.py
```

Run the dashboard:

```bash
streamlit run app/streamlit_app.py
```

---

## Professional Use Case

This project demonstrates skills relevant to roles such as:

- Data Governance Specialist
- Data Quality Analyst
- Analytics Engineer
- BI Developer
- Data Visualization Specialist
- AI Governance Analyst
- Public Sector Data Analyst
- GIS / Urban Analytics Analyst
- Decision Support Analyst

It is designed to show the ability to connect governance, analytics engineering, dashboard design, geospatial visualization, and executive decision support in one working product.

---

## Data Ethics and Confidentiality

This project uses public-data architecture and synthetic governance records only.

It does not use confidential employer data, client data, private data, or internal project material.

This project is not affiliated with or endorsed by the City of Toronto. Public open-data references are used only as a safe design basis for a professional demonstration.

---

## Next Development Roadmap

Planned improvements include:

- Integrating real Toronto Open Data geospatial files
- Adding 3D building massing and neighbourhood polygons
- Exporting processed dashboard marts to Parquet
- Adding DuckDB analytics queries
- Adding automated data quality tests
- Adding architecture diagrams
- Adding dashboard screenshots
- Adding CI checks through GitHub Actions
- Expanding metadata and lineage documentation

---

## Author

**Sima Saadi**  
Applied Data Scientist | Data Governance | Analytics Engineering | BI & Decision Support
'@ | Set-Content -Path "README.md" -Encoding UTF8