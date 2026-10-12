# Question-and-Answer Register: FP&A Rolling Forecast Engine

## Overview
This register records every explicit business, statistical, and operational question formulated for Project 2, supported by verified numerical evidence, backtest metrics, simulation results, and executive recommendations.

---

### Q-FPA-001: Which forecasting method performs best at each horizon?
- **Direct Answer**:
  - **1-Month Ahead**: Driver GBM performs best (0.062 WAPE), and a hybrid 80% GBM / 20% Seasonal blend reaches 0.061 WAPE.
  - **2-Months Ahead**: Driver GBM performs best (0.092 WAPE), and a hybrid 60% GBM / 40% Seasonal blend reaches 0.078 WAPE.
  - **3-Months Ahead**: Seasonal Naive (0.105 WAPE) outperforms pure Driver GBM (0.117 WAPE); however, an optimal **40% GBM / 60% Seasonal Naive blend achieves 0.089 WAPE**, beating both single methods.
- **Supporting Analysis**: 9-origin rolling backtest across 8 business units ($t=48$ to $64$).
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/model_report.md` Section 2.

---

### Q-FPA-002: Does machine learning consistently outperform simple baselines?
- **Direct Answer**: Machine learning consistently and decisively outperforms simple baselines at 1-month and 2-month horizons (reducing error by 41.0% and 13.2% respectively). At 3 months, pure machine learning degrades due to compounding driver uncertainty, requiring blending with seasonal anchors.
- **Supporting Analysis**: Backtest metrics demonstrate that at $h=1$, Driver GBM achieves 0.062 WAPE vs 0.105 for Seasonal Naive. At $h=3$, pure GBM drops to 0.117 WAPE.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/model_report.md` Section 2.

---

### Q-FPA-003: How much forecast error is reduced?
- **Direct Answer**: At the crucial 1-month horizon, forecast error is reduced by **4.3 percentage points on WAPE** (from 10.5% down to 6.2%), representing a **41.0% relative error reduction**. At 2 months, error drops by 1.4 percentage points (from 10.6% to 9.2%).
- **Supporting Analysis**: Aggregate dollar-weighted WAPE across 72 evaluations per horizon.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/results.json`.

---

### Q-FPA-004: Is the model systematically over- or under-forecasting?
- **Direct Answer**: No. The Driver GBM exhibits near-zero bias (-1.5% at 1m, -1.3% at 2m). In sharp contrast, the traditional **Seasonal Naive baseline exhibits severe negative bias (-10.4% to -10.5%)**, because it fails to capture ongoing corporate growth.
- **Supporting Analysis**: Empirical bias calculations across 9 rolling origins.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/model_report.md` Section 2.

---

### Q-FPA-005: Which business units are hardest to forecast?
- **Direct Answer**: Business Units with higher seasonal amplitude and lower base revenue (BU2 and BU6) exhibited the highest absolute forecast variance. Stable large-scale units (BU1 and BU5) achieved the lowest WAPE (<4.2% under regularized linear models).
- **Supporting Analysis**: Divisional cross-sectional error breakdowns across the 8 business units.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/model_report.md` Section 4.

---

### Q-FPA-006: Which business drivers are most useful?
- **Direct Answer**: Prior revenue momentum (`rev_lag0` and `roll3`) and historical annual seasonality (`same_month_last_year`) explain over 88% of variance. Commercial headcount (`sales_headcount`) provides the primary structural capacity signal, while pricing index captures inflationary pass-through.
- **Supporting Analysis**: OLS regression ($R^2 = 0.9791$) and feature attribution analysis.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/regression_analysis.md` Section 2.

---

### Q-FPA-007: When should forecasts be blended?
- **Direct Answer**: Forecasts should always be blended for horizons beyond 1 month. At 2 months, a 60% GBM / 40% Seasonal Naive blend reduces WAPE from 0.092 to 0.078. At 3 months, a 40% GBM / 60% Seasonal Naive blend reduces WAPE from 0.117 to 0.089.
- **Supporting Analysis**: Grid search across blending weights $w \in [0.0, 1.0]$.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/simulation_report.md` Section 3.

---

### Q-FPA-008: How should FP&A use prediction intervals and downside scenarios?
- **Direct Answer**: FP&A should utilize the 5,000-run Monte Carlo distribution to establish the **P05 downside scenario ($241.91M)** as the hard liquidity floor for treasury cash-buffer sizing, while using the median forecast ($247.38M) for operational procurement and inventory commits.
- **Supporting Analysis**: 5,000-iteration stochastic Monte Carlo simulation.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/simulation_report.md` Section 4.
