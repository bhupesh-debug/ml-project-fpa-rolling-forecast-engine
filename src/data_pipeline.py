import numpy as np, pandas as pd
def make_data(units=8, months=72, seed=3):
    """Synthetic monthly revenue by business unit with drivers (sales headcount, marketing spend, price index)."""
    r=np.random.default_rng(seed); rows=[]; idx=pd.period_range("2020-01",periods=months,freq="M")
    for u in range(units):
        base=r.uniform(8,30); g=r.uniform(.002,.012); amp=r.uniform(.05,.25); ph=r.uniform(0,6.28)
        hc=np.cumsum(r.normal(.15,.6,months))+r.integers(20,60); mk=np.clip(r.normal(1,.25,months),.3,2)*r.uniform(.5,2); pr=1+np.cumsum(r.normal(.002,.004,months))
        for t in range(months):
            seas=1+amp*np.sin(2*np.pi*t/12+ph); shock=-.18 if 30<=t<=33 else 0
            rev=base*(1+g)**t*seas*(1+.004*(hc[t]-hc[0]))*(1+.05*(mk[t]-1))*pr[t]*(1+shock)*(1+r.normal(0,.03))
            rows.append({"unit":f"BU{u+1}","month":idx[t].to_timestamp(),"t":t,"revenue":round(rev,2),"sales_headcount":round(hc[t],1),"marketing_spend":round(mk[t],3),"price_index":round(pr[t],4)})
    return pd.DataFrame(rows)
