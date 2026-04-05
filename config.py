"""
config.py — Supply Chain ETL & Analytics
"""
N_SHIPMENTS = 1_000
N_SKUS      = 200
SEED        = 99
DB_PATH     = "supply_chain.db"

LOG_FORMAT   = "%(asctime)s  [%(levelname)s]  %(message)s"
LOG_DATE_FMT = "%H:%M:%S"
LOG_LEVEL    = "INFO"

CHART_OUTPUT = "supply_chain_dashboard.png"
CHART_DPI    = 150
