"""
loader.py — Write transformed data to SQLite analytics schema (proxies Azure SQL)
"""
import sqlite3, logging
from datetime import datetime
import pandas as pd
import config

log = logging.getLogger("SC_Loader")

SCHEMA = """
CREATE TABLE IF NOT EXISTS fact_shipments (
    shipment_id TEXT PRIMARY KEY, carrier TEXT, origin TEXT,
    destination TEXT, category TEXT, route TEXT,
    dispatch_date TEXT, planned_delivery_date TEXT, actual_delivery_date TEXT,
    weight_kg REAL, shipping_cost REAL, distance_km INTEGER,
    status TEXT, delay_days INTEGER, delay_flag INTEGER,
    sla_breach_flag INTEGER, cost_per_km REAL, dispatch_month TEXT,
    load_ts TEXT
);
CREATE TABLE IF NOT EXISTS dim_inventory (
    sku_id TEXT PRIMARY KEY, warehouse TEXT, category TEXT,
    units_on_hand INTEGER, reorder_level INTEGER, unit_cost REAL,
    stock_value REAL, reorder_needed INTEGER, stock_status TEXT,
    load_ts TEXT
);
"""


def load(shipments: pd.DataFrame, inventory: pd.DataFrame) -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()

    ts = datetime.utcnow().isoformat()
    s  = shipments.copy(); s["load_ts"] = ts
    i  = inventory.copy(); i["load_ts"] = ts

    s.to_sql("fact_shipments", conn, if_exists="replace", index=False)
    i.to_sql("dim_inventory",  conn, if_exists="replace", index=False)
    conn.commit()

    log.info("LOAD | fact_shipments: %d rows", len(s))
    log.info("LOAD | dim_inventory:  %d rows", len(i))
    return conn
