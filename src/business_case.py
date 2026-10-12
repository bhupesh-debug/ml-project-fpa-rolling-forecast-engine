import os
import pandas as pd

def compute_business_case():
    """
    Computes rigorous corporate finance business case for FP&A Rolling Forecast Engine:
    - 3 Scenarios: Conservative, Base, Upside
    - Avoided inventory buffers / working capital misallocation
    - Reduced emergency supply chain expediting costs
    - FP&A analyst labor automation hours
    - Implementation costs, recurring costs, Year-1 Net Benefit, 3-Year NPV (10% discount), Payback Period
    """
    os.makedirs("reports", exist_ok=True)
    
    scenarios = {
        "Conservative": {
            "error_reduction_pct": 2.2, # percentage points WAPE improvement
            "working_capital_savings": 1100000,
            "expediting_cost_reduction": 450000,
            "analyst_hours_saved": 850,
            "analyst_rate_per_hour": 100,
            "implementation_cost": 260000,
            "annual_maintenance_cost": 65000
        },
        "Base": {
            "error_reduction_pct": 3.8,
            "working_capital_savings": 2100000,
            "expediting_cost_reduction": 850000,
            "analyst_hours_saved": 1200,
            "analyst_rate_per_hour": 100,
            "implementation_cost": 240000,
            "annual_maintenance_cost": 60000
        },
        "Upside": {
            "error_reduction_pct": 4.5,
            "working_capital_savings": 3200000,
            "expediting_cost_reduction": 1400000,
            "analyst_hours_saved": 1500,
            "analyst_rate_per_hour": 100,
            "implementation_cost": 220000,
            "annual_maintenance_cost": 55000
        }
    }
    
    rows = []
    discount_rate = 0.10
    
    for name, s in scenarios.items():
        labor_benefit = s["analyst_hours_saved"] * s["analyst_rate_per_hour"]
        total_annual_benefit = s["working_capital_savings"] + s["expediting_cost_reduction"] + labor_benefit
        capex = s["implementation_cost"]
        opex = s["annual_maintenance_cost"]
        
        net_yr1 = total_annual_benefit - capex - opex
        net_yr2 = total_annual_benefit - opex
        net_yr3 = total_annual_benefit - opex
        
        npv_3yr = -capex + (net_yr1 + capex)/(1 + discount_rate) + net_yr2/((1 + discount_rate)**2) + net_yr3/((1 + discount_rate)**3)
        payback_months = (capex / (total_annual_benefit - opex)) * 12
        roi_3yr = (npv_3yr / capex) * 100
        
        rows.append({
            "Scenario": name,
            "WAPE_Improvement_Pts": s["error_reduction_pct"],
            "Working_Capital_Optimization": f"${s['working_capital_savings']:,.0f}",
            "Expediting_Cost_Savings": f"${s['expediting_cost_reduction']:,.0f}",
            "Analyst_Labor_Savings": f"${labor_benefit:,.0f}",
            "Total_Annual_Benefit": f"${total_annual_benefit:,.0f}",
            "Implementation_Cost": f"${capex:,.0f}",
            "Annual_Maintenance_Cost": f"${opex:,.0f}",
            "Year1_Net_Benefit": f"${net_yr1:,.0f}",
            "Payback_Period_Months": round(payback_months, 1),
            "Three_Year_NPV": f"${npv_3yr:,.0f}",
            "ROI_3Year_Pct": f"{round(roi_3yr, 0)}%"
        })
        
    df_bc = pd.DataFrame(rows)
    df_bc.to_csv("reports/business_case_table.csv", index=False)
    return df_bc.to_dict(orient="records")
