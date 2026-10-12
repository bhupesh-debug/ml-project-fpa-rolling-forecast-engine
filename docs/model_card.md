# Model Card: Driver-Based FP&A Rolling Forecast Engine

## Model Details
- **Model Name**: Multi-Horizon Driver-Based Gradient Boosting Regressor (`driver_gbm`)
- **Version**: 2.0.0
- **Model Family**: HistGradientBoostingRegressor (LightGBM/HistGBM architecture)
- **Objective Loss**: Least Absolute Deviation (`loss="absolute_error"` / L1 norm) optimizing directly for Median Realization and Median Absolute Error (WAPE).
- **Hyperparameters**: `max_depth=4`, `learning_rate=0.06`, `max_iter=250`, `random_state=3`.
- **Developer / Maintainer**: Bhupesh Chandra Dimri (`bhupesh7cd@gmail.com`).

---

## Intended Use & Target Audience
- **Primary Use**: Automated monthly revenue forecasting across business units for Corporate FP&A, Treasury liquidity planning, and operational supply chain resource allocation.
- **Decision Context**: Generating baseline forecast trajectories for 1-, 2-, and 3-month forward horizons to support monthly financial closing and executive planning meetings.
- **Out of Scope**: Multi-year strategic planning (>12 months), customer-level transactional pricing, or high-frequency intraday demand forecasting.

---

## Benchmark Comparisons & Out-of-Sample Performance
Evaluated across a 9-origin rolling backtest ($t=48, 50, \dots, 64$) without lookahead leakage.

| Horizon | Model Architecture | WAPE | Forecast Bias | Error Reduction vs Seasonal Naive |
|---|---|---|---|---|
| **1-Month Ahead** | **Driver GBM** | **0.062** | **-1.6%** | **41.0% Error Reduction** |
| 1-Month Ahead | Trend-Adjusted Naive | 0.117 | -1.2% | -11.4% (Degradation) |
| 1-Month Ahead | Seasonal Naive | 0.105 | -10.4% | Benchmark Baseline |
| **2-Month Ahead** | **Driver GBM** | **0.092** | **-1.4%** | **13.2% Error Reduction** |
| 2-Month Ahead | Trend-Adjusted Naive | 0.119 | -1.7% | -12.3% (Degradation) |
| 2-Month Ahead | Seasonal Naive | 0.106 | -10.5% | Benchmark Baseline |
| **3-Month Ahead** | Driver GBM | 0.117 | -2.3% | -11.4% (Seasonal Naive preferred) |
| 3-Month Ahead | Trend-Adjusted Naive | 0.127 | -1.7% | -21.0% |
| **3-Month Ahead** | **Seasonal Naive** | **0.105** | **-10.4%** | **Benchmark Baseline (Optimal)** |

---

## Explainability & Feature Importance
The model relies heavily on:
1. `rev_lag0` & `roll3`: Autoregressive persistence anchors near-term operational momentum.
2. `sales_headcount_now`: Commercial sales capacity acts as the primary scale engine.
3. `marketing_spend_now`: Demand-generation catalyst with diminishing returns.
4. `price_index_now`: Inflationary and contractual pricing realisations.
5. `same_month_last_year` & `target_month`: Capture annual seasonality peaks and troughs.

---

## Ethical & Governance Considerations
- **Fairness & Bias**: Evaluated individually across all 8 business units to confirm the model does not disproportionately under-forecast specific divisions.
- **Synthetic Data Disclaimer**: Data was generated via calibrated synthetic stochastic processes. Production deployment requires shadow running on historical General Ledger data.
