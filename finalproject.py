import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ============================================================
# Page config & styling
# ============================================================
st.set_page_config(page_title="The Quiet Rise of Early-Onset Colorectal Cancer", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        .block-container { padding-top: 1.0rem; padding-bottom: 2.2rem; max-width: 1450px; }
        h1, h2, h3 { letter-spacing: -0.02em; }
        .metric-box {
            border: 1px solid #e5e7eb; border-radius: 18px; background: #ffffff;
            padding: 16px 16px 14px 16px; min-height: 96px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }
        .tag {
            display: inline-block; padding: 3px 9px; border-radius: 999px;
            font-size: 0.72rem; font-weight: 600; margin-left: 8px;
            background: #dbeafe; color: #1d4ed8;
        }
        .tag-real { background: #dcfce7; color: #15803d; }
        .footnote {
            font-size: 0.78rem; color: #6b7280; font-style: italic;
            margin-top: 8px; padding: 8px 10px; background: #f9fafb;
            border-left: 3px solid #93c5fd; border-radius: 4px;
        }
        .narrative {
            font-size: 0.95rem; color: #1f2937;
            background: #fef3c7; border-left: 4px solid #f59e0b;
            padding: 12px 16px; border-radius: 6px; margin: 8px 0 16px 0;
        }
        .question-anchor {
            background: #eff6ff; border-left: 4px solid #2563eb;
            padding: 12px 16px; border-radius: 6px; margin: 10px 0 16px 0;
        }
        .takeaway {
            background: #ecfdf5; border-left: 4px solid #10b981;
            padding: 12px 16px; border-radius: 6px; margin: 8px 0 16px 0;
            font-size: 0.95rem;
        }
        .section-divider {
            border-top: 2px solid #e5e7eb;
            margin: 30px 0 20px 0;
        }
        .chapter-num {
            display: inline-block;
            background: #1d4ed8; color: white;
            width: 32px; height: 32px; line-height: 32px;
            text-align: center; border-radius: 50%;
            font-weight: bold; margin-right: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Data Loading — REAL DATA SOURCES
# ============================================================
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

@st.cache_data
def load_state_counts():
    df = pd.read_csv(os.path.join(DATA_DIR, "colorectal_only_combined.csv"))
    df = df[(df['geography_level'] != 'national') & (df['state'] != 'US')]
    return df

@st.cache_data
def load_state_rates_real():
    return pd.read_csv(os.path.join(DATA_DIR, "state_crc_rates_real.csv"))

@st.cache_data
def load_globocan():
    return pd.read_csv(os.path.join(DATA_DIR, "globocan_2022_crc.csv"))

@st.cache_data
def load_globocan_historical():
    return pd.read_csv(os.path.join(DATA_DIR, "globocan_historical.csv"))

@st.cache_data
def load_historical_trends():
    return pd.read_csv(os.path.join(DATA_DIR, "historical_crc_trends.csv"))

@st.cache_data
def load_seer_survival():
    return pd.read_csv(os.path.join(DATA_DIR, "seer_survival_by_stage.csv"))

@st.cache_data
def load_risk_factors_real():
    return pd.read_csv(os.path.join(DATA_DIR, "crc_risk_factors_real.csv"))

@st.cache_data
def load_state_obesity():
    return pd.read_csv(os.path.join(DATA_DIR, "state_obesity_brfss.csv"))

@st.cache_data
def load_food_country():
    return pd.read_csv(os.path.join(DATA_DIR, "food_consumption_country.csv"))

@st.cache_data
def load_us_diet_trends():
    return pd.read_csv(os.path.join(DATA_DIR, "us_diet_trends.csv"))

@st.cache_data
def load_cancer_totals():
    return pd.read_csv(os.path.join(DATA_DIR, "cancer_totals_yearly.csv"))

# Region & abbreviation mappings
STATE_TO_REGION = {
    'Connecticut': 'Northeast', 'Maine': 'Northeast', 'Massachusetts': 'Northeast',
    'New Hampshire': 'Northeast', 'Rhode Island': 'Northeast', 'Vermont': 'Northeast',
    'New Jersey': 'Northeast', 'New York': 'Northeast', 'Pennsylvania': 'Northeast',
    'Illinois': 'Midwest', 'Indiana': 'Midwest', 'Michigan': 'Midwest',
    'Ohio': 'Midwest', 'Wisconsin': 'Midwest', 'Iowa': 'Midwest',
    'Kansas': 'Midwest', 'Minnesota': 'Midwest', 'Missouri': 'Midwest',
    'Nebraska': 'Midwest', 'North Dakota': 'Midwest', 'South Dakota': 'Midwest',
    'Delaware': 'South', 'Florida': 'South', 'Georgia': 'South',
    'Maryland': 'South', 'North Carolina': 'South', 'South Carolina': 'South',
    'Virginia': 'South', 'District of Columbia': 'South', 'West Virginia': 'South',
    'Alabama': 'South', 'Kentucky': 'South', 'Mississippi': 'South',
    'Tennessee': 'South', 'Arkansas': 'South', 'Louisiana': 'South',
    'Oklahoma': 'South', 'Texas': 'South',
    'Arizona': 'West', 'Colorado': 'West', 'Idaho': 'West',
    'Montana': 'West', 'Nevada': 'West', 'New Mexico': 'West',
    'Utah': 'West', 'Wyoming': 'West', 'Alaska': 'West',
    'California': 'West', 'Hawaii': 'West', 'Oregon': 'West', 'Washington': 'West',
}
STATE_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC',
}

# Load all datasets
state_counts_df = load_state_counts()
state_rates_df = load_state_rates_real()
globocan_df = load_globocan()
globocan_hist_df = load_globocan_historical()
historical_df = load_historical_trends()
seer_df = load_seer_survival()
risk_real_df = load_risk_factors_real()
obesity_df = load_state_obesity()
food_country_df = load_food_country()
us_diet_df = load_us_diet_trends()
cancer_totals_df = load_cancer_totals()

# Augment state datasets
state_counts_df['region'] = state_counts_df['state'].map(STATE_TO_REGION)
state_counts_df['state_code'] = state_counts_df['state'].map(STATE_ABBREV)
state_rates_df['region'] = state_rates_df['state'].map(STATE_TO_REGION)
state_rates_df['state_code'] = state_rates_df['state'].map(STATE_ABBREV)

# Normalize counts to per-capita rates
pop_lookup = state_rates_df[['state', 'population']].drop_duplicates()
state_counts_df = state_counts_df.merge(pop_lookup, on='state', how='left')
state_counts_df['rate_per_100k'] = (state_counts_df['value'] / state_counts_df['population']) * 100000

# ============================================================
# Sidebar
# ============================================================
st.sidebar.title("Story Navigator")

st.sidebar.markdown(
    "**Chapters**\n\n"
    "1. The Long Rise (1975–2023)\n"
    "2. The Diverging Age Curve (Q2)\n"
    "3. CRC's Share of All Cancer\n"
    "4. The Food Connection (Q1)\n"
    "5. Geographic & Racial Gaps (Q5)\n"
    "6. International Context\n"
    "7. Stage at Diagnosis (Q6)"
)
st.sidebar.markdown("---")

st.sidebar.markdown("**Filters**")
available_years = sorted(state_counts_df['year'].unique())
year_range = st.sidebar.slider(
    "ACS state-data year range",
    min_value=int(min(available_years)), max_value=int(max(available_years)),
    value=(int(min(available_years)), int(max(available_years))),
)
regions = ['All'] + sorted(state_counts_df['region'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions)
selected_metric = st.sidebar.selectbox("Metric", ['cases', 'deaths'])
display_mode = st.sidebar.radio(
    "Display values as",
    ['Rate per 100K (normalized)', 'Raw counts'],
    help="Rates per 100K control for state size and reveal true disparities."
)

st.sidebar.markdown("---")
st.sidebar.success(
    "**All data is real public-health data**\n\n"
    "• ACS Cancer Facts & Figures\n"
    "• CDC State Cancer Statistics\n"
    "• SEER 9 Registry (1973–)\n"
    "• IARC GLOBOCAN 2012/2018/2022\n"
    "• WCRF/AICR meta-analyses\n"
    "• CDC BRFSS 2022\n"
    "• FAO Food Balance Sheets\n"
    "• USDA Economic Research Service"
)

# Apply ACS filters
filtered = state_counts_df[
    (state_counts_df['year'] >= year_range[0]) & (state_counts_df['year'] <= year_range[1])
]
if selected_region != 'All':
    filtered = filtered[filtered['region'] == selected_region]
all_sex = filtered[filtered['sex'].isin(['All', 'Both'])]

value_col = 'rate_per_100k' if display_mode.startswith('Rate') else 'value'
value_label = 'Rate per 100K' if display_mode.startswith('Rate') else 'Count'

# ============================================================
# HEADER — story framing
# ============================================================
st.title("The Quiet Rise of Early-Onset Colorectal Cancer")
st.caption("A data-driven story built on real CDC, ACS, SEER, IARC, WCRF, FAO, and USDA sources")

st.markdown(
    """
    **The story this dashboard tells.**
    Since the mid-1970s, colorectal cancer in adults under 50 has been climbing steadily — even as the
    overall U.S. cancer story is one of progress. This dashboard walks through that paradox in seven
    chapters: the historical trend, the age-group divergence, CRC's place in the broader cancer
    landscape, the dietary correlates, geographic and racial disparities, the international picture,
    and the survival consequences of late detection. Every chart uses real, citable data.
    """
)

with st.expander("Research questions this dashboard answers", expanded=False):
    questions = {
        "Q1": "What lifestyle and dietary factors are most strongly associated with colorectal cancer risk?",
        "Q2": "How do risk and incidence differ between early-onset (<50) and traditional (50+) patients?",
        "Q3": "Are there distinct subgroups of patients under 50 based on health and demographic characteristics?",
        "Q4": "To what extent can colorectal cancer risk in those under 50 be predicted from lifestyle data?",
        "Q5": "How do geographic and socioeconomic factors influence CRC diagnosis rates?",
        "Q6": "How does stage at diagnosis and outcomes vary across demographic groups?",
    }
    for k, v in questions.items():
        st.markdown(f"**{k}.** {v}")

# ============================================================
# CHAPTER 1 — THE LONG RISE (1975–2023)
# ============================================================
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown(
    "<h2><span class='chapter-num'>1</span>The Long Rise: Early-Onset CRC, 1975–2023</h2>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='question-anchor'>"
    "<strong>The setup.</strong> Our class project asked why colorectal cancer diagnoses have been climbing "
    "in patients under 50 since the mid-20th century. National surveillance data starts in 1975 with the "
    "SEER 9 registry — the earliest reliable measurement. Here is what nearly five decades of real data show."
    "</div>",
    unsafe_allow_html=True,
)

eo_hist = historical_df[historical_df['age_group'] == '<50'].sort_values('year')
trad_hist = historical_df[historical_df['age_group'] == '50+'].sort_values('year')

# The headline chart: the 50-year story in one frame
st.markdown(
    "**Five Decades of Colorectal Cancer Incidence by Age Group** "
    "<span class='tag tag-real'>SEER 1975–2023</span>",
    unsafe_allow_html=True,
)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(
    x=eo_hist['year'], y=eo_hist['incidence_rate'],
    mode='lines+markers', name='Under 50 (early-onset)',
    line=dict(color='#dc2626', width=4), marker=dict(size=10),
), secondary_y=False)
fig.add_trace(go.Scatter(
    x=trad_hist['year'], y=trad_hist['incidence_rate'],
    mode='lines+markers', name='50 and older (traditional)',
    line=dict(color='#3b82f6', width=4, dash='dot'), marker=dict(size=10),
), secondary_y=True)
fig.update_yaxes(title_text="Under 50 incidence per 100K", secondary_y=False,
                 color='#dc2626', gridcolor='#fee2e2')
fig.update_yaxes(title_text="50+ incidence per 100K", secondary_y=True,
                 color='#3b82f6', gridcolor='#dbeafe')
fig.update_layout(
    template='simple_white', height=440,
    margin=dict(l=10, r=10, t=28, b=10),
    paper_bgcolor='#fff', plot_bgcolor='#fff',
    legend=dict(orientation='h', y=-0.15),
    hovermode='x unified',
)
fig.update_xaxes(title_text='Year', gridcolor='#e5e7eb')
st.plotly_chart(fig, use_container_width=True)

# Headline numbers
eo_min = eo_hist['incidence_rate'].min()
eo_max = eo_hist['incidence_rate'].iloc[-1]
eo_total_change = (eo_max - eo_min) / eo_min * 100
trad_first = trad_hist['incidence_rate'].iloc[0]
trad_last = trad_hist['incidence_rate'].iloc[-1]
trad_total_change = (trad_last - trad_first) / trad_first * 100

c1a, c1b, c1c, c1d = st.columns(4)
with c1a:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Early-onset 1975 rate</div>"
        f"<div style='margin-top:14px;font-size:1.6rem;font-weight:bold;color:#dc2626'>{eo_min:.1f}</div>"
        f"<div style='font-size:0.78rem;color:#6b7280'>per 100K, ages &lt;50</div></div>",
        unsafe_allow_html=True,
    )
with c1b:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Early-onset 2023 rate</div>"
        f"<div style='margin-top:14px;font-size:1.6rem;font-weight:bold;color:#dc2626'>{eo_max:.1f}</div>"
        f"<div style='font-size:0.78rem;color:#6b7280'>per 100K, ages &lt;50</div></div>",
        unsafe_allow_html=True,
    )
with c1c:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Change since 1975</div>"
        f"<div style='margin-top:14px;font-size:1.6rem;font-weight:bold;color:#dc2626'>{eo_total_change:+.0f}%</div>"
        f"<div style='font-size:0.78rem;color:#6b7280'>nearly 2.5× the 1975 rate</div></div>",
        unsafe_allow_html=True,
    )
with c1d:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>50+ change since 1975</div>"
        f"<div style='margin-top:14px;font-size:1.6rem;font-weight:bold;color:#059669'>{trad_total_change:+.0f}%</div>"
        f"<div style='font-size:0.78rem;color:#6b7280'>screening-driven decline</div></div>",
        unsafe_allow_html=True,
    )

st.markdown(
    "<div class='takeaway'>"
    "<strong>Takeaway (Q2).</strong> The 50+ rate fell by more than half over five decades thanks to "
    "screening — but the under-50 rate climbed nearly 150%. The two age groups are moving in opposite "
    "directions. The rest of this dashboard examines why."
    "</div>",
    unsafe_allow_html=True,
)

# ============================================================
# CHAPTER 2 — THE DIVERGING AGE CURVE (mortality + incidence)
# ============================================================
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown(
    "<h2><span class='chapter-num'>2</span>The Diverging Age Curve</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='question-anchor'>"
    "<strong>Q2.</strong> Both incidence and mortality should track each other if treatment was "
    "evenly improving. Instead, the under-50 mortality rate is also rising — meaning younger patients "
    "are dying of CRC at rates not seen in decades."
    "</div>",
    unsafe_allow_html=True,
)

c2a, c2b = st.columns(2)

with c2a:
    st.markdown(
        "**Incidence by Age Group** <span class='tag tag-real'>SEER/ACS</span>",
        unsafe_allow_html=True,
    )
    fig = px.line(
        historical_df, x='year', y='incidence_rate', color='age_group',
        markers=True, template='simple_white',
        color_discrete_map={'<50': '#dc2626', '50+': '#3b82f6'},
        labels={'incidence_rate': 'Incidence per 100K', 'age_group': 'Age group'},
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=28, b=10),
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_yaxes(gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)

with c2b:
    st.markdown(
        "**Mortality by Age Group** <span class='tag tag-real'>SEER/ACS</span>",
        unsafe_allow_html=True,
    )
    fig = px.line(
        historical_df, x='year', y='mortality_rate', color='age_group',
        markers=True, template='simple_white',
        color_discrete_map={'<50': '#dc2626', '50+': '#3b82f6'},
        labels={'mortality_rate': 'Mortality per 100K', 'age_group': 'Age group'},
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=28, b=10),
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_yaxes(gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<div class='takeaway'>"
    "<strong>Takeaway.</strong> Under-50 mortality has risen ~140% (1.8 → 4.3 per 100K) since 1975. "
    "The trend isn't just better detection of asymptomatic cases — younger patients are genuinely dying more often."
    "</div>",
    unsafe_allow_html=True,
)

# ============================================================
# CHAPTER 3 — CRC'S SHARE OF ALL CANCER (Year-by-year %)
# ============================================================
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown(
    "<h2><span class='chapter-num'>3</span>CRC's Share of All Cancer Diagnoses</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='question-anchor'>"
    "<strong>Context.</strong> Total U.S. cancer cases keep rising as the population ages. So is CRC "
    "rising in absolute numbers? Yes — but its share of all cancer is declining, masking the early-onset "
    "shift inside the headline numbers."
    "</div>",
    unsafe_allow_html=True,
)

c3a, c3b = st.columns([1.3, 1])

with c3a:
    st.markdown(
        "**Total New Cancers vs CRC Cases per Year** "
        "<span class='tag tag-real'>ACS Cancer Facts & Figures</span>",
        unsafe_allow_html=True,
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=cancer_totals_df['year'], y=cancer_totals_df['total_new_cancer_cases'],
        name='All cancer (new cases)', marker_color='#cbd5e1',
        hovertemplate='%{y:,}<extra></extra>',
    ), secondary_y=False)
    fig.add_trace(go.Bar(
        x=cancer_totals_df['year'], y=cancer_totals_df['crc_cases'],
        name='Colorectal cancer', marker_color='#dc2626',
        hovertemplate='%{y:,}<extra></extra>',
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=cancer_totals_df['year'], y=cancer_totals_df['crc_pct_of_total'],
        name='CRC % of all cancer',
        line=dict(color='#1f2937', width=3, dash='dash'),
        marker=dict(size=8), mode='lines+markers',
        hovertemplate='%{y}%<extra></extra>',
    ), secondary_y=True)
    fig.update_layout(
        template='simple_white', height=420, barmode='overlay',
        margin=dict(l=10, r=10, t=28, b=10),
        paper_bgcolor='#fff', plot_bgcolor='#fff',
        legend=dict(orientation='h', y=-0.18),
        hovermode='x unified',
    )
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='New cases (count)', secondary_y=False, gridcolor='#e5e7eb')
    fig.update_yaxes(title_text='CRC share of all cancer (%)', secondary_y=True, range=[0, 12])
    st.plotly_chart(fig, use_container_width=True)

with c3b:
    st.markdown(
        "**Year-by-Year Breakdown** <span class='tag'>summary</span>",
        unsafe_allow_html=True,
    )
    display_totals = cancer_totals_df[[
        'year', 'total_new_cancer_cases', 'crc_cases', 'crc_pct_of_total'
    ]].copy()
    display_totals.columns = ['Year', 'All cancer cases', 'CRC cases', 'CRC %']
    display_totals['All cancer cases'] = display_totals['All cancer cases'].map(lambda x: f'{x:,}')
    display_totals['CRC cases'] = display_totals['CRC cases'].map(lambda x: f'{x:,}')
    display_totals['CRC %'] = display_totals['CRC %'].map(lambda x: f'{x}%')
    st.dataframe(display_totals, use_container_width=True, hide_index=True, height=420)

st.markdown(
    f"<div class='footnote'>Source: ACS Cancer Facts & Figures, annual editions. "
    f"In 2000, CRC was 10.7% of all new cancer cases; by 2024, it's 7.6%. The absolute number of CRC cases is "
    f"flat-to-slightly-up (130K → 153K) while total cancers have grown faster (1.22M → 2.00M).</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='takeaway'>"
    "<strong>Takeaway.</strong> CRC's declining share of total cancer would feel like good news — except the "
    "decline reflects success in the 50+ population. Inside that aggregate, the early-onset rate is climbing "
    "in the opposite direction. Looking only at the share masks the under-50 problem."
    "</div>",
    unsafe_allow_html=True,
)

# ============================================================
# CHAPTER 4 — THE FOOD CONNECTION (Q1)
# ============================================================
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown(
    "<h2><span class='chapter-num'>4</span>The Food Connection</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='question-anchor'>"
    "<strong>Q1.</strong> What modifiable factors drive CRC risk? The IARC classifies processed meat as a "
    "Group 1 carcinogen and red meat as Group 2A. Below: real published meta-analysis effect sizes plus "
    "country-level dietary intake correlated with CRC incidence."
    "</div>",
    unsafe_allow_html=True,
)

# 4a — Forest plot of relative risks
st.markdown(
    "**Relative Risk by Modifiable Factor** "
    "<span class='tag tag-real'>WCRF/AICR meta-analyses</span>",
    unsafe_allow_html=True,
)

risk_sorted = risk_real_df.copy()
risk_sorted['err_low'] = risk_sorted['relative_risk'] - risk_sorted['ci_lower']
risk_sorted['err_high'] = risk_sorted['ci_upper'] - risk_sorted['relative_risk']
risk_sorted = risk_sorted.sort_values('relative_risk')

fig = go.Figure()
colors = ['#dc2626' if d == 'Increases' else '#059669' for d in risk_sorted['direction']]
fig.add_trace(go.Scatter(
    x=risk_sorted['relative_risk'], y=risk_sorted['risk_factor'],
    mode='markers',
    marker=dict(size=14, color=colors, line=dict(color='#1f2937', width=1)),
    error_x=dict(type='data', symmetric=False,
                 array=risk_sorted['err_high'], arrayminus=risk_sorted['err_low'],
                 color='#6b7280', thickness=2, width=8),
    text=[f"RR={rr:.2f} ({lo:.2f}–{hi:.2f})<br>{src}<br>Evidence: {ev}"
          for rr, lo, hi, src, ev in zip(
              risk_sorted['relative_risk'], risk_sorted['ci_lower'],
              risk_sorted['ci_upper'], risk_sorted['source'], risk_sorted['evidence_grade'])],
    hovertemplate='%{y}<br>%{text}<extra></extra>',
))
fig.add_vline(x=1.0, line_dash='dash', line_color='#9ca3af',
              annotation_text='No effect (RR=1.0)', annotation_position='top')
fig.update_layout(
    template='simple_white', height=460,
    margin=dict(l=10, r=10, t=28, b=10),
    xaxis_title='Relative risk (95% CI)', yaxis_title='',
    paper_bgcolor='#fff', plot_bgcolor='#fff', showlegend=False,
)
fig.update_xaxes(gridcolor='#e5e7eb')
st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "<div class='footnote'>Sources: WCRF/AICR Continuous Update Project 2018; IARC Monograph Vol. 100E (smoking); "
    "Larsson 2005 (diabetes). Red bars = risk-increasing; green = protective.</div>",
    unsafe_allow_html=True,
)

# 4b — Country food consumption vs CRC
st.markdown(
    "**Country Red Meat Consumption vs CRC Incidence** "
    "<span class='tag tag-real'>FAO + GLOBOCAN</span>",
    unsafe_allow_html=True,
)

food_crc = food_country_df.merge(globocan_df, on='country', how='inner')
fig = px.scatter(
    food_crc, x='red_meat_kg_per_capita_yr', y='incidence_asr_per_100k',
    color='region', hover_name='country', template='simple_white',
    trendline='ols', size='red_meat_kg_per_capita_yr', size_max=28,
    labels={'red_meat_kg_per_capita_yr': 'Red meat consumption (kg/person/year)',
            'incidence_asr_per_100k': 'CRC incidence per 100K (ASR)'},
)
fig.update_layout(height=420, margin=dict(l=10, r=10, t=28, b=10),
                  paper_bgcolor='#fff', plot_bgcolor='#fff')
fig.update_yaxes(gridcolor='#e5e7eb')
fig.update_xaxes(gridcolor='#e5e7eb')

food_corr = food_crc[['red_meat_kg_per_capita_yr', 'incidence_asr_per_100k']].corr().iloc[0, 1]
fig.add_annotation(x=food_crc['red_meat_kg_per_capita_yr'].max() * 0.7,
                   y=food_crc['incidence_asr_per_100k'].max() * 0.95,
                   text=f"<b>Pearson r = {food_corr:.2f}</b>",
                   showarrow=False, font=dict(size=14, color='#1f2937'),
                   bgcolor='white', bordercolor='#9ca3af', borderwidth=1)
st.plotly_chart(fig, use_container_width=True)
st.markdown(
    f"<div class='footnote'>Sources: FAO Food Balance Sheets 2020 (per-capita red meat); "
    f"IARC GLOBOCAN 2022 (CRC ASR). Country-level Pearson r = <strong>{food_corr:.2f}</strong>. "
    f"India and Nigeria — among the lowest red-meat consumers — also have the lowest CRC rates.</div>",
    unsafe_allow_html=True,
)

# 4c — Processed meat
food_corr2 = food_crc[['processed_meat_kg_per_capita_yr', 'incidence_asr_per_100k']].corr().iloc[0, 1]

c4a, c4b = st.columns(2)
with c4a:
    st.markdown(
        "**Processed Meat vs CRC Incidence** <span class='tag tag-real'>FAO + GLOBOCAN</span>",
        unsafe_allow_html=True,
    )
    fig = px.scatter(
        food_crc, x='processed_meat_kg_per_capita_yr', y='incidence_asr_per_100k',
        color='region', hover_name='country', template='simple_white',
        trendline='ols',
        labels={'processed_meat_kg_per_capita_yr': 'Processed meat (kg/person/year)',
                'incidence_asr_per_100k': 'CRC incidence per 100K'},
    )
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_yaxes(gridcolor='#e5e7eb')
    fig.update_xaxes(gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        f"<div class='footnote'>Pearson r = <strong>{food_corr2:.2f}</strong>. Germany — Europe's processed-meat capital — "
        f"sits high on CRC incidence.</div>",
        unsafe_allow_html=True,
    )

with c4b:
    fiber_corr = food_crc[['fiber_g_per_capita_day', 'incidence_asr_per_100k']].corr().iloc[0, 1]
    st.markdown(
        "**Dietary Fiber vs CRC Incidence** <span class='tag tag-real'>FAO + GLOBOCAN</span>",
        unsafe_allow_html=True,
    )
    fig = px.scatter(
        food_crc, x='fiber_g_per_capita_day', y='incidence_asr_per_100k',
        color='region', hover_name='country', template='simple_white',
        trendline='ols',
        labels={'fiber_g_per_capita_day': 'Dietary fiber (g/person/day)',
                'incidence_asr_per_100k': 'CRC incidence per 100K'},
    )
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_yaxes(gridcolor='#e5e7eb')
    fig.update_xaxes(gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        f"<div class='footnote'>Pearson r = <strong>{fiber_corr:.2f}</strong>. Negative correlation: "
        f"high-fiber diets (India, Pakistan, Nigeria, Kenya) track with lower CRC.</div>",
        unsafe_allow_html=True,
    )

# 4d — US dietary trends overlay
st.markdown(
    "**The U.S. Diet, 1970–2023** "
    "<span class='tag tag-real'>USDA ERS / NHANES</span>",
    unsafe_allow_html=True,
)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(
    x=us_diet_df['year'], y=us_diet_df['ultraprocessed_pct_calories'],
    mode='lines+markers', name='Ultra-processed % of calories',
    line=dict(color='#dc2626', width=3), marker=dict(size=8),
), secondary_y=False)
fig.add_trace(go.Scatter(
    x=us_diet_df['year'], y=us_diet_df['sugar_added_lbs_per_capita'],
    mode='lines+markers', name='Added sugar (lbs/yr)',
    line=dict(color='#f59e0b', width=3, dash='dot'), marker=dict(size=8),
), secondary_y=True)
fig.add_trace(go.Scatter(
    x=us_diet_df['year'], y=us_diet_df['red_meat_lbs_per_capita'],
    mode='lines+markers', name='Red meat (lbs/yr)',
    line=dict(color='#7c3aed', width=3, dash='dash'), marker=dict(size=8),
), secondary_y=True)
fig.update_yaxes(title_text='Ultra-processed % of calories', secondary_y=False, gridcolor='#fee2e2')
fig.update_yaxes(title_text='lbs / person / year', secondary_y=True, gridcolor='#dbeafe')
fig.update_layout(template='simple_white', height=380, margin=dict(l=10, r=10, t=28, b=10),
                  paper_bgcolor='#fff', plot_bgcolor='#fff',
                  legend=dict(orientation='h', y=-0.18), hovermode='x unified')
fig.update_xaxes(title_text='Year')
st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "<div class='footnote'>Sources: USDA ERS food availability series; Martínez Steele et al. 2016 (NHANES "
    "ultra-processed estimates). The U.S. diet shifted from ~53% to ~57% ultra-processed calories during "
    "the same decades when early-onset CRC began climbing.</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='takeaway'>"
    f"<strong>Takeaway (Q1).</strong> At the country level, red meat (r={food_corr:.2f}) and processed meat "
    f"(r={food_corr2:.2f}) consumption show strong positive correlations with CRC incidence; fiber shows a "
    f"clear negative correlation (r={fiber_corr:.2f}). The U.S. dietary shift toward ultra-processed foods "
    f"(53→57% of calories) coincides with the rise in early-onset disease."
    "</div>",
    unsafe_allow_html=True,
)

# ============================================================
# CHAPTER 5 — GEOGRAPHIC & RACIAL DISPARITIES (Q5)
# ============================================================
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown(
    "<h2><span class='chapter-num'>5</span>Geographic & Racial Disparities</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='question-anchor'>"
    "<strong>Q5.</strong> Within the U.S., who carries the heaviest CRC burden? Once we normalize to rates per "
    "100K, the headline shifts from population-heavy states to Appalachia, the Deep South, and Black communities."
    "</div>",
    unsafe_allow_html=True,
)

# Choropleth
st.markdown(
    "**State CRC Rates per 100K** <span class='tag tag-real'>CDC</span>",
    unsafe_allow_html=True,
)
fig = px.choropleth(
    state_rates_df, locations='state_code', locationmode='USA-states',
    color='crc_rate_total', scope='usa', hover_name='state',
    color_continuous_scale='Reds', template='simple_white',
    labels={'crc_rate_total': 'CRC per 100K'},
    hover_data={'crc_rate_total': ':.1f', 'population': ':,', 'state_code': False},
)
fig.update_layout(height=400, margin=dict(l=10, r=10, t=28, b=10),
                  paper_bgcolor='#fff', plot_bgcolor='#fff',
                  coloraxis_colorbar_title='Rate per 100K')
st.plotly_chart(fig, use_container_width=True)

# Top 10 states normalized vs raw
c5a, c5b = st.columns(2)
with c5a:
    st.markdown("**Top 10 by Rate per 100K** <span class='tag tag-real'>normalized</span>", unsafe_allow_html=True)
    top_rate = state_rates_df.nlargest(10, 'crc_rate_total')[['state', 'crc_rate_total']]
    fig = px.bar(top_rate.sort_values('crc_rate_total'),
                 x='crc_rate_total', y='state', orientation='h',
                 template='simple_white', color='crc_rate_total',
                 color_continuous_scale='Reds',
                 labels={'crc_rate_total': 'CRC per 100K', 'state': ''})
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                      coloraxis_showscale=False, paper_bgcolor='#fff', plot_bgcolor='#fff')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "<div class='footnote'>Mississippi, Kentucky, West Virginia carry the heaviest per-capita CRC burden.</div>",
        unsafe_allow_html=True,
    )
with c5b:
    st.markdown("**Top 10 by Raw Cases (for contrast)** <span class='tag'>not normalized</span>", unsafe_allow_html=True)
    raw_counts = (all_sex[all_sex['metric'] == 'cases'].groupby('state')['value'].sum()
                  .nlargest(10).reset_index())
    fig = px.bar(raw_counts.sort_values('value'),
                 x='value', y='state', orientation='h',
                 template='simple_white', color='value',
                 color_continuous_scale='Blues',
                 labels={'value': 'Total cases', 'state': ''})
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                      coloraxis_showscale=False, paper_bgcolor='#fff', plot_bgcolor='#fff')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "<div class='footnote'>Without normalization, the leaders just reflect population size — not disparity.</div>",
        unsafe_allow_html=True,
    )

# Race
st.markdown(
    "**Racial Disparities in State CRC Rates** <span class='tag tag-real'>CDC</span>",
    unsafe_allow_html=True,
)
race_long = state_rates_df.melt(
    id_vars=['state'],
    value_vars=['crc_rate_white', 'crc_rate_black', 'crc_rate_asian',
                'crc_rate_indigenous', 'crc_rate_hispanic'],
    var_name='race', value_name='rate',
)
race_long['race'] = race_long['race'].str.replace('crc_rate_', '').str.title()
race_long = race_long[race_long['rate'] > 0]
fig = px.box(race_long, x='race', y='rate', color='race',
             template='simple_white', points='outliers',
             labels={'rate': 'CRC per 100K', 'race': ''},
             color_discrete_map={'White': '#3b82f6', 'Black': '#dc2626',
                                 'Asian': '#10b981', 'Indigenous': '#a855f7',
                                 'Hispanic': '#f59e0b'})
fig.update_layout(height=360, margin=dict(l=10, r=10, t=28, b=10),
                  showlegend=False, paper_bgcolor='#fff', plot_bgcolor='#fff')
fig.update_yaxes(gridcolor='#e5e7eb')
st.plotly_chart(fig, use_container_width=True)

mean_white = race_long[race_long['race'] == 'White']['rate'].mean()
mean_black = race_long[race_long['race'] == 'Black']['rate'].mean()
disparity_summary = state_rates_df[['state', 'disparity_ratio_black_white']].dropna()
disparity_summary = disparity_summary[disparity_summary['disparity_ratio_black_white'] > 0]
median_disparity = disparity_summary['disparity_ratio_black_white'].median()

st.markdown(
    f"<div class='footnote'>Black Americans face an average of <strong>{mean_black:.1f} per 100K</strong> "
    f"vs <strong>{mean_white:.1f} per 100K</strong> for white Americans — a median rate ratio of "
    f"<strong>{median_disparity:.2f}×</strong>.</div>",
    unsafe_allow_html=True,
)

# Obesity scatter
st.markdown(
    "**Q1 × Q5: State Obesity Prevalence vs CRC Rate** "
    "<span class='tag tag-real'>BRFSS + CDC</span>",
    unsafe_allow_html=True,
)
merged = state_rates_df.merge(obesity_df, on='state', how='inner')
merged['region'] = merged['state'].map(STATE_TO_REGION)
fig = px.scatter(merged, x='obesity_pct_adults', y='crc_rate_total',
                 color='region', hover_name='state',
                 template='simple_white', trendline='ols',
                 labels={'obesity_pct_adults': 'Adult obesity (%)',
                         'crc_rate_total': 'CRC per 100K'},
                 size='population', size_max=28)
fig.update_layout(height=400, margin=dict(l=10, r=10, t=28, b=10),
                  paper_bgcolor='#fff', plot_bgcolor='#fff')
fig.update_yaxes(gridcolor='#e5e7eb')
fig.update_xaxes(gridcolor='#e5e7eb')
corr = merged[['obesity_pct_adults', 'crc_rate_total']].corr().iloc[0, 1]
fig.add_annotation(x=merged['obesity_pct_adults'].max() * 0.95,
                   y=merged['crc_rate_total'].max() * 0.95,
                   text=f"<b>r = {corr:.2f}</b>",
                   showarrow=False, font=dict(size=14),
                   bgcolor='white', bordercolor='#9ca3af', borderwidth=1)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    f"<div class='takeaway'>"
    f"<strong>Takeaway (Q5).</strong> Geographic disparity tracks both racial composition and lifestyle prevalence. "
    f"Black Americans face systematically higher rates ({mean_black:.1f} vs {mean_white:.1f} per 100K). "
    f"State obesity correlates with CRC at r={corr:.2f}, concentrated in the South and Appalachia."
    f"</div>",
    unsafe_allow_html=True,
)

# ============================================================
# CHAPTER 6 — INTERNATIONAL CONTEXT (with historical GLOBOCAN)
# ============================================================
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown(
    "<h2><span class='chapter-num'>6</span>International Context: A Decade of GLOBOCAN</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='question-anchor'>"
    "<strong>Q5 (international).</strong> IARC's GLOBOCAN releases (2012, 2018, 2022) let us watch how "
    "country-level CRC rates have shifted over a decade. Some patterns: high-income Europe is improving, "
    "while China and India are seeing rising rates as their diets Westernize."
    "</div>",
    unsafe_allow_html=True,
)

# Historical comparison line chart
st.markdown(
    "**Country CRC Incidence Across GLOBOCAN Editions** "
    "<span class='tag tag-real'>IARC 2012/2018/2022</span>",
    unsafe_allow_html=True,
)
focus_countries = ['Hungary', 'USA', 'UK', 'Japan', 'South Korea', 'China', 'India', 'Brazil', 'Australia', 'Germany']
focus_df = globocan_hist_df[globocan_hist_df['country'].isin(focus_countries)].copy()

fig = px.line(focus_df, x='edition_year', y='incidence_asr_per_100k', color='country',
              markers=True, template='simple_white',
              labels={'incidence_asr_per_100k': 'CRC incidence per 100K (ASR)',
                      'edition_year': 'GLOBOCAN edition year', 'country': 'Country'})
fig.update_traces(line=dict(width=3), marker=dict(size=12))
fig.update_layout(height=460, margin=dict(l=10, r=10, t=28, b=10),
                  paper_bgcolor='#fff', plot_bgcolor='#fff', hovermode='x unified')
fig.update_yaxes(gridcolor='#e5e7eb')
fig.update_xaxes(tickmode='array', tickvals=[2012, 2018, 2022])
st.plotly_chart(fig, use_container_width=True)

# 10-year change table
st.markdown(
    "**10-Year Change by Country (2012 → 2022)** <span class='tag'>computed</span>",
    unsafe_allow_html=True,
)
change = globocan_hist_df.pivot(index='country', columns='edition_year',
                                 values='incidence_asr_per_100k').reset_index()
change.columns.name = None
change['change_2012_to_2022'] = change[2022] - change[2012]
change['pct_change'] = (change['change_2012_to_2022'] / change[2012] * 100).round(1)
change_display = change[['country', 2012, 2018, 2022, 'pct_change']].copy()
change_display.columns = ['Country', '2012', '2018', '2022', '% change']
change_display = change_display.sort_values('% change', ascending=False)

c6a, c6b = st.columns([1, 1])
with c6a:
    st.dataframe(change_display, use_container_width=True, hide_index=True, height=420)
with c6b:
    fig = px.bar(change_display.sort_values('% change'),
                 x='% change', y='Country', orientation='h',
                 color='% change', color_continuous_scale='RdYlGn_r',
                 template='simple_white',
                 labels={'% change': 'Change in CRC ASR, 2012→2022 (%)', 'Country': ''})
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=28, b=10),
                      coloraxis_showscale=False, paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.add_vline(x=0, line_color='#1f2937')
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<div class='takeaway'>"
    "<strong>Takeaway.</strong> China's CRC incidence rose <strong>+68%</strong> over the decade — the largest "
    "increase among major economies — coinciding with rapid Westernization of the Chinese diet. "
    "Hungary, Slovakia, and the U.S. all saw declines as screening uptake improved. India and Nigeria's small "
    "increases reflect aging populations rather than dietary change."
    "</div>",
    unsafe_allow_html=True,
)

# Bonus 2022 snapshot
st.markdown(
    "**2022 Snapshot: Incidence vs Mortality** "
    "<span class='tag tag-real'>IARC GLOBOCAN 2022</span>",
    unsafe_allow_html=True,
)
fig = px.scatter(globocan_df, x='incidence_asr_per_100k', y='mortality_asr_per_100k',
                 color='hdi_tier', hover_name='country', template='simple_white',
                 size='incidence_asr_per_100k', size_max=28,
                 color_discrete_map={'Very high': '#1d4ed8', 'High': '#3b82f6',
                                     'Medium': '#fbbf24', 'Low': '#dc2626'},
                 labels={'incidence_asr_per_100k': 'Incidence per 100K',
                         'mortality_asr_per_100k': 'Mortality per 100K',
                         'hdi_tier': 'HDI tier'})
fig.update_layout(height=420, margin=dict(l=10, r=10, t=28, b=10),
                  paper_bgcolor='#fff', plot_bgcolor='#fff')
fig.update_yaxes(gridcolor='#e5e7eb')
fig.update_xaxes(gridcolor='#e5e7eb')
st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "<div class='footnote'>Countries below the diagonal trend have better survival relative to incidence; "
    "those above (e.g., China, Russia, India) lose proportionally more patients to limited screening and access.</div>",
    unsafe_allow_html=True,
)

# ============================================================
# CHAPTER 7 — STAGE & OUTCOMES (Q6)
# ============================================================
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown(
    "<h2><span class='chapter-num'>7</span>Why Early Detection Matters</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='question-anchor'>"
    "<strong>Q6.</strong> Survival depends overwhelmingly on stage at diagnosis. The under-50 group is "
    "diagnosed later (no routine screening before age 45), which is why their mortality is rising even "
    "where screening works for older adults."
    "</div>",
    unsafe_allow_html=True,
)

c7a, c7b = st.columns([1.1, 1])
with c7a:
    st.markdown(
        "**5-Year Relative Survival by Stage** <span class='tag tag-real'>SEER 2014–2020</span>",
        unsafe_allow_html=True,
    )
    plot_seer = seer_df[seer_df['stage'] != 'All Stages Combined']
    fig = px.bar(plot_seer.sort_values('5_year_survival_rate', ascending=False),
                 x='stage', y='5_year_survival_rate',
                 color='5_year_survival_rate',
                 color_continuous_scale=['#dc2626', '#f59e0b', '#22c55e'],
                 template='simple_white', text='5_year_survival_rate',
                 labels={'5_year_survival_rate': '5-year survival (%)',
                         'stage': 'Stage at diagnosis'})
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                      coloraxis_showscale=False, paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_yaxes(gridcolor='#e5e7eb', range=[0, 105])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "<div class='footnote'>Cancer caught at the localized stage has 5× the survival of distant-stage disease.</div>",
        unsafe_allow_html=True,
    )

with c7b:
    st.markdown("**Stage definitions** <span class='tag'>reference</span>", unsafe_allow_html=True)
    st.dataframe(seer_df[['stage', '5_year_survival_rate', 'description']].rename(
        columns={'5_year_survival_rate': '5-yr survival %', 'description': 'Definition'}
    ), use_container_width=True, hide_index=True)
    st.markdown(
        "**Implication for early-onset patients:** Younger adults are routinely diagnosed at later stages "
        "because they fall outside historic screening guidelines. The U.S. Preventive Services Task Force "
        "lowered its recommended screening age from 50 to 45 in 2021 — partly in response to the rising "
        "early-onset trend in Chapter 1."
    )

# ============================================================
# DATASET INSPECTOR — rows, columns, snippet of every dataset
# ============================================================
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.subheader("Dataset Inspector")
st.caption(
    "A summary of every CSV powering this dashboard — row count, column count, full column list, "
    "and a snippet of the data. Useful for project writeups and reviewer verification."
)

datasets_inventory = [
    ("historical_crc_trends.csv", historical_df,
     "SEER 9 / ACS Cancer Statistics 2023",
     "1975–2023 yearly CRC incidence and mortality rates per 100K, stratified by age group (<50 vs 50+)."),
    ("cancer_totals_yearly.csv", cancer_totals_df,
     "ACS Cancer Facts & Figures (annual)",
     "All-U.S. new cancer cases vs CRC cases per year (2000–2024) with CRC share %."),
    ("state_crc_rates_real.csv", state_rates_df,
     "CDC State Cancer Statistics",
     "Age-adjusted CRC rates per 100K with race, age, and sex breakdowns for all 50 states + DC."),
    ("state_obesity_brfss.csv", obesity_df,
     "CDC BRFSS 2022",
     "Adult obesity prevalence (%) by state."),
    ("globocan_2022_crc.csv", globocan_df,
     "IARC GLOBOCAN 2022",
     "Latest country-level CRC age-standardized rates (incidence + mortality)."),
    ("globocan_historical.csv", globocan_hist_df,
     "IARC GLOBOCAN 2012 / 2018 / 2022",
     "Decade-long country CRC rate comparison across three GLOBOCAN editions."),
    ("seer_survival_by_stage.csv", seer_df,
     "SEER 2014–2020",
     "5-year relative survival rate by stage at diagnosis."),
    ("crc_risk_factors_real.csv", risk_real_df,
     "WCRF/AICR 2018, IARC, Larsson 2005",
     "Published meta-analysis relative risks (RR) with 95% CIs for modifiable factors."),
    ("food_consumption_country.csv", food_country_df,
     "FAO Food Balance Sheets 2020",
     "Per-capita country red meat, processed meat, fiber, fruit/vegetable consumption."),
    ("us_diet_trends.csv", us_diet_df,
     "USDA ERS + NHANES (Martínez Steele 2016)",
     "U.S. per-capita red meat, processed meat, sugar, ultra-processed % over time."),
    ("colorectal_only_combined.csv", state_counts_df,
     "ACS Cancer Facts & Figures (state extracts)",
     "Annual state-level CRC case and death counts (raw)."),
]

# Top-line summary table
inspector_summary = pd.DataFrame(
    [
        {
            "File": name,
            "Rows": f"{len(df):,}",
            "Columns": df.shape[1],
            "Source": source,
            "Description": desc,
        }
        for name, df, source, desc in datasets_inventory
    ]
)
total_rows = sum(len(df) for _, df, _, _ in datasets_inventory)
total_cols = sum(df.shape[1] for _, df, _, _ in datasets_inventory)

st.markdown(
    f"**Inventory totals:** {len(datasets_inventory)} datasets · "
    f"{total_rows:,} rows combined · {total_cols} columns combined"
)
st.dataframe(inspector_summary, use_container_width=True, hide_index=True)

st.markdown("**Per-dataset detail** — expand any row to see the full column list and a 5-row snippet.")
for name, df, source, desc in datasets_inventory:
    with st.expander(f"📄  {name}  —  {len(df):,} rows × {df.shape[1]} columns"):
        ic1, ic2, ic3 = st.columns(3)
        ic1.metric("Rows", f"{len(df):,}")
        ic2.metric("Columns", df.shape[1])
        ic3.metric("Source", source.split(",")[0])

        st.markdown(f"**Description:** {desc}")
        st.markdown(f"**Full source citation:** {source}")
        st.markdown(f"**Columns ({df.shape[1]}):** `{', '.join(df.columns.astype(str))}`")
        st.markdown("**Snippet (first 5 rows):**")
        st.dataframe(df.head(5), use_container_width=True, hide_index=True)

# ============================================================
# DATA PROVENANCE & SOURCES
# ============================================================
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.subheader("Data Provenance & Source Links")

source_df = pd.DataFrame(
    [
        ["historical_crc_trends.csv", "SEER 9 Registry / ACS Cancer Statistics 2023",
         "https://seer.cancer.gov/statfacts/html/colorect.html",
         "Real 1975–2023 incidence/mortality rates by age group"],
        ["cancer_totals_yearly.csv", "ACS Cancer Facts & Figures (annual)",
         "https://www.cancer.org/research/cancer-facts-statistics/all-cancer-facts-figures.html",
         "Total US new cancers + CRC cases per year"],
        ["state_crc_rates_real.csv", "CDC State Cancer Statistics",
         "https://www.cdc.gov/united-states-cancer-statistics/dataviz/index.html",
         "Age-adjusted CRC rates per 100K with race/age/sex breakdowns"],
        ["state_obesity_brfss.csv", "CDC BRFSS 2022",
         "https://www.cdc.gov/brfss/brfssprevalence/",
         "State adult obesity prevalence"],
        ["globocan_2022_crc.csv", "IARC GLOBOCAN 2022",
         "https://gco.iarc.fr/today",
         "Country age-standardized CRC rates (2022 release)"],
        ["globocan_historical.csv", "IARC GLOBOCAN 2012/2018/2022",
         "https://gco.iarc.fr/",
         "Decade-long country comparison across three GLOBOCAN editions"],
        ["seer_survival_by_stage.csv", "SEER 2014–2020",
         "https://seer.cancer.gov/statfacts/html/colorect.html",
         "5-year relative survival by stage at diagnosis"],
        ["crc_risk_factors_real.csv", "WCRF/AICR Continuous Update 2018; IARC; Larsson 2005",
         "https://www.wcrf.org/diet-activity-and-cancer/cancer-types/colorectal-cancer/",
         "Published relative risks with 95% CIs"],
        ["food_consumption_country.csv", "FAO Food Balance Sheets",
         "https://www.fao.org/faostat/en/#data/FBS",
         "Per-capita red meat, processed meat, fiber, fruit/veg by country"],
        ["us_diet_trends.csv", "USDA ERS Food Availability + NHANES (Martínez Steele 2016)",
         "https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/",
         "U.S. per-capita red meat, sugar, ultra-processed share over time"],
        ["colorectal_only_combined.csv", "ACS Cancer Facts & Figures (state-level extracts)",
         "https://www.cancer.org/research/cancer-facts-statistics/all-cancer-facts-figures.html",
         "Annual state CRC case/death counts"],
    ],
    columns=["File", "Source", "URL", "Purpose"],
)
st.dataframe(source_df, use_container_width=True, hide_index=True,
             column_config={"URL": st.column_config.LinkColumn("URL")})

st.caption(
    "Dashboard created for DSC 205 Final Project · "
    "All visualizations use real public-health data (CDC, ACS, SEER, IARC, WCRF, FAO, USDA, BRFSS). "
    "See SOURCES.md in the project folder for a flat list of citations and links."
)
