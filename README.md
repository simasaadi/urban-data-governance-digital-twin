# \# Urban Data Governance Digital Twin

# 

# <p align="center">

# &#x20; <a href="https://urban-data-governance-digital-twin.streamlit.app/" target="\_blank">

# &#x20;   <img src="https://img.shields.io/badge/Launch%20Interactive%20Dashboard-Urban%20Data%20Governance%20Digital%20Twin-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white" alt="Launch Interactive Dashboard"/>

# &#x20; </a>

# </p>

# 

# <p align="center">

# &#x20; <b>3D municipal operations dashboard with data quality, access risk, metadata completeness, service performance, lineage, and AI-readiness indicators.</b>

# </p>

# 

# \---

# 

# \## Project Overview

# 

# The \*\*Urban Data Governance Digital Twin\*\* is an interactive 3D municipal analytics and data governance dashboard. It demonstrates how operational data can be transformed into a decision-support product that supports service monitoring, data quality control, access governance, metadata management, lineage visibility, and AI-readiness assessment.

# 

# This project shows how data governance can move beyond policy documents into practical, measurable, operational tools.

# 

# The dashboard combines:

# 

# \- 3D geospatial visualization

# \- Municipal service performance monitoring

# \- Data quality risk scoring

# \- Metadata completeness tracking

# \- Access and privacy risk controls

# \- Issue management

# \- Lineage mapping

# \- AI-readiness scoring

# \- Executive-level KPIs

# 

# \---

# 

# \## Live Dashboard

# 

# <p align="center">

# &#x20; <a href="https://urban-data-governance-digital-twin.streamlit.app/" target="\_blank">

# &#x20;   <img src="https://img.shields.io/badge/Open%20Dashboard-Click%20Here-0E1117?style=for-the-badge\&logo=streamlit\&logoColor=white" alt="Open Dashboard"/>

# &#x20; </a>

# </p>

# 

# \---

# 

# \## Why This Project Matters

# 

# Many organizations want to use analytics, automation, and AI, but their operational data is often not ready. Common issues include incomplete metadata, unclear ownership, inconsistent definitions, weak lineage, unresolved data quality issues, unclear access rules, and limited visibility into whether datasets are fit for reporting or advanced analytics.

# 

# This project demonstrates a practical model for answering questions such as:

# 

# \- Which datasets are trusted enough for reporting?

# \- Which assets or service areas have the highest operational risk?

# \- Where are data quality problems concentrated?

# \- Which datasets are ready for AI or automation?

# \- Which datasets require access restrictions or approval?

# \- Which reports depend on weak lineage or incomplete metadata?

# \- Where should governance remediation start first?

# 

# \---

# 

# \## Dashboard Modules

# 

# \### 1. Executive Control Panel

# 

# The executive view summarizes the overall operational and governance risk position.

# 

# Key indicators include:

# 

# \- Datasets governed

# \- Assets monitored

# \- Service requests

# \- Average data quality score

# \- Average AI-readiness score

# \- Open governance issues

# \- Highest-risk assets and service districts

# 

# \### 2. 3D Digital Twin

# 

# The 3D map shows municipal assets and service-demand signals across Toronto-style geography.

# 

# The map supports interactive views for:

# 

# \- Operational risk

# \- Service pressure

# \- Data quality risk

# \- Governance maturity

# \- AI-readiness

# 

# 3D column height changes based on the selected metric, while colours represent risk tier.

# 

# \### 3. Service Performance

# 

# This section shows synthetic service demand patterns, including:

# 

# \- Service requests by category

# \- Open, closed, and in-progress requests

# \- District-level demand

# \- Priority levels

# \- Days open

# 

# \### 4. Data Quality Risk

# 

# This module shows data quality performance across governed datasets.

# 

# Quality dimensions include:

# 

# \- Completeness

# \- Validity

# \- Uniqueness

# \- Consistency

# \- Timeliness

# 

# The dashboard also includes a data issue log showing severity, status, assigned owner, and target resolution date.

# 

# \### 5. Access and Privacy

# 

# This section demonstrates access governance logic through a synthetic access decision register.

# 

# It includes:

# 

# \- Access request type

# \- Requester role

# \- Business need

# \- Risk level

# \- Sensitive data flag

# \- Minimum necessary review

# \- Decision status

# \- Review date

# \- Decision rationale

# 

# \### 6. Metadata, Lineage, and AI-Readiness

# 

# This section links governance controls to AI-readiness.

# 

# AI-readiness is scored using:

# 

# \- Data quality score

# \- Metadata completeness

# \- Lineage status

# \- Business definition status

# \- Data classification

# \- Access risk level

# 

# Datasets are categorized as:

# 

# \- Ready

# \- Needs Remediation

# \- Not Ready

# \- Restricted

# 

# \---

# 

# \## Data Sources and Design

# 

# This repository is designed around a safe public/synthetic data model.

# 

# \### Planned Public Data Layers

# 

# The project is structured to support Toronto Open Data layers such as:

# 

# \- Toronto 3D Massing

# \- Neighbourhoods

# \- City Wards and Ward Profiles

# \- Toronto Centreline

# \- Solid Waste Management Districts

# \- Solid Waste In-Park Assets

# \- Litter Bin Collection Frequency

# \- 311 Service Requests

# \- Road Restrictions

# \- Building Permits

# \- Traffic Movement Counts

# \- Cycling Network

# 

# \### Synthetic Governance Layers

# 

# The current version uses synthetic governance and operational records for demonstration.

# 

# Synthetic datasets include:

# 

# \- Metadata catalog

# \- Data quality results

# \- Data issue log

# \- Access decision log

# \- AI-readiness scores

# \- Lineage map

# \- Municipal asset risk layer

# \- Service request demand layer

# \- District governance summary

# 

# No confidential, private, employer-owned, client-owned, or internal project data is used.

# 

# \---

# 

# \## Technical Stack

# 

# | Layer | Tools |

# |---|---|

# | Dashboard | Streamlit |

# | 3D Mapping | PyDeck / deck.gl |

# | Charts | Plotly |

# | Data Processing | Python, pandas, NumPy |

# | Data Storage | CSV demo marts |

# | Governance Logic | Synthetic scoring rules |

# | Deployment | Streamlit Cloud |

# | Version Control | GitHub |

# 

# \---

# 

# \## Repository Structure

# 

# ```text

# urban-data-governance-digital-twin/

# │

# ├── app/

# │   └── streamlit\_app.py

# │

# ├── data/

# │   ├── raw/

# │   ├── processed/

# │   │   ├── municipal\_asset\_risk\_layer.csv

# │   │   ├── service\_request\_demand\_layer.csv

# │   │   └── district\_governance\_summary.csv

# │   ├── synthetic/

# │   │   ├── metadata\_catalog.csv

# │   │   ├── data\_quality\_results.csv

# │   │   ├── data\_issue\_log.csv

# │   │   ├── access\_decision\_log.csv

# │   │   ├── ai\_readiness\_scores.csv

# │   │   └── lineage\_map.csv

# │   └── external/

# │

# ├── governance/

# │   ├── business\_rules.yml

# │   └── dq\_rules.yml

# │

# ├── pipelines/

# │   ├── 01\_generate\_demo\_data.py

# │   └── 01\_generate\_synthetic\_governance\_data.py

# │

# ├── docs/

# │   └── screenshots/

# │

# ├── notebooks/

# ├── tests/

# ├── requirements.txt

# ├── README.md

# └── LICENSE

# ```

# 

# \---

# 

# \## Governance Scoring Logic

# 

# The project uses governance-oriented scoring to connect operational analytics with data management controls.

# 

# \### Data Quality Score

# 

# Calculated from:

# 

# \- Completeness

# \- Validity

# \- Uniqueness

# \- Consistency

# \- Timeliness

# 

# \### Governance Maturity Score

# 

# Based on:

# 

# \- Assigned data owner

# \- Assigned data steward

# \- Metadata completeness

# \- Classification status

# \- Business definition status

# \- Lineage status

# 

# \### AI-Readiness Score

# 

# Based on:

# 

# \- Data quality score

# \- Metadata completeness

# \- Lineage documentation

# \- Business definition status

# \- Data classification

# \- Access risk

# 

# \### Operational Risk Index

# 

# The synthetic operational risk index combines:

# 

# \- Service pressure

# \- Data quality risk

# \- Governance maturity

# \- Stale records

# \- Access risk

# \- Open issues

# 

# \---

# 

# \## How to Run Locally

# 

# Clone the repository:

# 

# ```bash

# git clone https://github.com/simasaadi/urban-data-governance-digital-twin.git

# cd urban-data-governance-digital-twin

# ```

# 

# Create a virtual environment:

# 

# ```bash

# python -m venv .venv

# ```

# 

# Activate the virtual environment on Windows PowerShell:

# 

# ```bash

# .venv\\Scripts\\Activate.ps1

# ```

# 

# Install dependencies:

# 

# ```bash

# pip install -r requirements.txt

# ```

# 

# Generate the demo data:

# 

# ```bash

# python pipelines/01\_generate\_demo\_data.py

# ```

# 

# Run the dashboard:

# 

# ```bash

# streamlit run app/streamlit\_app.py

# ```

# 

# \---

# 

# \## Professional Use Case

# 

# This project demonstrates skills relevant to roles such as:

# 

# \- Data Governance Specialist

# \- Data Quality Analyst

# \- Analytics Engineer

# \- BI Developer

# \- Data Visualization Specialist

# \- AI Governance Analyst

# \- Public Sector Data Analyst

# \- GIS / Urban Analytics Analyst

# \- Decision Support Analyst

# 

# It is designed to show the ability to connect governance, analytics engineering, dashboard design, geospatial visualization, and executive decision support in one working product.

# 

# \---

# 

# \## Data Ethics and Confidentiality

# 

# This project uses public-data architecture and synthetic governance records only.

# 

# It does not use confidential employer data, client data, private data, or internal project material.

# 

# This project is not affiliated with or endorsed by the City of Toronto. Public open-data references are used only as a safe design basis for a professional demonstration.

# 

# \---

# 

# \## Next Development Roadmap

# 

# Planned improvements include:

# 

# \- Integrating real Toronto Open Data geospatial files

# \- Adding 3D building massing and neighbourhood polygons

# \- Exporting processed dashboard marts to Parquet

# \- Adding DuckDB analytics queries

# \- Adding automated data quality tests

# \- Adding architecture diagrams

# \- Adding dashboard screenshots

# \- Adding CI checks through GitHub Actions

# \- Expanding metadata and lineage documentation

# 

# \---

# 

# \## Author

# 

# \*\*Sima Saadi\*\*  

# Applied Data Scientist | Data Governance | Analytics Engineering | BI \& Decision Support

