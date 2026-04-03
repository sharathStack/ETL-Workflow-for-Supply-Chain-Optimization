"""
analytics.py — SQL KPI queries on the supply chain warehouse
"""
import sqlite3
import pandas as pd


QUERIES = {
    "Delay Rate by Carrier": """
        SELECT carrier,
               COUNT(*)                                         AS shipments,
               ROUND(100.0 * SUM(delay_flag) / COUNT(*), 1)    AS delay_rate_pct,
               ROUND(100.0 * SUM(sla_breach_flag)/COUNT(*), 1) AS sla_breach_pct,
               ROUND(AVG(delay_days), 2)                       AS avg_delay_days
        FROM fact_shipments
        GROUP BY carrier
        ORDER BY delay_rate_pct DESC;
    """,
    "Top 5 Most Expensive Routes (Cost/km)": """
        SELECT route,
               COUNT(*)                          AS shipments,
               ROUND(AVG(cost_per_km), 4)        AS avg_cost_per_km,
               ROUND(SUM(shipping_cost) / 1e3, 1)AS total_cost_k
        FROM fact_shipments
        WHERE cost_per_km IS NOT NULL
        GROUP BY route
        ORDER BY avg_cost_per_km DESC
        LIMIT 5;
    """,
    "Monthly Shipping Cost Trend": """
        SELECT dispatch_month,
               COUNT(*)                               AS shipments,
               ROUND(SUM(shipping_cost) / 1e6, 3)     AS cost_million
        FROM fact_shipments
        GROUP BY dispatch_month
        ORDER BY dispatch_month
        LIMIT 8;
    """,
    "Inventory Reorder Alerts": """
        SELECT warehouse,
               SUM(reorder_needed)                AS skus_to_reorder,
               ROUND(SUM(stock_value) / 1e3, 1)  AS total_stock_value_k
        FROM dim_inventory
        GROUP BY warehouse
        ORDER BY skus_to_reorder DESC;
    """,
}


def run_analytics(conn: sqlite3.Connection) -> None:
    print("\n" + "=" * 55)
    print("  SUPPLY CHAIN ANALYTICS — QUERY RESULTS")
    print("=" * 55)
    for title, sql in QUERIES.items():
        df = pd.read_sql(sql, conn)
        print(f"\n  ── {title} ──")
        print(df.to_string(index=False))
