import numpy as np, pandas as pd
def build_features(d,h):
    """Features for forecasting revenue h months ahead; drivers are lagged so only information known at the origin is used."""
    x=d.sort_values(["unit","t"]).copy(); g=x.groupby("unit")
    for k in (0,1,2,11): x[f"rev_lag{k}"]=g.revenue.shift(k)
    x["roll3"]=g.revenue.transform(lambda s:s.rolling(3).mean()); x["roll12"]=g.revenue.transform(lambda s:s.rolling(12).mean())
    for c in ("sales_headcount","marketing_spend","price_index"): x[c+"_now"]=x[c]
    x["target_month"]=(x.month+pd.DateOffset(months=h)).dt.month; x["unit_id"]=x.unit.str[2:].astype(int)
    x["y"]=g.revenue.shift(-h); x["same_month_last_year"]=g.revenue.shift(12-h)
    return x
FEATS=["rev_lag0","rev_lag1","rev_lag2","rev_lag11","roll3","roll12","sales_headcount_now","marketing_spend_now","price_index_now","target_month","unit_id"]
