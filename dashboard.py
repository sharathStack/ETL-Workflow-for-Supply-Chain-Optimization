"""
dashboard.py — 6-panel supply chain analytics dashboard
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import pandas as pd
import config

COLORS = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]


def plot(shipments: pd.DataFrame, inventory: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(18, 10))
    fig.suptitle("Supply Chain Analytics Dashboard", fontsize=14, fontweight="bold")
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.48, wspace=0.38)

    # ── 1. Delay rate by carrier ──────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    dr  = shipments.groupby("carrier")["delay_flag"].mean().sort_values(ascending=False)
    ax1.bar(dr.index, dr.values * 100, color=COLORS[0], alpha=0.85)
    ax1.set_title("Delay Rate by Carrier (%)", fontweight="bold")
    ax1.set_ylabel("%")
    ax1.tick_params(axis="x", rotation=20)
    for i, v in enumerate(dr.values * 100):
        ax1.text(i, v + 0.3, f"{v:.1f}%", ha="center", fontsize=8)

    # ── 2. Top routes by cost/km ──────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    top = (shipments.groupby("route")["cost_per_km"].mean()
           .sort_values(ascending=False).head(8))
    ax2.barh(top.index, top.values, color=COLORS[1], alpha=0.85)
    ax2.set_title("Top Routes by Cost/km", fontweight="bold")
    ax2.set_xlabel("Cost/km (₹)")
    ax2.invert_yaxis()

    # ── 3. Delay duration histogram ───────────────────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    delayed = shipments[shipments["delay_days"] > 0]["delay_days"]
    ax3.hist(delayed, bins=20, color=COLORS[2], alpha=0.85, edgecolor="white")
    ax3.set_title("Delay Duration Distribution (delayed only)", fontweight="bold")
    ax3.set_xlabel("Days delayed")
    ax3.set_ylabel("Count")

    # ── 4. Shipment status pie ────────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 0])
    sc  = shipments["status"].value_counts()
    ax4.pie(sc.values, labels=sc.index, autopct="%1.0f%%",
            colors=COLORS[:len(sc)], startangle=140)
    ax4.set_title("Shipment Status Mix", fontweight="bold")

    # ── 5. Inventory stock status ─────────────────────────────────────────────
    ax5 = fig.add_subplot(gs[1, 1])
    status_colors = {
        "Out of Stock": "#e74c3c", "Critical": "#f39c12",
        "Healthy": "#2ecc71", "Overstocked": "#3498db",
    }
    sc2 = inventory["stock_status"].value_counts()
    bar_cols = [status_colors.get(str(s), "#95a5a6") for s in sc2.index]
    ax5.bar(sc2.index.astype(str), sc2.values, color=bar_cols, alpha=0.85)
    ax5.set_title("Inventory Stock Status (# SKUs)", fontweight="bold")
    ax5.set_ylabel("# SKUs")
    ax5.tick_params(axis="x", rotation=15)

    # ── 6. Monthly shipping cost ──────────────────────────────────────────────
    ax6 = fig.add_subplot(gs[1, 2])
    monthly = (shipments.groupby("dispatch_month")["shipping_cost"]
               .sum().reset_index().sort_values("dispatch_month"))
    ax6.plot(monthly["dispatch_month"], monthly["shipping_cost"] / 1e6,
             marker="o", color=COLORS[4], linewidth=1.8)
    ax6.set_title("Monthly Shipping Cost (₹ M)", fontweight="bold")
    ax6.set_ylabel("Cost (₹ M)")
    ax6.tick_params(axis="x", rotation=40, labelsize=7)
    for i in range(0, len(monthly), 2):
        ax6.get_xticklabels()[i].set_visible(False) if i < len(ax6.get_xticklabels()) else None

    plt.tight_layout()
    plt.savefig(config.CHART_OUTPUT, dpi=config.CHART_DPI, bbox_inches="tight")
    plt.close()
    print(f"Dashboard saved → {config.CHART_OUTPUT}")
