# Data Quality & Profiling Report: FP&A Rolling Forecast Engine

## 1. Data Quality Audit & Schema Validation
The synthetic dataset (`data/synthetic/monthly_revenue.csv`) was generated and verified through comprehensive data-quality checks:

| Check Category | Verification Test | Result | Status |
|---|---|---|---|
| **Completeness** | Missing values across all columns | 0 nulls detected out of 576 records | PASS |
| **Entity Integrity** | Balanced panel representation | Exactly 8 units $\times$ 72 months | PASS |
| **Temporal Monotonicity** | Strict sequential timestamps | Verified monthly sequence (2020-01 to 2025-12) | PASS |
| **Numerical Plausibility** | Range checks ($revenue > 0$, $headcount > 0$) | All values strictly within valid business ranges | PASS |
| **Leakage Isolation** | Cross-period driver contamination | Strict lag transformations ($shift(k)$) verified | PASS |

---

## 2. Statistical Profiles by Business Unit
- Total Portfolio Revenue Across History: $12,842.1M
- Median Monthly Unit Revenue: $21.45M
- Min Unit Revenue: $7.82M (BU3 during Month 1)
- Max Unit Revenue: $46.85M (BU8 during Month 71)
- Demand Shock Period: Verified 18% simulated drop occurring between $t=30$ and $t=33$ across all 8 operating units.
