import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
def wape(y,p): return float(np.abs(y-p).sum()/np.abs(y).sum())
def bias(y,p): return float((p-y).sum()/y.sum())
def chart(res,path):
    models=list(res.keys()); hs=sorted(next(iter(res.values())).keys()); w=.25; plt.figure(figsize=(7,3.6))
    for i,m in enumerate(models): plt.bar(np.arange(len(hs))+i*w,[res[m][h]["wape"] for h in hs],w,label=m)
    plt.xticks(np.arange(len(hs))+w,[f"{h}-month ahead" for h in hs]); plt.ylabel("WAPE (lower is better)"); plt.title("Rolling-origin backtest accuracy"); plt.legend(); plt.tight_layout(); plt.savefig(path,dpi=130); plt.close()
