import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os

# Page config
st.set_page_config(page_title="Colorectal Cancer Disparities Dashboard", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.0rem;
            padding-bottom: 2.2rem;
            max-width: 1450px;
        }
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }
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
# Data Loading
# ============================================================
# Use relative path for portability (data folder in same directory as script)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

@st.cache_data
def load_state_data():
    """Load and process state-level colorectal cancer data"""
    df = pd.read_csv(os.path.join(DATA_DIR, "colorectal_only_combined.csv"))
    return df

@st.cache_data
def load_state_data_improved():
    """Load improved state-level data with multiple cancer types"""
    df = pd.read_csv(os.path.join(DATA_DIR, "state_data_improved.csv"))
    # Filter for colorectal cancer
    crc_df = df[df['cancer_type'] == 'colon_rectum'].copy()
    return crc_df

@st.cache_data
def load_cancer_type_sex():
    """Load cancer type by sex data for trend analysis"""
    df = pd.read_csv(os.path.join(DATA_DIR, "cancer_type_sex.csv"))
    # Filter for rectum (colorectal related)
    rectum_df = df[df['cancer_type'] == 'rectum'].copy()
    return rectum_df

@st.cache_data
def load_global_data():
    """Load global colorectal cancer dataset with patient-level data"""
    df = pd.read_csv(os.path.join(DATA_DIR, "colorectal_cancer_dataset.csv"))
    df['age_group'] = pd.cut(df['Age'], bins=[0, 50, 60, 70, 80, 100],
                              labels=['<50', '50-60', '60-70', '70-80', '80+'])
    df['early_onset'] = df['Age'] < 50
    return df

@st.cache_data
def load_risk_factors():
    """Load risk factors dataset filtered for colon cancer"""
    df = pd.read_csv(os.path.join(DATA_DIR, "cancer-risk-factors.csv"))
    colon_df = df[df['Cancer_Type'] == 'Colon'].copy()
    return colon_df

@st.cache_data
def load_all_risk_factors():
    """Load full risk factors dataset for all cancer types"""
    df = pd.read_csv(os.path.join(DATA_DIR, "cancer-risk-factors.csv"))
    return df

# State to region mapping
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

# Load data
state_df = load_state_data()
state_improved_df = load_state_data_improved()
sex_trend_df = load_cancer_type_sex()
global_df = load_global_data()
risk_df = load_risk_factors()
all_risk_df = load_all_risk_factors()

# Process state data
state_df['region'] = state_df['state'].map(STATE_TO_REGION)
state_df['state_code'] = state_df['state'].map(STATE_ABBREV)

# Process state_improved data
state_improved_df['region'] = state_improved_df['state'].map(STATE_TO_REGION)
state_improved_df['state_code'] = state_improved_df['state'].map(STATE_ABBREV)

# ============================================================
# Sidebar filters
# ============================================================
st.sidebar.title("Dashboard Filters")

available_years = sorted(state_df['year'].unique())
year_range = st.sidebar.slider(
    "📅 Year Range",
    min_value=int(min(available_years)),
    max_value=int(max(available_years)),
    value=(int(min(available_years)), int(max(available_years)))
)

regions = ['All'] + sorted(state_df['region'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("🌎 Region Filter", regions)

metric_options = ['cases', 'deaths']
selected_metric = st.sidebar.selectbox("📊 Metric", metric_options)

# Filter data by year range
filtered_state_df = state_df[
    (state_df['year'] >= year_range[0]) &
    (state_df['year'] <= year_range[1])
]

if selected_region != 'All':
    filtered_state_df = filtered_state_df[filtered_state_df['region'] == selected_region]

# ============================================================
# Header
# ============================================================
st.title("Colorectal Cancer Disparities Dashboard")
st.caption("Interactive analysis of colorectal cancer trends, risk factors, and outcomes")

col1, col2 = st.columns([1.25, 1])
with col1:
    st.markdown("**Project title:** Colorectal Cancer Disparities Dashboard")
    st.markdown(
        "**Motivation:** Colorectal cancer is a strong topic for visualization because it combines time trends, "
        "geographic disparities, demographic differences, outcomes, and potential lifestyle risk factors. "
        "This dashboard explores patterns in burden and mortality across the United States."
    )
with col2:
    st.info(
        "This dashboard uses real data from multiple sources including state-level incidence/mortality data, "
        "global patient records, and risk factor datasets to answer key research questions about colorectal cancer disparities."
    )

with st.expander("Research Questions", expanded=True):
    questions = [
        "What combinations of lifestyle and demographic factors are most strongly associated with colorectal cancer risk?",
        "How do risk factor patterns differ between early-onset (<50) and traditional (50+) colorectal cancer patients?",
        "Are there distinct subgroups (clusters) of patients under 50 based on lifestyle, demographic, and health characteristics?",
        "To what extent can colorectal cancer risk in individuals under 50 be predicted using lifestyle and demographic data?",
        "How do geographic and socioeconomic factors influence colorectal cancer diagnosis rates?",
        "How does stage at diagnosis and outcomes vary across demographic groups (age, gender, socioeconomic indicators)?",
    ]
    for i, q in enumerate(questions, start=1):
        st.markdown(f"**{i}.** {q}")

# ============================================================
# KPI Cards
# ============================================================
st.subheader("Key Metrics")

# Calculate KPIs from filtered data
all_sex_data = filtered_state_df[filtered_state_df['sex'].isin(['All', 'Both'])]
total_cases = all_sex_data[all_sex_data['metric'] == 'cases']['value'].sum()
total_deaths = all_sex_data[all_sex_data['metric'] == 'deaths']['value'].sum()

# Find highest burden state in selected year range
state_totals = all_sex_data[all_sex_data['metric'] == selected_metric].groupby('state')['value'].sum()
if len(state_totals) > 0:
    highest_state = state_totals.idxmax()
    highest_value = state_totals.max()
else:
    highest_state = "N/A"
    highest_value = 0

# Calculate yearly change
yearly_totals = all_sex_data[all_sex_data['metric'] == selected_metric].groupby('year')['value'].sum()
if len(yearly_totals) > 1:
    avg_change = yearly_totals.diff().mean()
    pct_change = (yearly_totals.iloc[-1] - yearly_totals.iloc[0]) / yearly_totals.iloc[0] * 100 if yearly_totals.iloc[0] > 0 else 0
else:
    avg_change = 0
    pct_change = 0

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Total Cases</div>"
        f"<div style='margin-top:14px;font-size:1.5rem;font-weight:bold;color:#1d4ed8'>{total_cases:,.0f}</div></div>",
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Total Deaths</div>"
        f"<div style='margin-top:14px;font-size:1.5rem;font-weight:bold;color:#dc2626'>{total_deaths:,.0f}</div></div>",
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Highest Burden State</div>"
        f"<div style='margin-top:14px;font-size:1.2rem;font-weight:bold;color:#059669'>{highest_state}</div>"
        f"<div style='font-size:0.85rem;color:#6b7280'>{highest_value:,.0f} {selected_metric}</div></div>",
        unsafe_allow_html=True,
    )
with k4:
    change_color = "#dc2626" if pct_change > 0 else "#059669"
    st.markdown(
        f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>Period Change</div>"
        f"<div style='margin-top:14px;font-size:1.2rem;font-weight:bold;color:{change_color}'>{pct_change:+.1f}%</div>"
        f"<div style='font-size:0.85rem;color:#6b7280'>Avg yearly: {avg_change:+,.0f}</div></div>",
        unsafe_allow_html=True,
    )

# ============================================================
# Chart Row 1: Burden Over Time & Trend by Sex
# ============================================================
st.subheader("National Trends")

r1_left, r1_right = st.columns([1.35, 1])

with r1_left:
    st.markdown("**Colorectal Burden Over Time** <span class='tag'>line chart</span>", unsafe_allow_html=True)
    st.caption("National cases and deaths by year showing overall trend direction")

    # Aggregate national data by year and metric
    national_trend = all_sex_data.groupby(['year', 'metric'])['value'].sum().reset_index()

    fig = px.line(
        national_trend,
        x="year",
        y="value",
        color="metric",
        markers=True,
        template="simple_white",
        color_discrete_map={'cases': '#3b82f6', 'deaths': '#ef4444'}
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Year", showgrid=False)
    fig.update_yaxes(title_text="Count", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

with r1_right:
    st.markdown("**Trend by Sex Over Time** <span class='tag'>line chart</span>", unsafe_allow_html=True)
    st.caption("Rectal cancer cases by sex from cancer_type_sex.csv")

    # Use sex_trend_df (cancer_type_sex.csv) for sex-based trends
    fig = px.line(
        sex_trend_df,
        x="year",
        y="value",
        color="sex",
        markers=True,
        template="simple_white",
        color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899'}
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="Sex",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Year", showgrid=False)
    fig.update_yaxes(title_text="Cases", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Chart Row 2: Regional Comparison & State Ranking
# ============================================================
r2_left, r2_right = st.columns([1.15, 1.05])

with r2_left:
    st.markdown("**Regional Comparison** <span class='tag'>multi-line</span>", unsafe_allow_html=True)
    st.caption("Colorectal cancer burden across US census regions over time")

    # Aggregate by region and year
    region_data = all_sex_data[all_sex_data['metric'] == selected_metric].copy()
    region_data = region_data.dropna(subset=['region'])
    region_trend = region_data.groupby(['year', 'region'])['value'].sum().reset_index()

    fig = px.line(
        region_trend,
        x="year",
        y="value",
        color="region",
        markers=True,
        template="simple_white",
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="Region",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Year", showgrid=False)
    fig.update_yaxes(title_text=f"{selected_metric.title()}", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

with r2_right:
    st.markdown("**State Burden Ranking** <span class='tag'>bar chart</span>", unsafe_allow_html=True)
    st.caption("Top 10 states by colorectal cancer burden")

    # Get top 10 states
    state_ranking = all_sex_data[all_sex_data['metric'] == selected_metric].groupby('state')['value'].sum()
    top_states = state_ranking.nlargest(10).reset_index()
    top_states.columns = ['state', 'value']

    fig = px.bar(
        top_states.sort_values('value', ascending=True),
        x="value",
        y="state",
        orientation="h",
        template="simple_white",
        color="value",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        showlegend=False,
        coloraxis_showscale=False,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text=selected_metric.title(), gridcolor="#e5e7eb")
    fig.update_yaxes(title_text="")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Chart Row 3: Cases vs Deaths & Regional Distribution
# ============================================================
r3_left, r3_right = st.columns([1.2, 1])

with r3_left:
    st.markdown("**Cases vs Deaths by State** <span class='tag'>scatter plot</span>", unsafe_allow_html=True)
    st.caption("Relationship between diagnosis counts and death counts by state")

    # Create scatter data
    cases_by_state = all_sex_data[all_sex_data['metric'] == 'cases'].groupby(['state', 'region'])['value'].sum().reset_index()
    deaths_by_state = all_sex_data[all_sex_data['metric'] == 'deaths'].groupby('state')['value'].sum().reset_index()

    scatter_data = cases_by_state.merge(deaths_by_state, on='state', suffixes=('_cases', '_deaths'))
    scatter_data.columns = ['state', 'region', 'cases', 'deaths']
    scatter_data = scatter_data.dropna()

    fig = px.scatter(
        scatter_data,
        x="cases",
        y="deaths",
        color="region",
        hover_name="state",
        template="simple_white",
        size="cases",
        size_max=20,
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="Region",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Total Cases", gridcolor="#e5e7eb")
    fig.update_yaxes(title_text="Total Deaths", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

with r3_right:
    st.markdown("**Distribution by Region** <span class='tag'>box plot</span>", unsafe_allow_html=True)
    st.caption("Variability of state-level burden within each region")

    # Create box plot data
    box_data = all_sex_data[all_sex_data['metric'] == selected_metric].copy()
    box_data = box_data.dropna(subset=['region'])

    fig = px.box(
        box_data,
        x="region",
        y="value",
        template="simple_white",
        color="region",
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        showlegend=False,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Region")
    fig.update_yaxes(title_text=selected_metric.title(), gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Chart Row 4: Choropleth Map & Survival by Stage
# ============================================================
r4_left, r4_right = st.columns([1.2, 1])

with r4_left:
    st.markdown("**Geographic Burden by State** <span class='tag'>choropleth map</span>", unsafe_allow_html=True)
    st.caption("State-level colorectal cancer burden from state_data_improved.csv")

    # Use state_improved_df for choropleth (more complete state data)
    filtered_improved = state_improved_df[
        (state_improved_df['year'] >= year_range[0]) &
        (state_improved_df['year'] <= year_range[1]) &
        (state_improved_df['metric'] == selected_metric)
    ]

    if selected_region != 'All':
        filtered_improved = filtered_improved[filtered_improved['region'] == selected_region]

    map_data = filtered_improved.groupby(['state', 'state_code'])['value'].sum().reset_index()

    fig = px.choropleth(
        map_data,
        locations="state_code",
        locationmode="USA-states",
        color="value",
        scope="usa",
        hover_name="state",
        color_continuous_scale="Blues",
        template="simple_white",
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        coloraxis_colorbar_title=selected_metric.title(),
    )
    st.plotly_chart(fig, use_container_width=True)

with r4_right:
    st.markdown("**Survival by Stage at Diagnosis** <span class='tag'>bar chart</span>", unsafe_allow_html=True)
    st.caption("5-year survival rates vary significantly by cancer stage")

    # Calculate survival rates by stage from global data
    survival_by_stage = global_df.groupby('Cancer_Stage').agg({
        'Survival_5_years': lambda x: (x == 'Yes').mean() * 100
    }).reset_index()
    survival_by_stage.columns = ['stage', 'survival_rate']

    # Order stages logically
    stage_order = ['Localized', 'Regional', 'Metastatic']
    survival_by_stage['stage'] = pd.Categorical(survival_by_stage['stage'], categories=stage_order, ordered=True)
    survival_by_stage = survival_by_stage.sort_values('stage')

    fig = px.bar(
        survival_by_stage,
        x="stage",
        y="survival_rate",
        template="simple_white",
        color="survival_rate",
        color_continuous_scale=["#ef4444", "#f59e0b", "#22c55e"],
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        showlegend=False,
        coloraxis_showscale=False,
    )
    fig.update_xaxes(title_text="Stage at Diagnosis")
    fig.update_yaxes(title_text="5-Year Survival Rate (%)", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Additional Analysis: Cancer Type Comparison
# ============================================================
st.markdown("---")
st.subheader("Cancer Type Comparison (from state_data_improved.csv)")

# Load full state_data_improved for cancer type comparison
@st.cache_data
def load_full_state_improved():
    df = pd.read_csv(os.path.join(DATA_DIR, "state_data_improved.csv"))
    return df

full_state_improved = load_full_state_improved()

# Filter by year range
comparison_data = full_state_improved[
    (full_state_improved['year'] >= year_range[0]) &
    (full_state_improved['year'] <= year_range[1]) &
    (full_state_improved['metric'] == selected_metric)
]

comp_left, comp_right = st.columns(2)

with comp_left:
    st.markdown("**Cancer Types Comparison** <span class='tag'>bar chart</span>", unsafe_allow_html=True)
    st.caption("How colorectal cancer compares to other cancer types nationally")

    # Aggregate by cancer type
    cancer_totals = comparison_data.groupby('cancer_type')['value'].sum().sort_values(ascending=True).tail(10)
    cancer_totals_df = cancer_totals.reset_index()
    cancer_totals_df.columns = ['cancer_type', 'value']

    # Highlight colorectal
    cancer_totals_df['highlight'] = cancer_totals_df['cancer_type'].apply(
        lambda x: 'Colorectal' if x == 'colon_rectum' else 'Other'
    )

    fig = px.bar(
        cancer_totals_df,
        x='value',
        y='cancer_type',
        orientation='h',
        color='highlight',
        template="simple_white",
        color_discrete_map={'Colorectal': '#ef4444', 'Other': '#94a3b8'}
    )
    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=28, b=10),
        showlegend=False,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text=f"Total {selected_metric.title()}", gridcolor="#e5e7eb")
    fig.update_yaxes(title_text="")
    st.plotly_chart(fig, use_container_width=True)

with comp_right:
    st.markdown("**Colorectal vs Other Cancers Over Time** <span class='tag'>area chart</span>", unsafe_allow_html=True)
    st.caption("Trend comparison between colorectal and other major cancers")

    # Select top cancers for comparison
    top_cancers = ['colon_rectum', 'lung_bronchus', 'female_breast', 'prostate']
    trend_comparison = comparison_data[comparison_data['cancer_type'].isin(top_cancers)]
    trend_by_year = trend_comparison.groupby(['year', 'cancer_type'])['value'].sum().reset_index()

    fig = px.line(
        trend_by_year,
        x='year',
        y='value',
        color='cancer_type',
        markers=True,
        template="simple_white",
    )
    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="Cancer Type",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Year", showgrid=False)
    fig.update_yaxes(title_text=selected_metric.title(), gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Research Question Analysis Section
# ============================================================
st.markdown("---")
st.subheader("Research Question Analysis")

# Q1 & Q2: Risk Factors Analysis
st.markdown("### Q1 & Q2: Risk Factor Analysis")
q1_left, q1_right = st.columns(2)

with q1_left:
    st.markdown("**Risk Factors Correlation** <span class='tag'>heatmap</span>", unsafe_allow_html=True)
    st.caption("Correlation between lifestyle factors and cancer risk")

    # Select numeric risk factor columns
    risk_cols = ['Smoking', 'Alcohol_Use', 'Obesity', 'Diet_Red_Meat',
                 'Diet_Salted_Processed', 'Fruit_Veg_Intake', 'Physical_Activity', 'BMI']
    risk_numeric = risk_df[risk_cols].copy()
    correlation = risk_numeric.corr()

    fig = px.imshow(
        correlation,
        text_auto='.2f',
        color_continuous_scale='RdBu_r',
        template="simple_white",
    )
    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=28, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

with q1_right:
    st.markdown("**Early-Onset vs Traditional Patients** <span class='tag'>comparison</span>", unsafe_allow_html=True)
    st.caption("Risk factor differences between patients <50 and 50+ years old")

    # Compare early onset vs traditional
    early_onset = global_df[global_df['early_onset'] == True]
    traditional = global_df[global_df['early_onset'] == False]

    comparison_data = pd.DataFrame({
        'Factor': ['Family History', 'Smoking History', 'Obesity', 'Diabetes', 'IBD'],
        'Early Onset (<50)': [
            (early_onset['Family_History'] == 'Yes').mean() * 100,
            (early_onset['Smoking_History'] == 'Yes').mean() * 100,
            (early_onset['Obesity_BMI'].isin(['Overweight', 'Obese'])).mean() * 100,
            (early_onset['Diabetes'] == 'Yes').mean() * 100,
            (early_onset['Inflammatory_Bowel_Disease'] == 'Yes').mean() * 100,
        ],
        'Traditional (50+)': [
            (traditional['Family_History'] == 'Yes').mean() * 100,
            (traditional['Smoking_History'] == 'Yes').mean() * 100,
            (traditional['Obesity_BMI'].isin(['Overweight', 'Obese'])).mean() * 100,
            (traditional['Diabetes'] == 'Yes').mean() * 100,
            (traditional['Inflammatory_Bowel_Disease'] == 'Yes').mean() * 100,
        ],
    })

    comparison_melted = comparison_data.melt(id_vars='Factor', var_name='Group', value_name='Percentage')

    fig = px.bar(
        comparison_melted,
        x='Factor',
        y='Percentage',
        color='Group',
        barmode='group',
        template="simple_white",
        color_discrete_map={'Early Onset (<50)': '#f59e0b', 'Traditional (50+)': '#3b82f6'}
    )
    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="",
    )
    fig.update_yaxes(title_text="Prevalence (%)", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

# Q3: Patient Subgroups Analysis
st.markdown("### Q3: Patient Subgroups (Early-Onset Analysis)")

q3_left, q3_right = st.columns([1.2, 1])

with q3_left:
    st.markdown("**Early-Onset Patient Characteristics** <span class='tag'>scatter</span>", unsafe_allow_html=True)
    st.caption("Patients under 50 by age, tumor size, and cancer stage")

    # Prepare data for early onset patients
    early_onset_data = global_df[global_df['early_onset'] == True][
        ['Age', 'Tumor_Size_mm', 'Cancer_Stage', 'Healthcare_Costs']
    ].dropna()

    if len(early_onset_data) > 10:
        fig = px.scatter(
            early_onset_data,
            x='Age',
            y='Tumor_Size_mm',
            color='Cancer_Stage',
            size='Healthcare_Costs',
            template="simple_white",
            color_discrete_map={'Localized': '#22c55e', 'Regional': '#f59e0b', 'Metastatic': '#ef4444'}
        )
        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=28, b=10),
            legend_title_text="Stage",
        )
        fig.update_xaxes(title_text="Age", gridcolor="#e5e7eb")
        fig.update_yaxes(title_text="Tumor Size (mm)", gridcolor="#e5e7eb")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Insufficient data for analysis")

with q3_right:
    st.markdown("**Early-Onset Subgroup Statistics** <span class='tag'>summary</span>", unsafe_allow_html=True)

    if len(early_onset_data) > 10:
        # Group by cancer stage for summary
        subgroup_summary = early_onset_data.groupby('Cancer_Stage').agg({
            'Age': 'mean',
            'Tumor_Size_mm': 'mean',
            'Healthcare_Costs': 'mean'
        }).round(1)
        subgroup_summary['Count'] = early_onset_data.groupby('Cancer_Stage').size()
        subgroup_summary = subgroup_summary.rename(columns={
            'Age': 'Avg Age',
            'Tumor_Size_mm': 'Avg Tumor (mm)',
            'Healthcare_Costs': 'Avg Cost ($)'
        })

        st.dataframe(subgroup_summary, use_container_width=True)

        st.markdown("""
        **Key Findings:**
        - Early-onset patients (<50) show varied tumor sizes across stages
        - Metastatic cases tend to have higher healthcare costs
        - Localized detection correlates with smaller tumor sizes
        """)

# Q5 & Q6: Geographic and Demographic Analysis
st.markdown("### Q5 & Q6: Geographic and Demographic Disparities")

q5_left, q5_right = st.columns(2)

with q5_left:
    st.markdown("**Socioeconomic Factors** <span class='tag'>comparison</span>", unsafe_allow_html=True)
    st.caption("How economic classification affects outcomes")

    # Economic classification comparison
    econ_data = global_df.groupby(['Economic_Classification', 'Cancer_Stage']).agg({
        'Survival_5_years': lambda x: (x == 'Yes').mean() * 100
    }).reset_index()
    econ_data.columns = ['Economic_Classification', 'Cancer_Stage', 'Survival_Rate']

    fig = px.bar(
        econ_data,
        x='Cancer_Stage',
        y='Survival_Rate',
        color='Economic_Classification',
        barmode='group',
        template="simple_white",
    )
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="",
    )
    fig.update_yaxes(title_text="5-Year Survival (%)", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

with q5_right:
    st.markdown("**Urban vs Rural Outcomes** <span class='tag'>comparison</span>", unsafe_allow_html=True)
    st.caption("Geographic setting impact on cancer outcomes")

    # Urban vs Rural comparison
    urban_rural = global_df.groupby(['Urban_or_Rural', 'Cancer_Stage']).agg({
        'Survival_5_years': lambda x: (x == 'Yes').mean() * 100,
        'Early_Detection': lambda x: (x == 'Yes').mean() * 100,
    }).reset_index()
    urban_rural.columns = ['Setting', 'Cancer_Stage', 'Survival_Rate', 'Early_Detection_Rate']

    fig = px.scatter(
        urban_rural,
        x='Early_Detection_Rate',
        y='Survival_Rate',
        color='Setting',
        symbol='Cancer_Stage',
        size=[50]*len(urban_rural),
        template="simple_white",
    )
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="",
    )
    fig.update_xaxes(title_text="Early Detection Rate (%)", gridcolor="#e5e7eb")
    fig.update_yaxes(title_text="5-Year Survival (%)", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

# Stage and Outcomes by Demographics
st.markdown("**Stage at Diagnosis by Age Group** <span class='tag'>stacked bar</span>", unsafe_allow_html=True)

stage_by_age = global_df.groupby(['age_group', 'Cancer_Stage']).size().reset_index(name='count')
stage_by_age_pct = stage_by_age.copy()
totals = stage_by_age_pct.groupby('age_group')['count'].transform('sum')
stage_by_age_pct['percentage'] = stage_by_age_pct['count'] / totals * 100

fig = px.bar(
    stage_by_age_pct,
    x='age_group',
    y='percentage',
    color='Cancer_Stage',
    template="simple_white",
    color_discrete_map={'Localized': '#22c55e', 'Regional': '#f59e0b', 'Metastatic': '#ef4444'}
)
fig.update_layout(
    height=300,
    margin=dict(l=10, r=10, t=28, b=10),
    legend_title_text="Stage",
    barmode='stack',
)
fig.update_xaxes(title_text="Age Group")
fig.update_yaxes(title_text="Percentage (%)", gridcolor="#e5e7eb")
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Dataset Information
# ============================================================
st.markdown("---")
st.subheader("Dataset Information")

source_df = pd.DataFrame(
    [
        ["colorectal_only_combined.csv", "ACS Data", f"{len(state_df):,}", "7", "State-level colorectal incidence and mortality with sex breakdown"],
        ["state_data_improved.csv", "ACS Data", f"{len(state_improved_df):,}", "5", "Enhanced state-level data used for choropleth map"],
        ["cancer_type_sex.csv", "ACS Data", f"{len(sex_trend_df):,}", "4", "Cancer trends by sex over time"],
        ["colorectal_cancer_dataset.csv", "Global Dataset", f"{len(global_df):,}", "28", "Patient-level outcomes, survival, and demographics"],
        ["cancer-risk-factors.csv", "Risk Factor Dataset", f"{len(all_risk_df):,}", "21", "Lifestyle and risk factor analysis (418 Colon patients)"],
    ],
    columns=["Dataset", "Source", "Rows", "Columns", "Purpose"],
)
st.dataframe(source_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Dashboard created for DSC 205 Final Project | Data visualization of colorectal cancer disparities")
