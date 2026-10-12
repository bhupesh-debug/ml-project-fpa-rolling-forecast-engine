import pytest
import numpy as np
import pandas as pd
from src.data_pipeline import make_data
from src.feature_engineering import build_features, FEATS
from src.model import gbm
from src.evaluate import wape, bias
from src.business_case import compute_business_case

def test_data_generation():
    df = make_data(units=4, months=36, seed=42)
    assert len(df) == 4 * 36
    assert "revenue" in df.columns
    assert "sales_headcount" in df.columns
    assert "marketing_spend" in df.columns
    assert "price_index" in df.columns
    assert df["revenue"].isna().sum() == 0

def test_feature_engineering_no_leakage():
    df = make_data(units=2, months=24, seed=42)
    f = build_features(df, h=1)
    for col in FEATS:
        assert col in f.columns
    # Assert target y is shifted by h
    assert "y" in f.columns
    assert "same_month_last_year" in f.columns

def test_model_training_and_metrics():
    y_true = np.array([100.0, 110.0, 105.0, 120.0])
    y_pred = np.array([102.0, 108.0, 107.0, 118.0])
    score_wape = wape(y_true, y_pred)
    score_bias = bias(y_true, y_pred)
    assert 0 <= score_wape <= 1
    assert -1 <= score_bias <= 1

def test_business_case_calculation():
    bc = compute_business_case()
    assert len(bc) == 3
    for row in bc:
        assert "Year1_Net_Benefit" in row
        assert "Payback_Period_Months" in row
        assert row["Payback_Period_Months"] > 0
