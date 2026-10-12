# Data Dictionary: FP&A Rolling Forecast Engine

## Overview
This data dictionary documents the schema, operational definitions, data lineage, and statistical distributions for the synthetic dataset utilized in the FP&A Rolling Forecast Engine (`data/synthetic/monthly_revenue.csv`).

## Dataset Architecture
- **Entities**: 8 Autonomous Business Units (`BU1` through `BU8`).
- **Temporal Horizon**: 72 Monthly observation periods (`2020-01-01` to `2025-12-01`).
- **Total Records**: 576 entity-month observations.
- **Grain**: One record per business unit per calendar month.

---

## Schema Specifications

| Column Name | Data Type | Nullable | Source System | Business Definition | Typical Range |
|---|---|---|---|---|---|
| `unit` | String (Categorical) | No | SAP Master Data | Business Unit unique identifier (`BU1` to `BU8`). | Categorical (8 values) |
| `month` | Timestamp (YYYY-MM-01) | No | General Ledger (GL) | Calendar accounting month of reporting period. | 2020-01 to 2025-12 |
| `t` | Integer | No | Pipeline Index | Sequential integer time index ($t = 0, 1, \dots, 71$). | 0 to 71 |
| `revenue` | Float (Millions USD) | No | Financial Reporting (SAP/Hyperion) | Net recognized accounting revenue in Millions USD. | $6.50M – $48.20M |
| `sales_headcount` | Float | No | Workday / HRIS | Average active commercial sales representative FTE count during the period. | 18.0 – 85.0 FTEs |
| `marketing_spend` | Float (Millions USD) | No | Marketing Operations (Marketo) | Direct promotional and demand-generation marketing expenditure. | $0.25M – $3.80M |
| `price_index` | Float (Index Base=1.0) | No | Commercial Pricing Master | Realized net price index relative to initial period baseline. | 0.950 – 1.450 |

---

## Feature Engineering Lineage & Transformation Matrix

| Feature Symbol | Raw Precursor | Mathematical Formula | Purpose / Economic Rationale | Lookahead Safety |
|---|---|---|---|---|
| `rev_lag0` | `revenue` | $y_{i, t}$ | Immediate prior month revenue baseline. | Safe (Known at origin $t$) |
| `rev_lag1` | `revenue` | $y_{i, t-1}$ | Momentum indicator (2 months prior). | Safe (Known at origin $t-1$) |
| `rev_lag2` | `revenue` | $y_{i, t-2}$ | Quarter-end baseline anchor. | Safe (Known at origin $t-2$) |
| `rev_lag11` | `revenue` | $y_{i, t-11}$ | Same calendar month revenue from prior fiscal year. | Safe (Known at origin $t-11$) |
| `roll3` | `revenue` | $\frac{1}{3}\sum_{k=0}^2 y_{i, t-k}$ | 3-month trailing moving average smoothing noise. | Safe (Known at origin $t$) |
| `roll12` | `revenue` | $\frac{1}{12}\sum_{k=0}^{11} y_{i, t-k}$ | 12-month annual baseline run-rate. | Safe (Known at origin $t$) |
| `sales_headcount_now` | `sales_headcount` | $hc_{i, t}$ | Commercial capacity driver available at close. | Safe (Known at origin $t$) |
| `marketing_spend_now` | `marketing_spend` | $mk_{i, t}$ | Trailing promotional push driving lead pipelines. | Safe (Known at origin $t$) |
| `price_index_now` | `price_index` | $pr_{i, t}$ | Realized contractual pricing index. | Safe (Known at origin $t$) |
| `target_month` | `month` | $\text{Month}(t + h)$ | Cyclical month indicator (1-12) for seasonality. | Safe (Deterministic calendar) |
| `unit_id` | `unit` | $\text{Integer}(unit)$ | Categorical entity identifier. | Safe (Static entity) |
| `y` (Target) | `revenue` | $y_{i, t+h}$ | Forward realized revenue $h$ months ahead ($h \in \{1, 2, 3\}$). | Target (Masked during inference) |
| `same_month_last_year` | `revenue` | $y_{i, t+h-12}$ | Seasonal baseline anchor for evaluation. | Safe (Known at origin $t$) |
