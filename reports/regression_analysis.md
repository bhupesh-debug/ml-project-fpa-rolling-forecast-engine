# Econometric & Statistical Regression Analysis: FP&A Rolling Forecast Engine

## 1. Econometric Specification
To quantify the statistical relationship between business drivers and realized monthly revenue, we estimated an Ordinary Least Squares (OLS) specification using HC3 heteroskedasticity-consistent robust standard errors:

$$\text{Revenue}_{i, t+1} = \beta_0 + \beta_1 \text{rev\_lag0}_{i, t} + \beta_2 \text{same\_month\_last\_year}_{i, t} + \beta_3 \text{sales\_headcount}_{i, t} + \beta_4 \text{marketing\_spend}_{i, t} + \beta_5 \text{price\_index}_{i, t} + \beta_6 \text{roll3}_{i, t} + \epsilon_{i, t+1}$$

---

## 2. Statistical Estimation Summary

| Variable | Coefficient | Std. Error (HC3) | t-Statistic | p-Value | 95% Confidence Interval | VIF |
|---|---|---|---|---|---|---|
| **Intercept** | -0.210 | 1.744 | -0.120 | 0.904 | [-3.629, 3.209] | N/A |
| **`rev_lag0`** | +0.928 | 0.080 | 11.562 | $< 0.0001$ | [+0.771, +1.085] | 72.17 |
| **`same_month_last_year`** | +0.485 | 0.044 | 11.072 | $< 0.0001$ | [+0.399, +0.571] | 19.56 |
| **`sales_headcount_now`** | -0.030 | 0.011 | -2.840 | 0.0045 | [-0.051, -0.009] | 1.42 |
| **`marketing_spend_now`** | -0.018 | 0.142 | -0.129 | 0.8970 | [-0.296, +0.259] | 1.27 |
| **`price_index_now`** | +2.140 | 1.630 | 1.313 | 0.1892 | [-1.055, +5.334] | 1.34 |
| **`roll3`** | -0.384 | 0.054 | -7.143 | $< 0.0001$ | [-0.489, -0.279] | 35.86 |

### Overall Regression Diagnostics
- **Observations ($N$)**: 480 panel periods
- **R-squared**: 0.9791 (97.91% of variance explained)
- **Adjusted R-squared**: 0.9788
- **F-statistic**: 3,250.01 ($p < 0.0001$)

---

## 3. Methodological Interpretations & Caveats

### Multicollinearity in Time Series (VIF)
- The high VIF for `rev_lag0` (72.17) and `roll3` (35.86) reflects natural autoregressive colinearity common in panel time-series data.
- When lagged revenue is present, the static partial elasticity of commercial drivers reflects short-run marginal adjustments rather than total macro impact.
- Regularized estimation (Ridge with $\alpha=10.0$ and Lasso with $\alpha=0.1$) verified that the predictive stability remains robust across all rolling origins, delivering 0.044–0.045 WAPE at $h=1$.

### Association vs. Causation
- **Critical Caveat**: These regression coefficients reflect observational statistical associations in historical data. They do not constitute structural causal estimates.
- Increasing marketing spend or hiring additional sales reps will not automatically yield higher revenue unless underlying market demand and execution capacity are maintained.
