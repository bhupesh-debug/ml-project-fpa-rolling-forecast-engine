from sklearn.ensemble import HistGradientBoostingRegressor as H
def gbm(): return H(loss="absolute_error",max_depth=4,learning_rate=0.06,max_iter=250,random_state=3)
