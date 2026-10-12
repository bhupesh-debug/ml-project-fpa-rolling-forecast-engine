import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    NAVY = RGBColor(15, 34, 64)
    SLATE = RGBColor(70, 80, 95)
    DARK = RGBColor(30, 41, 59)
    WHITE = RGBColor(255, 255, 255)
    ACCENT_BLUE = RGBColor(30, 115, 190)
    LIGHT_BG = RGBColor(245, 247, 250)
    
    slides_data = [
        {
            "title": "FP&A Rolling Forecast Engine",
            "subtitle": "Driver-Based Machine Learning Benchmarked Against Corporate Baselines\nExecutive Presentation | Bhupesh Chandra Dimri | bhupesh7cd@gmail.com",
            "is_cover": True
        },
        {
            "title": "Executive Summary & Core Business Dilemma",
            "bullets": [
                "The Business Dilemma: Traditional corporate budget cycles rely on static annual budgets or naive run-rate forecasts, creating multi-million-dollar inventory and liquidity mismatches.",
                "The Core Finding: Machine learning (driver-based GBM) dramatically reduces 1-month forecast error to 6.2% WAPE vs 10.5% for Seasonal Naive (a 41% relative error reduction).",
                "Horizon Decay Reality: By 3 months ahead, simple seasonal naive converges to 10.5% while driver GBM drifts to 11.7% WAPE due to compounding driver uncertainty.",
                "Strategic Solution: A hybrid forecasting engine deploying pure Driver GBM for 1-month operational plans, blending 50/50 at 2 months, and anchoring to seasonal baselines for 3+ months.",
                "Financial Return: Year-1 Net Benefit of $2.45M (Base Case) from working capital optimization and avoided expediting fees, with payback achieved in 1.2 months."
            ]
        },
        {
            "title": "Time-Series Structure & Driver Architecture",
            "bullets": [
                "Dataset Architecture: 8 autonomous Business Units tracked across 72 monthly periods (576 panel observations).",
                "Key Leading Drivers: Sales Headcount (FTEs), Marketing Campaign Spend ($k), and Sector Price Index.",
                "Complex Dynamics Modeled: Underlying compound monthly growth (0.2% - 1.2%), annual seasonality cycles, idiosyncratic white noise, and a simulated 4-month severe demand shock.",
                "Strict Information Boundary: Feature engineering enforces strict lag alignment; driver metrics are lagged so zero lookahead information contaminates historical origins.",
                "Panel Heterogeneity: Baseline scales range from $8M to $30M monthly across business units, requiring normalized feature representations."
            ]
        },
        {
            "title": "Econometric & Statistical Regression Findings",
            "bullets": [
                "OLS Explanatory Model: Statistically significant driver relationships with R-squared of 0.984 across panel history.",
                "Sales Headcount Elasticity: Positive significant coefficient (p < 0.001); each additional commercial FTE adds ~$84k in incremental monthly revenue.",
                "Marketing Spend Elasticity: Robust positive return; marketing multiplier exhibits diminishing marginal returns above 1.5x baseline.",
                "Autoregressive Persistence: Prior month revenue (rev_lag0) and same-month last year explain 88% of baseline variance, confirming strong autoregression.",
                "Multicollinearity Diagnostics: Variance Inflation Factor (VIF) controlled below 5.0 for key drivers; regularized Ridge/Lasso validate coefficient stability."
            ]
        },
        {
            "title": "Rolling-Origin Backtest: 9-Origin Fair Benchmark",
            "bullets": [
                "Backtest Rigor: 9 sequential rolling origins (months 48 to 64 in increments of 2), preventing any future target leakage.",
                "1-Month Horizon Performance: Driver GBM achieves 0.062 WAPE (-1.6% bias) vs Seasonal Naive 0.105 (-10.4% bias) and Trend Naive 0.117 (-1.2% bias).",
                "2-Month Horizon Performance: Driver GBM achieves 0.092 WAPE (-1.4% bias) vs Seasonal Naive 0.106 (-10.5% bias) and Trend Naive 0.119 (-1.7% bias).",
                "3-Month Horizon Performance: Driver GBM reaches 0.117 WAPE vs Seasonal Naive 0.105 and Trend Naive 0.127.",
                "Bias Diagnostics: Seasonal Naive exhibits severe negative bias (-10.4%) because it systematically fails to account for secular corporate growth."
            ]
        },
        {
            "title": "Multi-Scenario Stress Testing & Sensitivity Analysis",
            "bullets": [
                "Commercial Headcount Shock (+/-20%): Portfolio monthly revenue shifts by +$8.4M / -$8.1M, validating commercial capacity as the core scale driver.",
                "Marketing Budget Sensitivity (+/-50%): Drives a +$6.2M / -$6.0M revenue swing across business units.",
                "Systemic Demand Shock (-18% Contraction): Model captures sudden volume drop within 1 period, outperforming naive seasonal models which lag by 12 months.",
                "Delayed Driver Reporting Simulation: Simulating a 1-month lag in ERP driver feeds degrades WAPE by only 0.8 percentage points, proving operational robustness.",
                "Optimal Horizon Blending: 80% GBM / 20% Seasonal at Month 1 (0.061 WAPE); 50/50 blend at Month 2 (0.088 WAPE); 30% GBM / 70% Seasonal at Month 3 (0.101 WAPE)."
            ]
        },
        {
            "title": "Monte Carlo Uncertainty Quantification (N=5,000 Runs)",
            "bullets": [
                "Stochastic Simulation Framework: 5,000 Monte Carlo iterations modeling driver shocks and residual forecast error variance.",
                "Portfolio Revenue Distribution: Expected monthly median of $198.4M across the 8 business units.",
                "Downside Tail Risk (P05): Severe downside revenue realisations indicate a minimum expected floor of $184.2M.",
                "Upside Potential (P95): Favorable macro and commercial execution upside reaches $213.1M.",
                "Value-at-Risk (VaR 95): Corporate FP&A must budget for an operational revenue variance corridor of +/-$14.2M relative to the baseline."
            ]
        },
        {
            "title": "Corporate Finance Business Case & ROI",
            "bullets": [
                "Working Capital Optimization: Reducing forecast error from 10.5% to 6.2% liberates $2.10M in safety stock buffers annually.",
                "Supply Chain Expediting Reduction: Eliminates $850k in premium freight and last-minute procurement expediting costs.",
                "FP&A Automation Savings: 1,200 hours of manual spreadsheet compilation converted to high-value variance analysis ($120k value).",
                "Cost Structure: $240,000 initial engineering implementation + $60,000 annual cloud/monitoring maintenance.",
                "Financial Returns: Year-1 Net Benefit of $2.45M, Payback in 1.2 Months, 3-Year NPV of $6.24M, and 2,600% 3-year ROI."
            ]
        },
        {
            "title": "FP&A Operational Target Architecture & Close Workflow",
            "bullets": [
                "Day -3 Pre-Close: Automated ETL ingestion of marketing CRM pipelines, sales headcount roster, and pricing indices.",
                "Day 0 Close Night: Rolling origin evaluation and automated forecast inference generation across 1-, 2-, and 3-month horizons.",
                "Day +1 Finance Review: FP&A Directors review unit-level ML predictions with driver contribution waterfalls and confidence bands.",
                "Day +2 Executive Consensus: Implementation of hybrid blending rules (near-term driver ML + medium-term seasonal baseline).",
                "Day +3 ERP Integration: Push final rolling forecasts into SAP / Oracle Hyperion GL for procurement and inventory scheduling."
            ]
        },
        {
            "title": "Model Governance, Controls & Implementation Roadmap",
            "bullets": [
                "Phase 1 (Weeks 1-4): Production data pipeline deployment, automated ERP ingestion, and historical baseline validation.",
                "Phase 2 (Weeks 5-8): Parallel run alongside existing spreadsheet forecast with shadow variance attribution.",
                "Phase 3 (Weeks 9-12): FP&A training, UAT sign-off, executive dashboard launch, and automated monthly drift monitoring.",
                "Model Risk Management: Quarterly recalibration trigger if WAPE exceeds 8.5% or forecast bias exceeds +/-3.0% for two consecutive cycles.",
                "Audit Trail: Complete immutability of training origin datasets and model artifacts logged with Git SHA and pipeline execution metadata."
            ]
        }
    ]
    
    for s_idx, data in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)
        
        # Background
        bg = slide.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(7.5)) # 1 is msoShapeRectangle
        bg.fill.solid()
        bg.fill.fore_color.rgb = WHITE if not data.get("is_cover") else NAVY
        bg.line.fill.background()
        
        if data.get("is_cover"):
            # Cover Slide
            title_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.0))
            tf = title_box.text_frame
            tf.word_wrap = True
            
            p = tf.paragraphs[0]
            p.text = data["title"]
            p.font.size = Pt(44)
            p.font.bold = True
            p.font.color.rgb = WHITE
            
            p2 = tf.add_paragraph()
            p2.text = data["subtitle"]
            p2.font.size = Pt(20)
            p2.font.color.rgb = RGBColor(200, 215, 235)
            p2.space_before = Pt(24)
        else:
            # Header banner
            header = slide.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(1.1))
            header.fill.solid()
            header.fill.fore_color.rgb = NAVY
            header.line.fill.background()
            
            # Header text
            title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.2), Inches(11.7), Inches(0.8))
            tf = title_box.text_frame
            p = tf.paragraphs[0]
            p.text = data["title"]
            p.font.size = Pt(26)
            p.font.bold = True
            p.font.color.rgb = WHITE
            
            # Subtitle bar
            sub_bar = slide.shapes.add_shape(1, 0, Inches(1.1), Inches(13.333), Inches(0.1))
            sub_bar.fill.solid()
            sub_bar.fill.fore_color.rgb = ACCENT_BLUE
            sub_bar.line.fill.background()
            
            # Content Box
            content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4))
            tf_content = content_box.text_frame
            tf_content.word_wrap = True
            
            for b_idx, bullet in enumerate(data.get("bullets", [])):
                p_bullet = tf_content.paragraphs[0] if b_idx == 0 else tf_content.add_paragraph()
                p_bullet.text = bullet
                p_bullet.font.size = Pt(15)
                p_bullet.font.color.rgb = DARK
                p_bullet.space_before = Pt(14)
                p_bullet.level = 0
                
            # Footer
            footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.4))
            tf_f = footer_box.text_frame
            pf = tf_f.paragraphs[0]
            pf.text = f"FP&A Rolling Forecast Engine | Confidential & Proprietary | Slide {s_idx + 1} of {len(slides_data)}"
            pf.font.size = Pt(10)
            pf.font.color.rgb = SLATE
            
    os.makedirs("slides", exist_ok=True)
    prs.save("slides/project_deck.pptx")
    print("Project 2 presentation saved to slides/project_deck.pptx")

if __name__ == "__main__":
    create_presentation()
