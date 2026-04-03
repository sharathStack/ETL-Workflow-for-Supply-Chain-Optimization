"""
main.py — Supply Chain ETL & Analytics Pipeline entry point
"""
import logging, time, os
import config
from extractor   import extract_shipments, extract_inventory
from transformer import transform_shipments, transform_inventory
from loader      import load
from analytics   import run_analytics
from dashboard   import plot

logging.basicConfig(level=config.LOG_LEVEL,
                    format=config.LOG_FORMAT,
                    datefmt=config.LOG_DATE_FMT)


def main():
    print("=" * 55)
    print("  SUPPLY CHAIN ETL & ANALYTICS PIPELINE")
    print("=" * 55)
    t0 = time.time()

    ships_raw = extract_shipments()
    inv_raw   = extract_inventory()

    ships = transform_shipments(ships_raw)
    inv   = transform_inventory(inv_raw)

    conn = load(ships, inv)
    run_analytics(conn)
    conn.close()

    print("\n[5] Generating dashboard...")
    plot(ships, inv)

    print(f"\n  Pipeline complete in {time.time()-t0:.2f}s")
    print(f"  DB → {os.path.abspath(config.DB_PATH)}")
    print("\n  Done ✓")


if __name__ == "__main__":
    main()
