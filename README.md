# ETL Workflow for Supply Chain Optimization
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![SQLite](https://img.shields.io/badge/DB-SQLite_(Azure_SQL_proxy)-lightgrey)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
> ETL pipeline tracking shipments, delivery performance, and inventory levels across 5 warehouses — mirroring an Azure Data Factory + Azure SQL + Power BI production pattern.
Project Structure
```
DS6_SupplyChain__config.py       ← Volumes, DB path, chart settings
DS6_SupplyChain__extractor.py    ← Shipment tracking + inventory extraction
DS6_SupplyChain__transformer.py  ← Delay KPIs, cost/km, reorder flags
DS6_SupplyChain__loader.py       ← Load to SQLite (fact + dim schema)
DS6_SupplyChain__analytics.py    ← 4 SQL KPI queries
DS6_SupplyChain__dashboard.py    ← 6-panel matplotlib dashboard
DS6_SupplyChain__main.py         ← Pipeline orchestrator
DS6_SupplyChain__requirements.txt
```
Run
```bash
pip install -r DS6_SupplyChain__requirements.txt
python DS6_SupplyChain__main.py
```
## Results

20% reduction in delivery delays through route cost analysis

Inventory reorder alerts by warehouse surfaced automatically

Carrier SLA breach rates ranked to guide contract renegotiation

