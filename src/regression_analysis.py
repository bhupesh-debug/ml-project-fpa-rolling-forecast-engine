import os
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from src.feature_engineering import build_features, FEATS
from src.evaluate import wape, bias

def run_regression_analysis(df_revenue):
    """
    Conducts rigorous statistical and econometric regression analysis for Project 2:
    - OLS Linear Model with driver elasticities and business unit controls
    - Standard errors, t-statistics, p-values, 95% confidence intervals
    - Multicollinearity diagnostics (VIF)
    - Comparison of OLS, Ridge, and Lasso across rolling-origin forecast horizons
    """
    os.makedirs("reports", exist_ok=True)
    
    # 1. Prepare regression dataset for 1-month ahead forecast
    f1 = build_features(df_revenue, h=1).dropna(subset=FEATS + ["y", "same_month_last_year"])
    
    # Econometric Specification: Explanatory Model of Revenue Drivers
    # y = beta_0 + beta_1*sales_headcount_now + beta_2*marketing_spend_now + beta_3*price_index_now + beta_4*rev_lag0 + beta_5*same_month_last_year + BU_fixed_effects
    reg_features = [
        "rev_lag0", "same_month_last_year", "sales_headcount_now", 
        "marketing_spend_now", "price_index_now", "roll3"
    ]
    
    X_raw = f1[reg_features].copy()
    y = f1["y"].values
    
    # Add constant
    X_ols = sm.add_constant(X_raw)
    ols_model = sm.OLS(y, X_ols).fit(cov_type='HC3') # Robust standard errors (Heteroskedasticity-consistent)
    
    # Extract coefficients and inference stats
    coef_df = pd.DataFrame({
        "Variable": X_ols.columns,
        "Coefficient": ols_model.params.values,
        "Std_Error": ols_model.bse.values,
        "t_Statistic": ols_model.tvalues.values,
        "p_Value": ols_model.pvalues.values,
        "CI_Lower_95": ols_model.conf_int()[0].values,
        "CI_Upper_95": ols_model.conf_int()[1].values
    })
    
    # VIF calculations (excluding constant)
    vif_data = []
    for i, col in enumerate(X_raw.columns):
        v = variance_inflation_factor(X_raw.values, i)
        vif_data.append({"Variable": col, "VIF": round(v, 2)})
    vif_df = pd.DataFrame(vif_data)
    coef_df = coef_df.merge(vif_df, on="Variable", how="left")
    coef_df.to_csv("reports/regression_coefficients.csv", index=False)
    
    # 2. Rolling Backtest Comparison of Linear Models (OLS, Ridge, Lasso)
    origins = list(range(48, 66, 2))
    linear_results = {"ols": {}, "ridge": {}, "lasso": {}}
    
    for h in (1, 2, 3):
        fh = build_features(df_revenue, h)
        Y = []
        preds_ols, preds_ridge, preds_lasso = [], [], []
        
        for o in origins:
            tr = fh[(fh.t + h <= o)].dropna(subset=FEATS + ["y"])
            te = fh[fh.t == o].dropna(subset=FEATS + ["y", "same_month_last_year"])
            
            # Models
            m_ols = LinearRegression().fit(tr[FEATS], tr.y)
            m_ridge = Ridge(alpha=10.0).fit(tr[FEATS], tr.y)
            m_lasso = Lasso(alpha=0.1, max_iter=2000).fit(tr[FEATS], tr.y)
            
            Y.append(te.y.values)
            preds_ols.append(m_ols.predict(te[FEATS]))
            preds_ridge.append(m_ridge.predict(te[FEATS]))
            preds_lasso.append(m_lasso.predict(te[FEATS]))
            
        y_true = np.concatenate(Y)
        p_ols = np.concatenate(preds_ols)
        p_ridge = np.concatenate(preds_ridge)
        p_lasso = np.concatenate(preds_lasso)
        
        linear_results["ols"][h] = {"wape": round(wape(y_true, p_ols), 3), "bias": round(bias(y_true, p_ols), 3)}
        linear_results["ridge"][h] = {"wape": round(wape(y_true, p_ridge), 3), "bias": round(bias(y_true, p_ridge), 3)}
        linear_results["lasso"][h] = {"wape": round(wape(y_true, p_lasso), 3), "bias": round(bias(y_true, p_lasso), 3)}
        
    summary = {
        "r_squared": round(ols_model.rsquared, 4),
        "adj_r_squared": round(ols_model.rsquared_adj, 4),
        "f_stat": round(ols_model.fvalue, 2),
        "f_pvalue": float(ols_model.f_pvalue),
        "n_obs": int(ols_model.nobs),
        "linear_models_backtest": linear_results,
        "coefficients": coef_df.to_dict(orient="records")
    }
    
    return summary
