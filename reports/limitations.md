# Limitations & Risk Register: FP&A Rolling Forecast Engine

## 1. Synthetic Data Disclaimer & External Validity
- **Synthetic Data Prototype**: All datasets in this repository are synthetic, constructed using parametric sine waves, trend exponentials, and Gaussian noise.
- **Limitation**: Real-world General Ledger revenues contain customer churn, contract renegotiations, currency exchange fluctuations, and accounting timing changes that may not follow smooth sinusoidal cycles.

---

## 2. Modeling Limitations & Methodological Risks
- **Driver Uncertainty Compounding**: At 3 months ahead, the model assumes drivers are known or stationary. In real deployments, future sales headcount and marketing spend are themselves forecasts subject to execution variance.
- **Non-Causal Associations**: Regression elasticities reflect observational correlations. Reallocating marketing budgets or hiring reps without commercial enablement will not mechanically guarantee revenue gains.
- **Extrapolation Risk**: Extreme macroeconomic shocks outside the historical training envelope (e.g., severe global stagflation) may require manual executive intervention and override protocols.
