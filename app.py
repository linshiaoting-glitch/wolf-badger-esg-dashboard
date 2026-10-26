"""
Wolf & Badger — ESG Performance Dashboard (SAM 503 · Lab 4)

Audience : sustainability analysts → Sustainability Director → Board
Data     : Wolf & Badger Annual Impact Reports 2024 & 2025, B Corp Impact Report 2023,
           B Lab public directory, and the Lab 1 data-quality inventory (see data/ and README).
Run      : streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------- setup
st.set_page_config(page_title="Wolf & Badger ESG Dashboard", page_icon="🌿", layout="wide")

DATA = Path(__file__).parent / "data"
INK, MUTED = "#1F2A24", "#6B7770"
GREEN, SAGE, CLAY, SAND, SKY, RED = "#2F6B4F", "#8DB59E", "#C0703F", "#E2C792", "#4F7FA8", "#B54A3A"
LAYOUT = dict(template="simple_white", font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
              margin=dict(l=10, r=10, t=50, b=10), legend=dict(orientation="h", y=-0.18),
              hoverlabel=dict(bgcolor="white"))


@st.cache_data
def load():
    return (pd.read_csv(DATA / "emissions_annual.csv"), pd.read_csv(DATA / "scope3_categories.csv"),
            pd.read_csv(DATA / "b_impact_scores.csv"), pd.read_csv(DATA / "social_governance.csv"),
            pd.read_csv(DATA / "kpi_quality_lab1.csv"))


em, s3, bia, sg, kq = load()
latest = em[em.version == "Reported"].iloc[0]          # FY2024
base = em[em.version == "Restated"].iloc[0]             # FY2023 restated
orig = em[em.version.str.startswith("Original")].iloc[0]


def pct(a, b):
    return (a - b) / b


def fmt_t(x):
    return f"{x:,.0f} t"


st.markdown("""
<style>
.block-container {padding-top: 1.6rem;}
div[data-testid="stMetricValue"] {font-size: 1.7rem;}
.callout {border-left: 4px solid #2F6B4F; background: #F3F7F4; padding: .7rem 1rem; border-radius: 4px; margin: .4rem 0;}
.warn {border-left-color: #C0703F; background: #FBF4EE;}
.gap {border: 1px dashed #B54A3A; border-radius: 6px; padding: .9rem; text-align: center; color: #B54A3A;}
.small {color: #6B7770; font-size: .85rem;}
</style>""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("### 🌿 Wolf & Badger")
    st.caption("Online marketplace for independent fashion & lifestyle brands · UK · private · Certified B Corp")
    st.markdown("**Audience:** sustainability analysts → Sustainability Director → Board")
    st.markdown("**Reporting year:** FY2024 (calendar) · horizon to 2035")
    show_original = st.toggle("Show FY2023 as originally published", value=False,
                              help="FY2023 was restated in the 2025 report (−12.7% on total emissions).")
    st.divider()
    st.markdown("**Data**")
    for f in sorted(DATA.glob("*.csv")):
        st.download_button(f"⬇ {f.name}", f.read_bytes(), file_name=f.name, mime="text/csv", width="stretch")
    st.caption("No figure on this dashboard is third-party assured. Estimates and modelled values are labelled.")

st.title("Wolf & Badger — ESG Performance Dashboard")
st.caption("Built for SAM 503 Lab 4 · Sources: W&B Annual Impact Reports 2024–2025, B Corp Impact Report 2023, "
           "B Lab directory · All emissions in tCO₂e")

tabs = st.tabs(["📌 Overview", "🌍 Climate", "🔮 10-year scenarios", "⚡💧♻️ Energy · Water · Waste",
                "🤝 Social & Governance", "🔎 Data quality", "✅ Recommendations"])

# ============================================================================= 1. OVERVIEW
with tabs[0]:
    c = st.columns(6)
    c[0].metric("Total emissions FY2024", fmt_t(latest.total_reported_t),
                f"{pct(latest.total_reported_t, base.total_reported_t):+.0%} vs FY2023", delta_color="inverse")
    c[1].metric("Intensity (t / £m GMV)", f"{latest.intensity_t_per_gbp_m:.1f}",
                f"{pct(latest.intensity_t_per_gbp_m, base.intensity_t_per_gbp_m):+.0%}", delta_color="inverse")
    c[2].metric("Scope 3 share", f"{latest.scope3_t / latest.total_reported_t:.1%}")
    c[3].metric("Freight share of Scope 3", f"{8000 / latest.scope3_t:.0%}")
    c[4].metric("B Impact score (2025)", "108.8", "+34% vs 2021")
    c[5].metric("Engagement score", "84 / 100", "+13 pts")

    left, right = st.columns([1.15, 1])
    with left:
        st.subheader("Key ESG questions this dashboard answers")
        st.markdown("""
1. **Is the footprint growing faster than the business?** → *Climate*, *Scenarios*
2. **What drives emissions, and how much of the change is real vs methodological?** → *Climate*
3. **Can W&B hit a credible 2030 Scope 3 target while growing ~15% a year?** → *Scenarios*
4. **Where are the disclosure gaps (energy, water, waste, workforce, board)?** → *Energy·Water·Waste*, *Data quality*
5. **Are social and governance practices improving?** → *Social & Governance*
""")
    with right:
        st.subheader("What the data says")
        st.markdown(f"""
<div class="callout"><b>Delivery is the footprint.</b> Freight (Scope 3 Cat. 9) is 78% of Scope 3; Scope 1 is zero
and market-based Scope 2 is ~0 after the switch to renewable tariffs.</div>
<div class="callout warn"><b>Emissions grew faster than sales.</b> Total +55% vs GMV +15%. The company attributes much
of the gap to data: freight calculated from activity data fell from 59% to 26% after a carrier change. Its like-for-like estimate is ≈ +15%.</div>
<div class="callout warn"><b>No target, no assurance.</b> The 2030 net-zero ambition (2023) was not reaffirmed. The Scope 3
target % is still undefined, and no KPI is third-party assured.</div>
<div class="callout"><b>Social & governance momentum is real.</b> B Impact score up from 81 to 108.8 (verified by B Lab); engagement up from 71 to 84.</div>
""", unsafe_allow_html=True)

    st.subheader("Areas requiring urgent attention")
    urgent = pd.DataFrame([
        ("🔴", "Climate", "Scope 3 freight growth without a reduction target", "Rising +52%; target % not set"),
        ("🔴", "Data", "Freight data quality (only 26% activity-based)", "Distorts the trend; blocks target-setting"),
        ("🟠", "Environment", "Energy, water and waste not disclosed", "Cannot benchmark or manage"),
        ("🟠", "Governance", "No third-party assurance; board composition not disclosed", "Credibility risk with investors and partners"),
        ("🟡", "Social", "Gender pay gap analysed but not published", "Transparency gap"),
    ], columns=["", "Area", "Issue", "Why it matters"])
    st.dataframe(urgent, hide_index=True, width="stretch")

# ============================================================================= 2. CLIMATE
with tabs[1]:
    a, b = st.columns(2)
    with a:
        rows = [orig, base, latest] if show_original else [base, latest]
        labels = ["FY2023 (original)", "FY2023 (restated)", "FY2024"] if show_original else ["FY2023 (restated)", "FY2024"]
        fig = go.Figure()
        fig.add_bar(name="Scope 1", x=labels, y=[r.scope1_t for r in rows], marker_color=SAND)
        fig.add_bar(name="Scope 2 (market-based)", x=labels, y=[r.scope2_market_t for r in rows], marker_color=SKY)
        fig.add_bar(name="Scope 3", x=labels, y=[r.scope3_t for r in rows], marker_color=GREEN)
        fig.update_layout(barmode="stack", title="Emissions by scope (tCO₂e)", **LAYOUT)
        st.plotly_chart(fig, width="stretch")
        st.caption("Scope 1 = 0 (no owned combustion; no refrigerant top-ups). Market-based Scope 2 = 0.00k t in FY2024.")
    with b:
        fig = go.Figure()
        colors = {"Freight (Cat. 9 downstream transport)": GREEN, "Digital advertising (Cat. 1)": SAGE,
                  "Service purchases + other (residual)": SAND}
        for cat, g in s3.groupby("category", sort=False):
            fig.add_bar(name=cat, x=g.year.astype(str), y=g.tco2e, marker_color=colors[cat],
                        text=[f"{v:,.0f}" for v in g.tco2e], textposition="inside")
        fig.update_layout(barmode="stack", title="Scope 3 by category (tCO₂e)", **LAYOUT)
        st.plotly_chart(fig, width="stretch")
        st.caption("2024 freight 8.0k t (78%); digital advertising 1.57k t. Residual = reported total − itemised categories.")

    a, b = st.columns(2)
    with a:
        fig = go.Figure()
        yrs = ["FY2023", "FY2024"]
        fig.add_bar(name="Total emissions (t)", x=yrs, y=[base.total_reported_t, latest.total_reported_t],
                    marker_color=GREEN, yaxis="y")
        fig.add_scatter(name="Intensity (t / £m GMV)", x=yrs, y=[base.intensity_t_per_gbp_m, latest.intensity_t_per_gbp_m],
                        mode="lines+markers+text", text=[f"{base.intensity_t_per_gbp_m:.1f}", f"{latest.intensity_t_per_gbp_m:.1f}"],
                        textposition="top center", line=dict(color=CLAY, width=3), yaxis="y2")
        fig.add_scatter(name="GMV (£m)", x=yrs, y=[base.gmv_gbp_m, latest.gmv_gbp_m], mode="lines+markers",
                        line=dict(color=SKY, dash="dot"), yaxis="y2")
        fig.update_layout(title="Absolute vs intensity: emissions +55%, GMV +15%",
                          yaxis=dict(title="tCO₂e"), yaxis2=dict(title="t/£m · £m", overlaying="y", side="right"), **LAYOUT)
        st.plotly_chart(fig, width="stretch")
    with b:
        fig = go.Figure(go.Waterfall(
            x=["FY2023 as published", "Scope 3 restatement", "Scope 2 / rounding", "FY2023 restated", "Freight Δ",
               "Digital Δ", "Other Δ", "Scope 2 Δ", "FY2024"],
            measure=["absolute", "relative", "relative", "total", "relative", "relative", "relative", "relative", "total"],
            y=[orig.total_reported_t, base.scope3_t - orig.scope3_t,
               (base.total_reported_t - base.scope3_t) - (orig.total_reported_t - orig.scope3_t), 0,
               8000 - 4500, 1570 - 1400, 730 - 690,
               (latest.total_reported_t - latest.scope3_t) - (base.total_reported_t - base.scope3_t), 0],
            connector=dict(line=dict(color="#ccc")), increasing=dict(marker_color=CLAY),
            decreasing=dict(marker_color=SAGE), totals=dict(marker_color=GREEN)))
        fig.update_layout(title="Bridge: restatement and FY2023 → FY2024 drivers (tCO₂e)", showlegend=False, **LAYOUT)
        st.plotly_chart(fig, width="stretch")

    a, b = st.columns([1, 1.2])
    with a:
        fig = go.Figure()
        fig.add_bar(x=["FY2023", "FY2024"], y=[59, 26], name="Activity-based", marker_color=GREEN,
                    text=["59%", "26%"], textposition="inside")
        fig.add_bar(x=["FY2023", "FY2024"], y=[41, 74], name="Spend-based", marker_color=SAND,
                    text=["41%", "74%"], textposition="inside")
        fig.update_layout(barmode="stack", title="Freight emissions: share by calculation method (%)", **LAYOUT)
        st.plotly_chart(fig, width="stretch")
    with b:
        st.markdown("#### Real or methodological?")
        st.markdown(f"""
- Reported Scope 3 rose **{pct(latest.scope3_t, base.scope3_t):+.0%}**, but GMV and shipment volumes rose only **~15%**.
- After a UK–US shipping lane moved to a new carrier in Oct 2023, freight was mostly **spend-based** (74%). Spend-based
  factors are higher because they cannot separate routes or shipment types.
- The company's **like-for-like (spend-only) recalculation** shows freight emissions **+12%**, in line with activity.
- ⇒ Treat the +55% headline as an **upper bound**. The underlying trend is roughly *emissions growing in step with sales*,
  which is still incompatible with any absolute reduction target.
""")
        st.markdown('<p class="small">Sources: 2025 report p.21–24, 52–53. Freight split by method from appendix text.</p>',
                    unsafe_allow_html=True)

# ============================================================================= 3. SCENARIOS
with tabs[2]:
    st.markdown("Explore 2024 → 2035 pathways. **Actuals: FY2023–FY2024. Everything after 2024 is a projection.** "
                "W&B has *not* published a quantified target; the target below is illustrative and adjustable.")
    c1, c2, c3, c4 = st.columns(4)
    growth = c1.slider("GMV growth per year", 0, 25, 15, 1, format="%d%%") / 100
    decarb = c2.slider("Emissions-intensity improvement per year", 0, 30, 5, 1, format="%d%%",
                       help="Greener freight, route optimisation, fewer returns, packaging weight") / 100
    tgt_pct = c3.slider("Illustrative 2030 cut vs 2023 (restated)", 0, 90, 42, 1, format="%d%%",
                        help="42% ≈ SBTi 1.5°C-aligned near-term ambition") / 100
    lfl = c4.toggle("Start from like-for-like 2024", value=False,
                    help="Re-base 2024 to the company's like-for-like estimate (FY2023 × 1.15) to strip out the data-method effect")
    horizon = st.slider("Horizon", 2030, 2035, 2035)

    e24 = base.total_reported_t * 1.15 if lfl else latest.total_reported_t
    g24 = latest.gmv_gbp_m
    years = list(range(2024, horizon + 1))
    gmv = [g24 * (1 + growth) ** (y - 2024) for y in years]
    i24 = e24 / g24
    bau = [gm * i24 for gm in gmv]
    scen = [gm * i24 * (1 - decarb) ** (y - 2024) for y, gm in zip(years, gmv)]
    target_2030 = base.total_reported_t * (1 - tgt_pct)
    tgt_path = [e24 + (target_2030 - e24) * (y - 2024) / 6 if y <= 2030 else target_2030 for y in years]
    req = (target_2030 / e24) ** (1 / 6) / (1 + growth) - 1

    fig = go.Figure()
    fig.add_scatter(x=[2023, 2024], y=[base.total_reported_t, latest.total_reported_t], name="Actual (reported)",
                    mode="lines+markers", line=dict(color=INK, width=3), marker=dict(size=9))
    fig.add_scatter(x=years, y=bau, name="Business-as-usual (intensity flat)", line=dict(color=CLAY, dash="dash"))
    fig.add_scatter(x=years, y=scen, name=f"Scenario: −{decarb:.0%}/yr intensity", line=dict(color=SKY, width=3))
    fig.add_scatter(x=years, y=tgt_path, name=f"Illustrative target path (−{tgt_pct:.0%} by 2030)",
                    line=dict(color=GREEN, dash="dot", width=3))
    fig.add_vrect(x0=2024, x1=horizon, fillcolor="#f4f4f4", opacity=0.6, line_width=0, layer="below",
                  annotation_text="projection", annotation_position="top left")
    fig.update_layout(title="Total emissions pathways (tCO₂e)", xaxis=dict(dtick=1), **LAYOUT)
    st.plotly_chart(fig, width="stretch")

    k = st.columns(4)
    s2030 = scen[years.index(2030)]
    k[0].metric("2030 target (illustrative)", fmt_t(target_2030))
    k[1].metric("2030 under your scenario", fmt_t(s2030), f"{pct(s2030, target_2030):+.0%} vs target", delta_color="inverse")
    k[2].metric("2030 business-as-usual", fmt_t(bau[years.index(2030)]))
    k[3].metric("Intensity cut needed per year", f"{-req:.0%}" if req < 0 else "0%",
                help="Annual fall in t/£m GMV needed to hit the 2030 target at the chosen growth rate")
    st.markdown(f"""<div class="callout warn">At <b>{growth:.0%}</b> annual growth, reaching the illustrative 2030 level requires
emissions intensity to fall about <b>{-req:.0%} every year</b>. With freight at 78% of Scope 3, that is only plausible through
structural change: carrier activity data and greener lanes, fewer returns, more localised shopping, and lighter packaging.
These are the levers named in the company's 2025 roadmap.</div>""", unsafe_allow_html=True)

# ============================================================================= 4. ENERGY / WATER / WASTE
with tabs[3]:
    st.markdown("The lab brief asks for carbon, energy, water and waste. **For W&B only carbon is disclosed.** "
                "The gaps are shown deliberately: they are a finding, not missing work.")
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown("#### ⚡ Energy")
        st.metric("Electricity (modelled, FY2024)", "≈ 145 MWh", help="Back-calculated: location-based 30 t ÷ UK grid 207 kg/MWh")
        st.caption("Range 78–145 MWh depending on UK/US split (US grid 386 kg/MWh). Not disclosed by the company.")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=100, number=dict(suffix="%"),
                                     title=dict(text="Renewable electricity (tariffs)"),
                                     gauge=dict(axis=dict(range=[0, 100]), bar=dict(color=GREEN))))
        fig.update_layout(height=240, margin=dict(l=35, r=35, t=50, b=0))
        st.plotly_chart(fig, width="stretch")
        st.caption("'Renewable electricity tariffs across the board' (2025 report p.21); market-based Scope 2 ≈ 0. "
                   "Qualitative claim, not quantified.")
    with e2:
        st.markdown("#### 💧 Water")
        st.markdown('<div class="gap"><b>NOT DISCLOSED</b><br>No withdrawal, consumption or recycling data</div>',
                    unsafe_allow_html=True)
        st.markdown("""
**Materiality:** low for own operations (office + 3 stores); **high in the value chain** (cotton, dyeing and leather at brands).

**Ask:** metered water for stores/office (GRI 303-5); add water-intensity criteria to the brand Guarantees.
""")
    with e3:
        st.markdown("#### ♻️ Waste")
        st.markdown('<div class="gap"><b>NOT DISCLOSED</b><br>No tonnage, diversion rate or packaging data</div>',
                    unsafe_allow_html=True)
        st.markdown("""
**Materiality:** medium — e-commerce packaging and **returns** (the 2025 roadmap plans a returns analysis).

**Ask:** packaging tonnes per order, returns rate, store waste diversion (GRI 306-3/4/5).
""")
    st.info("A 2023 commitment to build an Environmental Management System tracking store energy, water and waste "
            "(B Corp Impact Report 2023 p.8) had not produced published data by the 2025 report.")

# ============================================================================= 5. SOCIAL & GOVERNANCE
with tabs[4]:
    a, b = st.columns([1.2, 1])
    with a:
        areas = ["Governance", "Workers", "Community", "Environment", "Customers"]
        fig = go.Figure()
        for yr, col in ((2021, SAND), (2025, GREEN)):
            g = bia[(bia.assessment_year == yr) & (bia.impact_area.isin(areas))].set_index("impact_area").loc[areas]
            fig.add_bar(name=str(yr), x=areas, y=g.score, marker_color=col, text=g.score, textposition="outside")
        fig.update_layout(barmode="group", title="B Impact Assessment by impact area (2021 → 2025)", **LAYOUT)
        st.plotly_chart(fig, width="stretch")
        st.caption("Overall 81.0 → 108.8 (+34%); 80 = certification threshold; median ordinary business 50.9. "
                   "Area scores for 2025 are read from the report chart; overall and governance confirmed on the B Lab directory.")
    with b:
        st.metric("Employee engagement", "84 / 100", "+13 vs 2023")
        st.metric("Women in leadership team (2023)", "> 50%")
        hw = sg.query("metric == 'Brands approved — Happy Worker Guarantee'").value.iloc[0]
        fig = go.Figure(go.Funnel(y=["Brand community (~)", "Brands vetted (2024)", "Happy Worker approved"],
                                  x=[2000, 800, hw], marker=dict(color=[SAND, SAGE, GREEN]),
                                  textinfo="value+percent initial"))
        fig.update_layout(title="Supply-chain social due diligence (brands)", height=300, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, width="stretch")
        st.caption("Happy Worker = mandatory self-declaration on tier-1 manufacturers; audit documents only for higher-risk suppliers.")

    st.markdown("#### Governance checklist")
    gov = pd.DataFrame([
        ("Board oversight of ESG strategy", "✅", "Board incl. independent non-executives (number not disclosed)"),
        ("Remuneration Committee / pay-equity oversight", "✅", "Introduced 2024; gender pay gap analysed"),
        ("Gender pay gap published", "❌", "Analysis reported to Board, figures not public"),
        ("Board size / independence % / diversity", "❌", "Not disclosed"),
        ("Third-party assurance of ESG data", "❌", "None; Greenly = calculation partner, B Lab = BIA verification"),
        ("Quantified climate target (validated)", "❌", "Scope 3 2030 % to be defined; SBTi SME route planned"),
        ("Mission lock / B Corp certification", "✅", "Recertified June 2025, Mission Locked +10 points"),
    ], columns=["Practice", "Status", "Evidence"])
    st.dataframe(gov, hide_index=True, width="stretch")

# ============================================================================= 6. DATA QUALITY
with tabs[5]:
    k = st.columns(4)
    disclosed = (kq.quality_score > 0).sum()
    k[0].metric("KPIs assessed (Lab 1)", len(kq))
    k[1].metric("With any disclosure", f"{disclosed} / {len(kq)}")
    k[2].metric("Average quality score", f"{kq.quality_score.mean():.1f} / 100")
    k[3].metric("High-quality KPIs", int((kq.grade == "High Quality").sum()))
    a, b = st.columns([1.3, 1])
    with a:
        d = kq[kq.quality_score > 0].sort_values("quality_score")
        cmap = {"High Quality": GREEN, "Acceptable": SAGE, "Use with Caution": SAND, "Insufficient": RED}
        fig = go.Figure(go.Bar(x=d.quality_score, y=d.kpi, orientation="h", marker_color=[cmap.get(g, MUTED) for g in d.grade],
                               text=d.quality_score, textposition="outside", cliponaxis=False))
        fig.update_layout(title="Quality score of disclosed KPIs (0–100)", height=520, xaxis=dict(range=[0, 118]), **LAYOUT)
        st.plotly_chart(fig, width="stretch")
    with b:
        piv = kq.assign(status=kq.quality_score.gt(0).map({True: "Disclosed / partial", False: "Not disclosed"})) \
                .groupby(["pillar", "status"]).size().unstack(fill_value=0)
        fig = go.Figure()
        for s, col in (("Disclosed / partial", GREEN), ("Not disclosed", RED)):
            if s in piv:
                fig.add_bar(name=s, y=piv.index, x=piv[s], orientation="h", marker_color=col)
        fig.update_layout(barmode="stack", title="KPI coverage by pillar", height=320, **LAYOUT)
        st.plotly_chart(fig, width="stretch")
        st.markdown("""
**Scoring** (Lab 1 rubric): accuracy + completeness + timeliness + consistency, 25 points each.
Consistency is mostly 0 because a same-year second source rarely exists for a private SME.
""")
    with st.expander("Full KPI inventory (Lab 1)"):
        st.dataframe(kq, hide_index=True, width="stretch")

# ============================================================================= 7. RECOMMENDATIONS
with tabs[6]:
    st.markdown("#### For the Sustainability Director → Board")
    recs = pd.DataFrame([
        ("1", "Fix freight data before setting targets", "Contract the UK–US carrier for shipment-level activity data; aim for ≥80% activity-based freight by FY2026",
         "Removes the method distortion behind the +55%; enables a credible base year", "Q2 2026"),
        ("2", "Set and validate a Scope 3 target", "Define the 2030 % (vs 2021 baseline, published), submit via the SBTi SME route, add interim 2027 milestones",
         "Closes the 'no target' gap; aligns with B Corp 2025 standards", "FY2026"),
        ("3", "Decouple freight from growth", "Localised-shopping nudges, returns reduction, consolidated and greener lanes, packaging-weight KPI per order",
         "To hit a −42% 2030 target, intensity must fall ~19–26% a year at 5–15% growth (see Scenarios)", "Ongoing"),
        ("4", "Close operational disclosure gaps", "Publish kWh, water (m³) and waste/packaging tonnes for the office and 3 stores; quantify the renewable %",
         "Turns 28 'insufficient' KPIs into evidence", "FY2025 report"),
        ("5", "Raise data credibility", "Obtain limited assurance (ISAE 3000) on Scope 1–3 at the next report; publish board composition and the gender pay gap",
         "Investor and partner trust; consistency score", "FY2026"),
    ], columns=["#", "Recommendation", "Action", "Why / impact", "When"])
    st.dataframe(recs, hide_index=True, width="stretch")
    st.markdown("""<div class="callout"><b>Story in one line:</b> W&B's social and governance performance is improving and
verified, but its climate footprint is almost entirely freight and is growing with sales. Better freight data and a
validated Scope 3 target are the two decisions that unlock everything else.</div>""", unsafe_allow_html=True)

st.divider()
st.caption("Limitations: two years of emissions data (FY2023 restated, FY2024); all values self-reported and unassured; "
           "projections are illustrative scenarios, not forecasts. Prepared for SAM 503 (ESG Analytics & Management), IIT Stuart.")
