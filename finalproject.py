import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================================================
# Page config & styling — matches skeleton aesthetic
# ============================================================
st.set_page_config(page_title="Colorectal Cancer Disparities Dashboard", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.0rem;
            padding-bottom: 2.2rem;
            max-width: 1450px;
        }
        h1, h2, h3 { letter-spacing: -0.02em; }
        .metric-box {
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            background: #ffffff;
            padding: 16px 16px 14px 16px;
            min-height: 96px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }
        .tag {
            display: inline-block;
            padding: 3px 9px;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
            margin-left: 8px;
            background: #dbeafe;
            color: #1d4ed8;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Data loading — REAL public-health datasets
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
def load_historical():
    return pd.read_csv(os.path.join(DATA_DIR, "historical_crc_trends.csv"))

@st.cache_data
def load_sex_trend():
    return pd.read_csv(os.path.join(DATA_DIR, "crc_sex_trend.csv"))

@st.cache_data
def load_seer_survival():
    return pd.read_csv(os.path.join(DATA_DIR, "seer_survival_by_stage.csv"))

@st.cache_data
def load_food_country():
    return pd.read_csv(os.path.join(DATA_DIR, "food_consumption_country.csv"))

@st.cache_data
def load_risk_factors():
    return pd.read_csv(os.path.join(DATA_DIR, "crc_risk_factors_real.csv"))

@st.cache_data
def load_cancer_totals():
    return pd.read_csv(os.path.join(DATA_DIR, "cancer_totals_yearly.csv"))

@st.cache_data
def load_obesity():
    return pd.read_csv(os.path.join(DATA_DIR, "state_obesity_brfss.csv"))

@st.cache_data
def load_globocan_historical():
    return pd.read_csv(os.path.join(DATA_DIR, "globocan_historical.csv"))

@st.cache_data
def load_us_diet_trends():
    return pd.read_csv(os.path.join(DATA_DIR, "us_diet_trends.csv"))

@st.cache_data
def load_risk_by_age():
    return pd.read_csv(os.path.join(DATA_DIR, "risk_factors_by_age_group.csv"))

@st.cache_data
def load_risk_by_level():
    return pd.read_csv(os.path.join(DATA_DIR, "crc_risk_factors_by_level.csv"))

@st.cache_data
def load_under50_subgroups():
    return pd.read_csv(os.path.join(DATA_DIR, "under50_subgroups.csv"))

@st.cache_data
def load_prediction_models():
    return pd.read_csv(os.path.join(DATA_DIR, "prediction_models_under50.csv"))

@st.cache_data
def load_stage_by_age():
    return pd.read_csv(os.path.join(DATA_DIR, "stage_at_diagnosis_by_age.csv"))

@st.cache_data
def load_early_onset_share():
    return pd.read_csv(os.path.join(DATA_DIR, "early_onset_share.csv"))

@st.cache_data
def load_stage_by_sex():
    return pd.read_csv(os.path.join(DATA_DIR, "stage_by_sex.csv"))

# Region & abbreviation maps
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

# Load datasets
state_counts_df = load_state_counts()
state_rates_df = load_state_rates_real()
globocan_df = load_globocan()
globocan_hist_df = load_globocan_historical()
historical_df = load_historical()
sex_trend_df = load_sex_trend()
seer_df = load_seer_survival()
food_country_df = load_food_country()
risk_real_df = load_risk_factors()
cancer_totals_df = load_cancer_totals()
obesity_df = load_obesity()
us_diet_df = load_us_diet_trends()
risk_by_age_df = load_risk_by_age()
risk_by_level_df = load_risk_by_level()
under50_subgroups_df = load_under50_subgroups()
prediction_models_df = load_prediction_models()
stage_by_age_df = load_stage_by_age()
early_onset_share_df = load_early_onset_share()
stage_by_sex_df = load_stage_by_sex()

# Augment + normalize
state_counts_df['region'] = state_counts_df['state'].map(STATE_TO_REGION)
state_counts_df['state_code'] = state_counts_df['state'].map(STATE_ABBREV)
state_rates_df['region'] = state_rates_df['state'].map(STATE_TO_REGION)
state_rates_df['state_code'] = state_rates_df['state'].map(STATE_ABBREV)

pop_lookup = state_rates_df[['state', 'population']].drop_duplicates()
state_counts_df = state_counts_df.merge(pop_lookup, on='state', how='left')
state_counts_df['rate_per_100k'] = (state_counts_df['value'] / state_counts_df['population']) * 100000

# ============================================================
# Sidebar — matches skeleton's filter set
# ============================================================
st.sidebar.title("Sidebar Widgets")

available_years = sorted(state_counts_df['year'].unique())
year_range = st.sidebar.slider(
    "📅 Year range",
    min_value=int(min(available_years)),
    max_value=int(max(available_years)),
    value=(int(min(available_years)), int(max(available_years))),
)

regions = ['All'] + sorted(state_counts_df['region'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("🌎 Region filter", regions)

selected_metric = st.sidebar.selectbox("📊 Metric", ['cases', 'deaths'])

selected_sex = st.sidebar.selectbox("👥 Sex", ['Both', 'Male', 'Female'])

display_mode = st.sidebar.radio(
    "🧹 Normalization",
    ['Rate per 100K', 'Raw counts'],
    help="Per-capita rates control for state size and reveal true disparities.",
)

# Apply filters
filtered = state_counts_df[
    (state_counts_df['year'] >= year_range[0]) &
    (state_counts_df['year'] <= year_range[1])
]
if selected_region != 'All':
    filtered = filtered[filtered['region'] == selected_region]
all_sex = filtered[filtered['sex'].isin(['All', 'Both'])]

value_col = 'rate_per_100k' if display_mode == 'Rate per 100K' else 'value'
value_label = 'Rate per 100K' if display_mode == 'Rate per 100K' else 'Count'

# ============================================================
# Header — matches skeleton
# ============================================================
st.title("Colorectal Cancer Disparities Dashboard")
st.caption("Final project · all visualizations powered by real public-health data")

col1, col2 = st.columns([1.25, 1])
with col1:
    st.markdown("**Project title:** Colorectal Cancer Disparities Dashboard")
    st.markdown(
        "**Why this matters:** Colorectal cancer brings together a lot of stories at once — who gets it, "
        "where they live, what they eat, and how things have changed over time. Since the mid-1970s, more "
        "young adults under 50 are being diagnosed, even though older adults have seen big improvements "
        "thanks to screening. We built this dashboard to dig into those patterns using real public-health data."
    )
with col2:
    st.info(
        "Every chart on this page uses real data from CDC, the American Cancer Society, SEER, the World "
        "Health Organization (IARC), the World Cancer Research Fund, and the FAO. No synthetic numbers."
    )

with st.expander("Questions we want to answer", expanded=True):
    questions = [
        "Which lifestyle habits and personal factors are most strongly tied to getting colorectal cancer?",
        "What's different about people under 50 who get diagnosed compared to those 50 and older?",
        "Among younger patients, are there different 'types' of people who tend to get diagnosed?",
        "Can we predict a younger person's risk from their lifestyle and background?",
        "How do where you live and your income or community affect your chances?",
        "Does stage at diagnosis (how early it's caught) and survival differ by age, gender, or background?",
    ]
    for i, q in enumerate(questions, start=1):
        st.markdown(f"**Q{i}.** {q}")

# ============================================================
# Dashboard
# ============================================================
st.subheader("Dashboard")
st.caption("The same visualizations from our project plan, now powered by real data.")

# ----- KPI row -----
total_cases = all_sex[all_sex['metric'] == 'cases']['value'].sum()
total_deaths = all_sex[all_sex['metric'] == 'deaths']['value'].sum()

state_rate_avg = (
    all_sex[all_sex['metric'] == selected_metric]
    .groupby('state')['rate_per_100k'].mean().sort_values(ascending=False)
)
if len(state_rate_avg):
    highest_state = state_rate_avg.idxmax()
    highest_value = state_rate_avg.max()
else:
    highest_state = "N/A"
    highest_value = 0

yearly_totals = all_sex[all_sex['metric'] == selected_metric].groupby('year')['value'].sum()
if len(yearly_totals) > 1:
    avg_change = yearly_totals.diff().mean()
    pct_change = ((yearly_totals.iloc[-1] - yearly_totals.iloc[0]) / yearly_totals.iloc[0] * 100
                  if yearly_totals.iloc[0] > 0 else 0)
else:
    avg_change = 0
    pct_change = 0

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Total new cases</div>"
        f"<div style='margin-top:14px;font-size:1.5rem;font-weight:bold;color:#1d4ed8'>{total_cases:,.0f}</div>"
        f"<div style='font-size:0.78rem;color:#6b7280'>across the years and region you've selected</div></div>",
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Total deaths</div>"
        f"<div style='margin-top:14px;font-size:1.5rem;font-weight:bold;color:#dc2626'>{total_deaths:,.0f}</div>"
        f"<div style='font-size:0.78rem;color:#6b7280'>across the years and region you've selected</div></div>",
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>State with highest rate</div>"
        f"<div style='margin-top:14px;font-size:1.2rem;font-weight:bold;color:#059669'>{highest_state}</div>"
        f"<div style='font-size:0.85rem;color:#6b7280'>{highest_value:.1f} per 100,000 people ({selected_metric})</div></div>",
        unsafe_allow_html=True,
    )
with k4:
    change_color = '#dc2626' if pct_change > 0 else '#059669'
    direction_word = 'rose' if pct_change > 0 else 'fell'
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Change over period</div>"
        f"<div style='margin-top:14px;font-size:1.2rem;font-weight:bold;color:{change_color}'>{pct_change:+.1f}%</div>"
        f"<div style='font-size:0.85rem;color:#6b7280'>{direction_word} on average {avg_change:+,.0f}/year</div></div>",
        unsafe_allow_html=True,
    )

# ----- Chart row 1 -----
r1_left, r1_right = st.columns([1.35, 1])

with r1_left:
    st.markdown("**Under 50 vs 50 and older, over time** <span class='tag'>line chart</span>", unsafe_allow_html=True)
    st.caption(
        "Number of new colorectal cancer diagnoses per 100,000 people each year, "
        "from 1975 to 2023. The two age groups are heading in opposite directions."
    )

    fig = px.line(
        historical_df, x='year', y='incidence_rate', color='age_group',
        markers=True, template='simple_white',
        color_discrete_map={'<50': '#dc2626', '50+': '#3b82f6'},
        labels={'incidence_rate': 'Incidence per 100K', 'age_group': 'Age group'},
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(height=315, margin=dict(l=10, r=10, t=28, b=10),
                      legend_title_text='Age group',
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='Year', showgrid=False)
    fig.update_yaxes(title_text='Incidence per 100K', gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)

with r1_right:
    st.markdown("**Men vs women, over time** <span class='tag'>line chart</span>", unsafe_allow_html=True)
    st.caption(
        "New colorectal cancer cases per 100,000 people each year, comparing men and women. "
        "Both have improved overall, but men consistently get diagnosed more often."
    )

    sex_to_show = sex_trend_df.copy()
    if selected_sex != 'Both':
        sex_to_show = sex_to_show[sex_to_show['sex'] == selected_sex]

    fig = px.line(
        sex_to_show, x='year', y='incidence_rate', color='sex',
        markers=True, template='simple_white',
        color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899'},
    )
    fig.update_layout(height=315, margin=dict(l=10, r=10, t=28, b=10),
                      legend_title_text='', paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='Year', showgrid=False)
    fig.update_yaxes(title_text='Incidence per 100K', gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)

# ----- Share of CRC: over 55 vs under 55 over time (full width) -----
st.markdown(
    "**The age mix of CRC patients is shifting — older share down, younger share up** "
    "<span class='tag'>line chart</span>",
    unsafe_allow_html=True,
)
st.caption(
    "Of every 100 colorectal cancer diagnoses each year, how many were in adults 55 and older "
    "versus under 55. The older group's share of CRC has been falling (89% → 78%) while the under-55 "
    "share has been climbing (11% → 22%). The two lines are converging — meaning younger patients now "
    "make up more than 1 in 5 colorectal cancer cases."
)

fig = px.line(
    early_onset_share_df,
    x='year', y='share_of_crc_pct', color='age_group',
    markers=True, template='simple_white',
    color_discrete_map={'Over 55': '#3b82f6', 'Under 55': '#dc2626'},
    category_orders={'age_group': ['Over 55', 'Under 55']},
    labels={'share_of_crc_pct': 'Share of all CRC diagnoses (%)',
            'year': 'Year', 'age_group': 'Age group'},
    text='share_of_crc_pct',
)
fig.update_traces(line=dict(width=3), marker=dict(size=10),
                  texttemplate='%{text}%', textposition='top center')
fig.update_layout(height=420, margin=dict(l=10, r=10, t=28, b=10),
                  legend_title_text='Age group',
                  paper_bgcolor='#fff', plot_bgcolor='#fff',
                  hovermode='x unified')
fig.update_xaxes(gridcolor='#e5e7eb')
fig.update_yaxes(gridcolor='#e5e7eb', range=[0, 100])
st.plotly_chart(fig, use_container_width=True)

# ----- Chart row 2 -----
r2_left, r2_right = st.columns([1.15, 1.05])

with r2_left:
    st.markdown("**How the four U.S. regions compare** <span class='tag'>line chart</span>", unsafe_allow_html=True)
    st.caption(
        "Each line is a U.S. region (Northeast, Midwest, South, West). "
        "Are some parts of the country doing better than others?"
    )

    region_data = all_sex[all_sex['metric'] == selected_metric].copy().dropna(subset=['region'])
    region_pop = region_data.groupby(['year', 'region']).agg(
        total_value=('value', 'sum'), total_pop=('population', 'sum')
    ).reset_index()
    region_pop['rate_per_100k'] = (region_pop['total_value'] / region_pop['total_pop']) * 100000

    y_col = 'rate_per_100k' if display_mode == 'Rate per 100K' else 'total_value'
    fig = px.line(
        region_pop, x='year', y=y_col, color='region',
        markers=True, template='simple_white',
    )
    fig.update_layout(height=315, margin=dict(l=10, r=10, t=28, b=10),
                      legend_title_text='', paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='Year', showgrid=False)
    fig.update_yaxes(title_text=value_label, gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)

with r2_right:
    st.markdown("**Top 10 states** <span class='tag'>bar chart</span>", unsafe_allow_html=True)
    st.caption(
        "The 10 states with the most colorectal cancer. Use the sidebar to switch between "
        "'rate per 100,000 people' (fairer for small states) and total counts."
    )

    if display_mode == 'Rate per 100K':
        rank_df = state_rates_df.nlargest(10, 'crc_rate_total')[['state', 'crc_rate_total']].copy()
        rank_df.columns = ['state', 'value']
        x_label = 'Rate per 100K (CDC)'
    else:
        rank_df = (all_sex[all_sex['metric'] == selected_metric]
                   .groupby('state')['value'].sum().nlargest(10).reset_index())
        x_label = f'Total {selected_metric}'

    fig = px.bar(
        rank_df.sort_values('value', ascending=True),
        x='value', y='state', orientation='h',
        template='simple_white', color='value', color_continuous_scale='Blues',
    )
    fig.update_layout(height=315, margin=dict(l=10, r=10, t=28, b=10),
                      showlegend=False, coloraxis_showscale=False,
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text=x_label, gridcolor='#e5e7eb')
    fig.update_yaxes(title_text='')
    st.plotly_chart(fig, use_container_width=True)

# ----- Chart row 3 -----
r3_left, r3_right = st.columns([1.2, 1])

with r3_left:
    st.markdown("**Diagnoses vs deaths in each state** <span class='tag'>scatter plot</span>", unsafe_allow_html=True)
    st.caption(
        "Each dot is a state. Further right = more diagnoses; higher up = more deaths. "
        "States that fall off the typical pattern stand out."
    )

    cases_by = (all_sex[all_sex['metric'] == 'cases']
                .groupby(['state', 'region'])['value'].sum().reset_index())
    deaths_by = (all_sex[all_sex['metric'] == 'deaths']
                 .groupby('state')['value'].sum().reset_index())
    scatter_data = cases_by.merge(deaths_by, on='state', suffixes=('_cases', '_deaths'))
    scatter_data.columns = ['state', 'region', 'cases', 'deaths']
    scatter_data = scatter_data.dropna()

    fig = px.scatter(
        scatter_data, x='cases', y='deaths', color='region',
        hover_name='state', template='simple_white',
    )
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(height=315, margin=dict(l=10, r=10, t=28, b=10),
                      legend_title_text='Region', paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='Cases', gridcolor='#e5e7eb')
    fig.update_yaxes(title_text='Deaths', gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)

with r3_right:
    st.markdown("**Black vs White Americans** <span class='tag'>bar chart</span>", unsafe_allow_html=True)
    st.caption(
        "Average diagnoses per 100,000 people, by race. "
        "Black Americans face notably higher rates than White Americans — one of the biggest gaps in any cancer."
    )

    # Compute race-level averages from real CDC data (drop suppressed zero values)
    race_means = pd.DataFrame({
        'Race': ['Black', 'White', 'Hispanic', 'Asian', 'Indigenous'],
        'rate': [
            state_rates_df.loc[state_rates_df['crc_rate_black'] > 0, 'crc_rate_black'].mean(),
            state_rates_df.loc[state_rates_df['crc_rate_white'] > 0, 'crc_rate_white'].mean(),
            state_rates_df.loc[state_rates_df['crc_rate_hispanic'] > 0, 'crc_rate_hispanic'].mean(),
            state_rates_df.loc[state_rates_df['crc_rate_asian'] > 0, 'crc_rate_asian'].mean(),
            state_rates_df.loc[state_rates_df['crc_rate_indigenous'] > 0, 'crc_rate_indigenous'].mean(),
        ],
    }).sort_values('rate', ascending=True)

    fig = px.bar(
        race_means, x='rate', y='Race', orientation='h',
        template='simple_white', text='rate',
        color='Race',
        color_discrete_map={
            'Black': '#dc2626', 'White': '#3b82f6',
            'Hispanic': '#f59e0b', 'Asian': '#10b981', 'Indigenous': '#a855f7',
        },
    )
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(height=315, margin=dict(l=10, r=10, t=28, b=10),
                      showlegend=False, paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='Diagnoses per 100,000 people', gridcolor='#e5e7eb')
    fig.update_yaxes(title_text='')
    st.plotly_chart(fig, use_container_width=True)

# ----- Chart row 4 -----
r4_left, r4_right = st.columns([1.2, 1])

with r4_left:
    st.markdown("**Map: how common CRC is in each state** <span class='tag'>map</span>", unsafe_allow_html=True)
    st.caption(
        "Diagnoses per 100,000 people, scaled fairly so big states aren't favored. "
        "Darker red = more common. Watch how Mississippi, Kentucky, and West Virginia stand out."
    )

    fig = px.choropleth(
        state_rates_df, locations='state_code', locationmode='USA-states',
        color='crc_rate_total', scope='usa', hover_name='state',
        color_continuous_scale='Reds', template='simple_white',
        labels={'crc_rate_total': 'CRC per 100K'},
    )
    fig.update_layout(height=315, margin=dict(l=10, r=10, t=28, b=10),
                      paper_bgcolor='#fff', plot_bgcolor='#fff',
                      coloraxis_colorbar_title='per 100K')
    st.plotly_chart(fig, use_container_width=True)

with r4_right:
    st.markdown("**Why catching it early matters** <span class='tag'>bar chart</span>", unsafe_allow_html=True)
    st.caption(
        "Out of 100 people diagnosed, how many are still alive 5 years later — based on how far the cancer "
        "had spread when found. The earlier it's caught, the better the odds."
    )

    plot_seer = seer_df[seer_df['stage'] != 'All Stages Combined']
    fig = px.bar(
        plot_seer.sort_values('5_year_survival_rate', ascending=False),
        x='stage', y='5_year_survival_rate',
        color='5_year_survival_rate',
        color_continuous_scale=['#dc2626', '#f59e0b', '#22c55e'],
        template='simple_white', text='5_year_survival_rate',
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=315, margin=dict(l=10, r=10, t=28, b=10),
                      coloraxis_showscale=False,
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='Stage')
    fig.update_yaxes(title_text='5-year survival %', gridcolor='#e5e7eb', range=[0, 105])
    st.plotly_chart(fig, use_container_width=True)

# ----- Chart row 5 — international context -----
r5_left, r5_right = st.columns([1, 1.1])

with r5_left:
    st.markdown(
        "**International: more developed countries get more CRC** "
        "<span class='tag'>bar chart</span>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Average diagnoses per 100,000 people, grouped by how developed a country is "
        "(UN Human Development Index). More developed countries get diagnosed more often. "
        "Colors match the Healthcare Access chart below — pair the two together to see "
        "the full picture."
    )

    hdi_means = (
        globocan_df.groupby('hdi_tier')['incidence_asr_per_100k'].mean().reset_index()
    )
    hdi_order = ['Low', 'Medium', 'High', 'Very high']
    hdi_means['hdi_tier'] = pd.Categorical(hdi_means['hdi_tier'], categories=hdi_order, ordered=True)
    hdi_means = hdi_means.sort_values('hdi_tier')

    fig = px.bar(
        hdi_means, x='hdi_tier', y='incidence_asr_per_100k',
        text='incidence_asr_per_100k',
        color='hdi_tier',
        template='simple_white',
        color_discrete_map={'Very high': '#22c55e', 'High': '#84cc16',
                            'Medium': '#f59e0b', 'Low': '#dc2626'},
    )
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                      showlegend=False,
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='How developed the country is')
    fig.update_yaxes(title_text='Diagnoses per 100,000 people', gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)

with r5_right:
    st.markdown(
        "**Country food habits and CRC** "
        "<span class='tag'>bubble chart</span>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Each circle is a country. The further right, the more red meat people eat per year. "
        "The higher up, the more colorectal cancer they get. Bigger circles = more deaths from it."
    )

    bubble_df = food_country_df.merge(globocan_df, on='country', how='inner')
    fig = px.scatter(
        bubble_df,
        x='red_meat_kg_per_capita_yr',
        y='incidence_asr_per_100k',
        size='mortality_asr_per_100k',
        color='hdi_tier',
        hover_name='country',
        size_max=38,
        template='simple_white',
        color_discrete_map={'Very high': '#22c55e', 'High': '#84cc16',
                            'Medium': '#f59e0b', 'Low': '#dc2626'},
    )
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                      legend_title_text='How developed',
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='Red meat eaten per person per year (kg)', gridcolor='#e5e7eb')
    fig.update_yaxes(title_text='Diagnoses per 100,000 people', gridcolor='#e5e7eb')

    rcorr = bubble_df[['red_meat_kg_per_capita_yr', 'incidence_asr_per_100k']].corr().iloc[0, 1]
    fig.add_annotation(
        x=bubble_df['red_meat_kg_per_capita_yr'].max() * 0.65,
        y=bubble_df['incidence_asr_per_100k'].max() * 0.05,
        text=f"<b>Strong link (r = {rcorr:.2f})</b>",
        showarrow=False, font=dict(size=12, color='#1f2937'),
        bgcolor='white', bordercolor='#9ca3af', borderwidth=1,
    )
    st.plotly_chart(fig, use_container_width=True)

# ----- Chart row 6 — Lifestyle risk factors (forest + by age group) -----
r6_left, r6_right = st.columns([1, 1])

with r6_left:
    st.markdown(
        "**Which habits matter most?** "
        "<span class='tag'>risk factor chart</span>",
        unsafe_allow_html=True,
    )
    st.caption(
        "How much each habit or condition changes your chances of colorectal cancer. "
        "The dashed line is 'no effect'. Red bars to the right = raises chances. "
        "Green bars to the left = lowers chances. The further from the line, the bigger the effect."
    )

    risk_sorted = risk_real_df.copy()
    risk_sorted['err_low'] = risk_sorted['relative_risk'] - risk_sorted['ci_lower']
    risk_sorted['err_high'] = risk_sorted['ci_upper'] - risk_sorted['relative_risk']
    risk_sorted = risk_sorted.sort_values('relative_risk')

    forest_colors = ['#dc2626' if d == 'Increases' else '#059669' for d in risk_sorted['direction']]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=risk_sorted['relative_risk'], y=risk_sorted['risk_factor'],
        mode='markers',
        marker=dict(size=14, color=forest_colors, line=dict(color='#1f2937', width=1)),
        error_x=dict(type='data', symmetric=False,
                     array=risk_sorted['err_high'], arrayminus=risk_sorted['err_low'],
                     color='#9ca3af', thickness=2, width=8),
        text=[f"{d}: about {abs(rr-1)*100:.0f}% {('higher' if rr>1 else 'lower')} risk"
              for rr, d in zip(risk_sorted['relative_risk'], risk_sorted['direction'])],
        hovertemplate='%{y}<br>%{text}<extra></extra>',
        showlegend=False,
    ))
    fig.add_vline(x=1.0, line_dash='dash', line_color='#9ca3af',
                  annotation_text='No effect', annotation_position='top')
    fig.update_layout(template='simple_white', height=420,
                      margin=dict(l=10, r=10, t=28, b=10),
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='Risk score (1.0 = no effect)', gridcolor='#e5e7eb')
    fig.update_yaxes(title_text='')
    st.plotly_chart(fig, use_container_width=True)

with r6_right:
    st.markdown(
        "**Risk factors: under 50 vs 50 and older** "
        "<span class='tag'>grouped bar chart</span>",
        unsafe_allow_html=True,
    )
    st.caption(
        "How common each risk factor is in patients diagnosed under 50 versus 50 and older. "
        "Younger patients more often have a family history or genetic syndrome; "
        "older patients more often have smoking history and diabetes."
    )

    fig = px.bar(
        risk_by_age_df,
        x='risk_factor', y='prevalence_pct',
        color='age_group', barmode='group',
        template='simple_white',
        text='prevalence_pct',
        color_discrete_map={'<50': '#f59e0b', '50+': '#3b82f6'},
        labels={'risk_factor': '', 'prevalence_pct': 'Share of patients (%)',
                'age_group': 'Age group'},
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=28, b=10),
                      legend_title_text='Age group',
                      paper_bgcolor='#fff', plot_bgcolor='#fff',
                      xaxis_tickangle=-30)
    fig.update_yaxes(gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)

# ----- Chart row 7 — Healthcare access + Risk-by-level -----
r7_left, r7_right = st.columns([1, 1])

with r7_left:
    st.markdown(
        "**Healthcare access: developed vs underdeveloped countries** "
        "<span class='tag'>bar chart</span>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Of every 100 people diagnosed, how many die from the disease — grouped by country "
        "development. The flip side of the chart above: green countries get diagnosed more, "
        "but they also save far more lives. Red countries get diagnosed less, but most cases "
        "still end in death."
    )

    # Compute mortality-to-incidence ratio (real cancer epidemiology metric for access)
    hdi_access = globocan_df.groupby('hdi_tier').agg(
        incidence=('incidence_asr_per_100k', 'mean'),
        mortality=('mortality_asr_per_100k', 'mean'),
    ).reset_index()
    hdi_access['death_share_pct'] = (hdi_access['mortality'] / hdi_access['incidence']) * 100
    hdi_order = ['Low', 'Medium', 'High', 'Very high']
    hdi_access['hdi_tier'] = pd.Categorical(
        hdi_access['hdi_tier'], categories=hdi_order, ordered=True
    )
    hdi_access = hdi_access.sort_values('hdi_tier')

    fig = px.bar(
        hdi_access, x='hdi_tier', y='death_share_pct',
        text='death_share_pct',
        color='hdi_tier',
        template='simple_white',
        color_discrete_map={'Very high': '#22c55e', 'High': '#84cc16',
                            'Medium': '#f59e0b', 'Low': '#dc2626'},
    )
    fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                      showlegend=False,
                      paper_bgcolor='#fff', plot_bgcolor='#fff')
    fig.update_xaxes(title_text='How developed the country is')
    fig.update_yaxes(title_text='Share of cases that end in death (%)',
                     gridcolor='#e5e7eb', range=[0, 80])
    st.plotly_chart(fig, use_container_width=True)

with r7_right:
    st.markdown(
        "**Risk factors broken down by overall risk level** "
        "<span class='tag'>grouped bar chart</span>",
        unsafe_allow_html=True,
    )
    st.caption(
        "How common each habit is among people classified as high, medium, or low risk for "
        "colorectal cancer. The pattern is exactly what you'd expect — high-risk people are more "
        "likely to be obese, smoke, drink heavily, and live a sedentary lifestyle."
    )

    fig = px.bar(
        risk_by_level_df,
        x='risk_factor', y='prevalence_pct',
        color='risk_level', barmode='group',
        template='simple_white',
        text='prevalence_pct',
        color_discrete_map={'High': '#dc2626', 'Medium': '#f59e0b', 'Low': '#22c55e'},
        category_orders={'risk_level': ['High', 'Medium', 'Low']},
        labels={'risk_factor': '', 'prevalence_pct': 'Share with this habit (%)',
                'risk_level': 'Risk level'},
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                      legend_title_text='Risk level',
                      paper_bgcolor='#fff', plot_bgcolor='#fff',
                      xaxis_tickangle=-15)
    fig.update_yaxes(gridcolor='#e5e7eb', range=[0, 65])
    st.plotly_chart(fig, use_container_width=True)

# ----- Chart row 8 — Q3 (subgroups), full width -----
st.markdown(
    "**Q3 — Types of patients under 50** "
    "<span class='tag'>bar chart</span>",
    unsafe_allow_html=True,
)
st.caption(
    "When someone under 50 is diagnosed, what's the most likely reason? "
    "Younger patients fall into a few clear groups — not just 'bad luck'."
)

sg = under50_subgroups_df.sort_values('share_pct')
fig = px.bar(
    sg, x='share_pct', y='subgroup', orientation='h',
    color='subgroup_type',
    text='share_pct',
    template='simple_white',
    color_discrete_map={
        'Genetic': '#7c3aed', 'Lifestyle': '#f59e0b',
        'Medical': '#3b82f6', 'Unknown': '#9ca3af',
    },
    labels={'share_pct': 'Share of under-50 patients (%)',
            'subgroup': '', 'subgroup_type': 'Type'},
)
fig.update_traces(texttemplate='%{text}%', textposition='outside')
fig.update_layout(height=360, margin=dict(l=10, r=10, t=28, b=10),
                  legend_title_text='Type',
                  paper_bgcolor='#fff', plot_bgcolor='#fff')
fig.update_xaxes(gridcolor='#e5e7eb', range=[0, 38])
st.plotly_chart(fig, use_container_width=True)

# ----- Chart row 9 — Q6 (stage at diagnosis by age), full width -----
st.markdown(
    "**Q6 — When the cancer is found, by age** "
    "<span class='tag'>stacked bar</span>",
    unsafe_allow_html=True,
)
st.caption(
    "How far the cancer has already spread when it's first found. Younger patients are "
    "much more likely to be diagnosed after it has spread to other organs — they're not "
    "routinely screened, so it's caught later."
)

fig = px.bar(
    stage_by_age_df,
    x='age_group', y='share_pct',
    color='stage', barmode='stack',
    template='simple_white',
    text='share_pct',
    color_discrete_map={
        'Localized': '#22c55e',
        'Regional': '#f59e0b',
        'Distant (metastatic)': '#dc2626',
    },
    category_orders={'stage': ['Localized', 'Regional', 'Distant (metastatic)']},
    labels={'age_group': 'Age group', 'share_pct': 'Share of patients (%)',
            'stage': 'How far it had spread'},
)
fig.update_traces(texttemplate='%{text}%', textposition='inside')
fig.update_layout(height=360, margin=dict(l=10, r=10, t=28, b=10),
                  legend_title_text='Stage when found',
                  paper_bgcolor='#fff', plot_bgcolor='#fff')
fig.update_yaxes(gridcolor='#e5e7eb')
st.plotly_chart(fig, use_container_width=True)

# ----- Stage at diagnosis, broken down by sex (full width) -----
st.markdown(
    "**Q6 — When the cancer is found, by sex** "
    "<span class='tag'>stacked bar</span>",
    unsafe_allow_html=True,
)
st.caption(
    "Same idea as the chart above, but now broken down by sex. The differences are smaller than "
    "by age — men are slightly more likely to be diagnosed at a metastatic stage (25% vs 22% for "
    "women), partly because men are also less likely to keep up with screening."
)

fig = px.bar(
    stage_by_sex_df,
    x='sex', y='share_pct',
    color='stage', barmode='stack',
    template='simple_white',
    text='share_pct',
    color_discrete_map={
        'Localized': '#22c55e',
        'Regional': '#f59e0b',
        'Distant (metastatic)': '#dc2626',
    },
    category_orders={'stage': ['Localized', 'Regional', 'Distant (metastatic)']},
    labels={'sex': 'Sex', 'share_pct': 'Share of patients (%)',
            'stage': 'How far it had spread'},
)
fig.update_traces(texttemplate='%{text}%', textposition='inside')
fig.update_layout(height=380, margin=dict(l=10, r=10, t=28, b=10),
                  legend_title_text='Stage when found',
                  paper_bgcolor='#fff', plot_bgcolor='#fff')
fig.update_yaxes(gridcolor='#e5e7eb')
st.plotly_chart(fig, use_container_width=True)

# ----- Chart row 10 — Q4 (prediction skill), full width -----
st.markdown(
    "**Q4 — How well can we predict who'll get it?** "
    "<span class='tag'>bar chart</span>",
    unsafe_allow_html=True,
)
st.caption(
    "Different prediction models, ranked by accuracy. 0.5 = random guessing; "
    "1.0 = perfect prediction. Lifestyle data alone gets us partway; adding "
    "screening history and genetics improves it more."
)

pm = prediction_models_df.copy().sort_values('auc')
pm['color'] = pm['auc'].apply(
    lambda v: '#dc2626' if v < 0.6 else ('#f59e0b' if v < 0.7 else '#22c55e')
)
fig = go.Figure()
fig.add_trace(go.Bar(
    x=pm['auc'], y=pm['model'], orientation='h',
    marker=dict(color=pm['color']),
    text=[f"{v:.2f}" for v in pm['auc']],
    textposition='outside',
    showlegend=False,
))
fig.add_vline(x=0.5, line_dash='dash', line_color='#9ca3af',
              annotation_text='Random guess', annotation_position='top')
fig.update_layout(template='simple_white', height=360,
                  margin=dict(l=10, r=10, t=28, b=10),
                  paper_bgcolor='#fff', plot_bgcolor='#fff',
                  xaxis_title='Prediction skill (0.5 = guessing, 1.0 = perfect)',
                  yaxis_title='')
fig.update_xaxes(gridcolor='#e5e7eb', range=[0.45, 0.85])
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Pre-processing notes — matches skeleton
# ============================================================
st.subheader("How we cleaned and combined the data")
pre_df = pd.DataFrame(
    [
        ["Made state names match across data sources", "So we could combine CDC, ACS, and BRFSS data correctly"],
        ["Converted raw counts to 'per 100,000 people'", "So small states aren't unfairly compared to big ones"],
        ["Removed national totals from state-level data", "So country-wide numbers don't drown out state details"],
        ["Replaced a synthetic dataset with real WHO data", "So our country comparisons reflect real disease patterns"],
        ["Joined food and cancer data by country", "So we could see if eating habits track with disease rates"],
    ],
    columns=["What we did", "Why we did it"],
)
st.dataframe(pre_df, use_container_width=True, hide_index=True)

# ============================================================
# Sources
# ============================================================
st.subheader("Source links")
links_df = pd.DataFrame(
    [
        ["SEER (Colorectal Cancer Stat Facts)", "https://seer.cancer.gov/statfacts/html/colorect.html"],
        ["CDC State Cancer Statistics", "https://www.cdc.gov/united-states-cancer-statistics/dataviz/index.html"],
        ["ACS Cancer Facts & Figures", "https://www.cancer.org/research/cancer-facts-statistics/all-cancer-facts-figures.html"],
        ["IARC GLOBOCAN", "https://gco.iarc.fr/today"],
        ["WCRF/AICR Colorectal Cancer", "https://www.wcrf.org/diet-activity-and-cancer/cancer-types/colorectal-cancer/"],
        ["CDC BRFSS Prevalence", "https://www.cdc.gov/brfss/brfssprevalence/"],
        ["FAO Food Balance Sheets", "https://www.fao.org/faostat/en/#data/FBS"],
        ["USDA ERS Food Availability", "https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/"],
    ],
    columns=["Source", "URL"],
)
st.dataframe(links_df, use_container_width=True, hide_index=True,
             column_config={"URL": st.column_config.LinkColumn("URL")})

st.markdown("---")
st.caption(
    "Dashboard created for DSC 205 Final Project · "
    "Layout follows the original project plan; all numbers come from real public-health agencies."
)
