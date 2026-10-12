import os
import json
import numpy as np
import pandas as pd
from src.data_pipeline import make_data
from src.feature_engineering import build_features, FEATS
from src.model import gbm
from src.evaluate import wape, bias, chart
from src.regression_analysis import run_regression_analysis
from src.simulation import run_fpa_simulations
from src.business_case import compute_business_case
from slides.generate_deck import create_presentation

def main():
    os.makedirs("data/synthetic", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("slides", exist_ok=True)

    # 1. Data generation
    df = make_data()
    df.to_csv("data/synthetic/monthly_revenue.csv", index=False)

    # 2. Rolling-origin backtest
    res = {"seasonal_naive": {}, "trend_adjusted_naive": {}, "driver_gbm": {}}
    origins = list(range(48, 66, 2)) # 9 rolling origins in the back half of history

    for h in (1, 2, 3):
        f = build_features(df, h)
        Y = []
        P = {k: [] for k in res}
        for o in origins:
            tr = f[(f.t + h <= o)].dropna(subset=FEATS + ["y"])
            te = f[f.t == o].dropna(subset=FEATS + ["y", "same_month_last_year"])
            m = gbm().fit(tr[FEATS], tr.y)
            Y.append(te.y.values)
            P["driver_gbm"].append(m.predict(te[FEATS]))
            P["seasonal_naive"].append(te.same_month_last_year.values)
            # Trend adjusted naive
            trend_ratio = (te.roll3 / f.loc[te.index, "rev_lag11"].replace(0, np.nan).fillna(1)).clip(0.7, 1.4)
            P["trend_adjusted_naive"].append((te.same_month_last_year * trend_ratio).values)

        y = np.concatenate(Y)
        for k in res:
            p = np.concatenate(P[k])
            res[k][h] = {"wape": round(wape(y, p), 3), "bias": round(bias(y, p), 3)}

    chart(res, "reports/backtest_wape.png")

    # 3. Econometric Regression Analysis
    reg_summary = run_regression_analysis(df)

    # 4. Multi-Scenario Simulations & 5,000-run Monte Carlo
    sim_summary = run_fpa_simulations(df, n_mc_runs=5000, seed=42)

    # 5. Financial Business Case
    bc_summary = compute_business_case()

    # 6. Generate Executive Slide Deck
    create_presentation()

    # 7. Compile Results JSON
    out = {
        "origins": len(origins),
        "units": int(df.unit.nunique()),
        "total_months": int(df.t.max() + 1),
        "backtest_results": {k: {str(h): v for h, v in r.items()} for k, r in res.items()},
        "regression": reg_summary,
        "simulations": sim_summary,
        "business_case": bc_summary
    }

    with open("reports/results.json", "w") as f_out:
        json.dump(out, f_out, indent=2)

    print(f"Project 2 pipeline executed successfully across {len(origins)} origins and {df.unit.nunique()} units.")
    print(f"Results written to reports/results.json")

if __name__ == "__main__":
    main()
