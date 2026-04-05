"""
transformer.py — Clean, enrich, and derive KPIs from raw supply chain data
"""
import logging
import numpy as np
import pandas as pd

log = logging.getLogger("SC_Transformer")


def transform_shipments(df: pd.DataFrame) -> pd.DataFrame:
    log.info("TRANSFORM | Processing %d shipments...", len(df))
    df = df.copy()

    # Fill missing shipping cost with carrier-level median
    df["shipping_cost"] = df.groupby("carrier")["shipping_cost"].transform(
        lambda x: x.fillna(x.median())
    )

    # Derived KPIs
    df["delay_days"]      = (df["actual_delivery_date"] - df["planned_delivery_date"]).dt.days
    df["delay_flag"]      = (df["delay_days"] > 0).astype(int)
    df["sla_breach_flag"] = (df["delay_days"] > 3).astype(int)
    df["cost_per_km"]     = (df["shipping_cost"] / df["distance_km"].replace(0, np.nan)).round(4)
    df["route"]           = df["origin"] + " → " + df["destination"]
    df["dispatch_month"]  = df["dispatch_date"].dt.to_period("M").astype(str)

    log.info(
        "TRANSFORM | Delay rate: %.1f%%  |  SLA breach: %.1f%%",
        df["delay_flag"].mean() * 100,
        df["sla_breach_flag"].mean() * 100,
    )
    return df


def transform_inventory(df: pd.DataFrame) -> pd.DataFrame:
    log.info("TRANSFORM | Enriching %d SKUs...", len(df))
    df = df.copy()

    df["stock_value"]    = df["units_on_hand"] * df["unit_cost"]
    df["reorder_needed"] = (df["units_on_hand"] < df["reorder_level"]).astype(int)
    df["stock_status"]   = pd.cut(
        df["units_on_hand"],
        bins=[-1, 0, 20, 100, 10_000],
        labels=["Out of Stock", "Critical", "Healthy", "Overstocked"],
    )

    log.info(
        "TRANSFORM | Reorder needed: %d SKUs  |  Total stock value: $%,.0f",
        df["reorder_needed"].sum(),
        df["stock_value"].sum(),
    )
    return df
