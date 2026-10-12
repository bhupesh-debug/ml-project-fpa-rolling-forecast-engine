# Model Governance, Internal Controls & Monitoring Framework: Project 2 (FP&A Rolling Forecast Engine)

## 1. Regulatory & Governance Framework
This governance framework aligns with Federal Reserve SR 11-7 / OCC 2011-12 standards on Model Risk Management (MRM) and corporate financial reporting controls (SOX Section 404).

---

## 2. Model Lifecycle & Change Management

### Model Inventory & Tier Classification
- **Model ID**: `MRM-FPA-002`
- **Model Category**: Corporate Financial Planning & Revenue Forecasting
- **Risk Tier**: **Tier 2 (Medium-High Impact)** — Informs revenue expectations, working capital commitments, and executive board presentations, but subject to managerial review prior to external financial release.

### Change Approval Matrix
| Change Type | Validation Requirement | Approval Authority |
|---|---|---|
| Pipeline Bug Fix / Data Schema Patch | Unit tests pass, backtest regression verified | Lead ML Engineer |
| Driver Feature Addition / Transformation | Full 9-origin backtest, VIF check, WAPE improvement >0.5% | Lead Data Scientist & FP&A Director |
| Model Architecture Change (e.g., Deep Learning / Prophet) | Parallel 3-cycle shadow run, SR 11-7 validation report | VP Financial Planning & Model Risk Officer |

---

## 3. Operational Close Calendar & Workflow Controls

```
  [Day -3: Ingestion]   -->   [Day 0: Inference]   -->   [Day +1: FP&A Review]  -->  [Day +2: Consensus]  -->  [Day +3: ERP Push]
  - HRIS Headcount            - ML Execution             - Unit Waterfalls           - Hybrid Blending         - SAP / Hyperion GL
  - CRM Pipelines             - Rolling Horizons         - Variance Attribution      - Executive Sign-off      - Supply Chain Run
  - ERP GL Ledger             - Uncertainty Bands        - Override Logs             - Board Summary           - Working Capital Sizing
```

### Mandatory Control Gates
1. **Gate 1: Input Integrity Validation**:
   - Zero missing entity keys or timestamps.
   - Headcount numbers cross-reconciled against payroll active roster (+/-0.5% tolerance).
   - Marketing spend validated against approved PO accruals.
2. **Gate 2: Plausibility Bounds Check**:
   - Automated assertion that forecasted revenue falls within $[-25\%, +35\%]$ of 3-month rolling trailing average (`roll3`).
   - Forecasts outside this corridor trigger an immediate `ANOMALY_ESCALATION` flag requiring manual variance explanation.
3. **Gate 3: Override Governance**:
   - Any manual executive override exceeding \$1.0M or 5% of model prediction requires documented rationale and dual sign-off (Business Unit VP + Corporate FP&A VP).

---

## 4. Ongoing Model Performance Monitoring & Trigger Thresholds

| Metric | Normal Operating Range | Warning Alert Trigger | Critical Model Retirement Trigger |
|---|---|---|---|
| **1-Month Horizon WAPE** | $< 0.075$ | $0.075 - 0.090$ | $> 0.090$ for 2 consecutive cycles |
| **Forecast Bias** | $-3.0\% \text{ to } +3.0\%$ | $|\text{Bias}| > 4.0\%$ | $|\text{Bias}| > 6.0\%$ |
| **Driver Data Freshness** | Lag $\le 3$ days post-close | Lag $> 5$ days | Lag $> 10$ days |
| **Population Drift (PSI)** | $\text{PSI} < 0.10$ | $0.10 \le \text{PSI} < 0.25$ | $\text{PSI} \ge 0.25$ |

### Remediation Protocol
- If a Warning Alert fires: Issue diagnostic report within 48 hours evaluating whether driver shock or macro disruption occurred.
- If a Critical Trigger fires: Revert immediately to fallback **Seasonal Naive Baseline** while the data science team retrains and validates updated model parameters.
