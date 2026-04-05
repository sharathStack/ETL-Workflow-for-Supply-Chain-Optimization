"""
extractor.py — Simulate extraction from shipment tracking + inventory systems
"""
import numpy as np, pandas as pd, logging
import config

log = logging.getLogger("SC_Extractor")

def extract_shipments() -> pd.DataFrame:
    log.info("EXTRACT | %d shipments...", config.N_SHIPMENTS)
    np.random.seed(config.SEED)
    n = config.N_SHIPMENTS
    carriers   = ["DHL","FedEx","UPS","BlueDart","Delhivery"]
    statuses   = ["Delivered","In Transit","Delayed","Returned","Lost"]
    origins    = ["Mumbai","Delhi","Bangalore","Chennai","Kolkata"]
    dests      = ["Hyderabad","Pune","Ahmedabad","Jaipur","Lucknow"]
    cats       = ["Electronics","Apparel","FMCG","Pharmaceuticals","Auto Parts"]

    dispatch    = pd.to_datetime("2024-01-01") + pd.to_timedelta(np.random.randint(0,365,n), unit="D")
    planned_d   = np.random.randint(1,10,n)
    delay_flag  = np.random.rand(n) < 0.20
    actual_d    = planned_d + np.where(delay_flag, np.random.randint(1,7,n), 0)

    df = pd.DataFrame({
        "shipment_id":           [f"SHP{str(i).zfill(6)}" for i in range(1,n+1)],
        "carrier":               np.random.choice(carriers, n),
        "origin":                np.random.choice(origins, n),
        "destination":           np.random.choice(dests, n),
        "category":              np.random.choice(cats, n),
        "dispatch_date":         dispatch,
        "planned_delivery_date": dispatch + pd.to_timedelta(planned_d, unit="D"),
        "actual_delivery_date":  dispatch + pd.to_timedelta(actual_d,  unit="D"),
        "weight_kg":             np.round(np.random.uniform(0.5, 100, n), 2),
        "shipping_cost":         np.round(np.random.uniform(50, 3_000, n), 2),
        "status":                np.random.choice(statuses, n, p=[0.70,0.15,0.10,0.03,0.02]),
        "distance_km":           np.random.randint(100, 3_000, n),
    })
    # Inject missing costs
    df.loc[np.random.choice(df.index, 30, replace=False), "shipping_cost"] = np.nan
    log.info("EXTRACT | %d shipments | 30 nulls injected", len(df))
    return df

def extract_inventory() -> pd.DataFrame:
    log.info("EXTRACT | %d SKU inventory snapshot...", config.N_SKUS)
    np.random.seed(config.SEED+1)
    n = config.N_SKUS
    whs = ["WH-HYD","WH-BLR","WH-DEL","WH-MUM","WH-CHN"]
    cats= ["Electronics","Apparel","FMCG","Pharmaceuticals","Auto Parts"]
    df = pd.DataFrame({
        "sku_id":        [f"SKU{str(i).zfill(4)}" for i in range(1,n+1)],
        "warehouse":     np.random.choice(whs, n),
        "category":      np.random.choice(cats, n),
        "units_on_hand": np.random.randint(0, 500, n),
        "reorder_level": np.random.randint(20, 80, n),
        "unit_cost":     np.round(np.random.uniform(10, 2_000, n), 2),
    })
    log.info("EXTRACT | %d SKUs", len(df))
    return df
