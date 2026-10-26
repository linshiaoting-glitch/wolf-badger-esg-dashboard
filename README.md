# Wolf & Badger — ESG Performance Dashboard

SAM 503 · ESG Analytics & Management · **Lab 4: Environmental Performance Dashboard**


An interactive Streamlit dashboard that tracks the carbon, energy, water, waste, social and governance performance of
**Wolf & Badger Ltd** (a UK online marketplace for independent fashion and lifestyle brands, and a Certified B Corp).
It also projects emissions pathways to 2035.

| | |
|---|---|
| **Audience** | Sustainability analysts who monitor and report ESG metrics |
| **Purpose** | Inform the Sustainability Director, who reports findings, risks and progress to the Board |
| **Time horizon** | FY2021 (first B Impact assessment) → 2035 (scenario projections) |
| **Reporting year** | FY2024 (calendar year) |

## Key questions answered
1. Is the footprint growing faster than the business? (absolute vs intensity)
2. What drives emissions, and how much of the change is real vs methodological?
3. Can W&B hit a credible 2030 Scope 3 target while growing ~15% a year? (scenario explorer)
4. Where are the disclosure gaps (energy, water, waste, workforce, board)?
5. Are social and governance practices improving?

## Dashboard tabs
| Tab | Content |
|---|---|
| 📌 Overview | KPI tiles, key findings, areas needing urgent attention |
| 🌍 Climate | Emissions by scope, Scope 3 by category, absolute vs intensity, restatement bridge, freight data-method split |
| 🔮 10-year scenarios | Sliders for growth, intensity improvement and target ambition; BAU vs scenario vs target path to 2035 |
| ⚡💧♻️ Energy · Water · Waste | Modelled electricity, renewable share, and explicit disclosure-gap cards |
| 🤝 Social & Governance | B Impact scores 2021 vs 2025, engagement, supply-chain due-diligence funnel, governance checklist |
| 🔎 Data quality | Lab 1 quality scores (accuracy, completeness, timeliness, consistency) and coverage by pillar |
| ✅ Recommendations | Five board-level actions |

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run in Google Colab
Open `notebooks/01_explore_wolf_badger_esg.ipynb` in Colab (File → Open notebook → GitHub). The notebook explores and
charts the same CSVs. To launch the app from Colab:
```python
!pip -q install streamlit plotly
!git clone https://github.com/linshiaoting-glitch/wolf-badger-esg-dashboard.git
%cd wolf-badger-esg-dashboard
!streamlit run app.py &>/content/log.txt &
!npx --yes localtunnel --port 8501
```

## Deploy (Streamlit Community Cloud, free)
1. Push this folder to a public GitHub repo (`linshiaoting-glitch/wolf-badger-esg-dashboard`).
2. Go to share.streamlit.io → **New app** → pick the repo, branch `main`, main file `app.py`.
3. Click **Deploy**. The app gets a public `*.streamlit.app` URL.

## Data (`data/`)
| File | Content | Source |
|---|---|---|
| `emissions_annual.csv` | Scope 1/2/3, totals, GMV, intensity, freight data method — FY2023 original, FY2023 restated, FY2024 | W&B Annual Impact Report 2024 (p.22), 2025 (p.21, 52–53) |
| `scope3_categories.csv` | Scope 3 by category (freight, digital, residual) | 2025 report p.24; residual calculated |
| `b_impact_scores.csv` | B Impact Assessment by impact area, 2021 vs 2025 | B Corp Impact Report 2023 p.5; 2025 report p.14; B Lab directory |
| `social_governance.csv` | Engagement, women in leadership, Happy Worker Guarantee, governance practices | 2024 & 2025 reports |
| `kpi_quality_lab1.csv` | 41 KPIs scored for data quality (Lab 1) | Lab 1 workbook |

## Methodology notes & limitations
- **All figures are self-reported; none is third-party assured.** Emissions are calculated by Greenly using the GHG Protocol, operational control approach.
- FY2023 was **restated** in the 2025 report (total 7,619 → 6,650 t). The dashboard uses restated values by default; a sidebar toggle shows the original.
- FY2024 freight emissions are 74% spend-based (vs 41% in FY2023), so the reported +55% growth partly reflects the method. The company's like-for-like estimate is ≈ +15%.
- Electricity use (≈145 MWh) is **modelled** by back-calculating from the reported location-based Scope 2 and the UK grid factor. Water and waste are **not disclosed**.
- The 2030 target is **illustrative**: W&B has not yet published a quantified Scope 3 target.
- Scenario projections are what-if tools, not forecasts.

## How this was built
Code was drafted with Claude as an AI coding assistant (prompt in `PROMPT.md`), then reviewed, tested and documented by the author.
