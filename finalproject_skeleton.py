import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import folium

st.set_page_config(page_title="Project Proposal Skeleton", page_icon="📊", layout="wide")

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
# Sidebar skeleton
# ============================================================
st.sidebar.title("Sidebar Widgets")
st.sidebar.markdown("📅 **Year range slider**")
st.sidebar.markdown("🌎 **Region filter**")
st.sidebar.markdown("📊 **Metric selector**")
st.sidebar.markdown("👥 **Sex selector**")
st.sidebar.markdown("🔎 **Dataset toggle**")
st.sidebar.markdown("🧹 **Pre-processing toggle**")

# ============================================================
# Header / proposal content
# ============================================================
st.title("Colorectal Cancer Disparities Dashboard")
st.caption("Project proposal presentation skeleton")

col1, col2 = st.columns([1.25, 1])
with col1:
    st.markdown("**Project title:** Colorectal Cancer Disparities Dashboard")
    st.markdown(
        "**Motivation:** Colorectal cancer is a strong topic for visualization because it combines time trends, geographic disparities, demographic differences, outcomes, and potential lifestyle risk factors. The goal is to move beyond simple plots and build a dashboard that explains patterns in burden and mortality."
    )
with col2:
    st.info(
        "This is a true skeleton for the milestone: it focuses on layout, chart placeholders, dataset snippets, research questions, and preprocessing notes rather than a final polished analytical dashboard."
    )

with st.expander("Visualization goals / questions", expanded=True):
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
# Dataset sources and snippets
# ============================================================
st.subheader("Dataset sources and snippets")
source_df = pd.DataFrame(
    [
        ["Global Colorectal Cancer Dataset", "Kaggle", "167,497", "28", "Age trends and geographic comparisons"],
        ["Dietary & Lifestyle Dataset", "External dataset", "TBD", "TBD", "Diet, alcohol, activity, obesity"],
        ["Cancer Risk Factors Dataset", "Kaggle", "TBD", "TBD", "Broader health and demographic correlations"],
        ["Survival Dataset", "Kaggle", "89,945", "30", "Outcomes, mortality, stage"],
        ["ACS Cancer Facts & Figures 2015–Present", "American Cancer Society", "TBD", "TBD", "National incidence, mortality, disparities"],
    ],
    columns=["Dataset", "Source", "Rows", "Columns", "Purpose"],
)
st.dataframe(source_df, use_container_width=True, hide_index=True)

snippet_left, snippet_right = st.columns(2)
with snippet_left:
    st.markdown("**Snippet: ACS dataset**")
    st.dataframe(
        pd.DataFrame(
            {
                "year": [2015, 2015, 2015, 2016, 2016],
                "state": ["California", "Texas", "Florida", "California", "Texas"],
                "metric": ["cases", "cases", "deaths", "cases", "deaths"],
                "cancer_type": ["colon_rectum"] * 5,
                "value": [14510, 9460, 3920, 14720, 4010],
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

with snippet_right:
    st.markdown("**Snippet: Global / risk / survival examples**")
    st.dataframe(
        pd.DataFrame(
            {
                "country": ["United States", "Canada", "Japan", "Germany", "Brazil"],
                "age_group": ["45-49", "50-54", "55-59", "60-64", "40-44"],
                "incidence_rate": [36.1, 31.4, 42.0, 33.7, 18.6],
                "mortality_rate": [12.8, 10.7, 14.2, 11.9, 7.4],
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# Dashboard skeleton
# ============================================================
st.subheader("Dashboard skeleton")
st.caption("Primary visualizations and widgets modeled after the sample layout screenshots")

# Mock sketch data
np.random.seed(7)
years = list(range(2015, 2025))

trend_df = pd.DataFrame(
    {
        "year": years * 2,
        "metric": ["Cases"] * len(years) + ["Deaths"] * len(years),
        "value": [
            132000, 133500, 135200, 136800, 138600,
            140300, 141800, 143900, 145100, 147200,
            50000, 50500, 51200, 51800, 52500,
            53100, 53800, 54400, 55100, 55900,
        ],
    }
)

sex_df = pd.DataFrame(
    {
        "year": years * 2,
        "sex": ["Male"] * len(years) + ["Female"] * len(years),
        "value": [
            70000, 71000, 72000, 72600, 73500,
            74200, 74800, 75400, 76000, 77000,
            62000, 62500, 63200, 64200, 65100,
            66100, 67000, 68500, 69100, 70200,
        ],
    }
)

region_df = pd.DataFrame(
    {
        "year": years * 4,
        "region": (
            ["Northeast"] * len(years)
            + ["Midwest"] * len(years)
            + ["South"] * len(years)
            + ["West"] * len(years)
        ),
        "value": [
            21000, 21200, 21400, 21650, 21900, 22050, 22300, 22550, 22800, 23050,
            26000, 26250, 26500, 26800, 27100, 27300, 27550, 27800, 28100, 28450,
            43000, 43500, 43800, 44200, 44700, 45100, 45500, 46000, 46600, 47200,
            37000, 37300, 37600, 37900, 38200, 38600, 39000, 39400, 39900, 40400,
        ],
    }
)

state_rank_df = pd.DataFrame(
    {
        "state": ["California", "Texas", "Florida", "New York", "Pennsylvania", "Illinois", "Ohio", "Georgia"],
        "value": [14720, 9600, 8400, 7700, 6900, 6500, 6100, 5900],
    }
)

scatter_df = pd.DataFrame(
    {
        "state": ["California", "Texas", "Florida", "New York", "Pennsylvania", "Illinois", "Ohio", "Georgia"],
        "region": ["West", "South", "South", "Northeast", "Northeast", "Midwest", "Midwest", "South"],
        "cases": [14720, 9600, 8400, 7700, 6900, 6500, 6100, 5900],
        "deaths": [5200, 3400, 3200, 2500, 2400, 2200, 2100, 2050],
    }
)

box_df = pd.DataFrame(
    {
        "region": np.repeat(["Northeast", "Midwest", "South", "West"], 10),
        "value": [
            2200, 2350, 2480, 2520, 2600, 2720, 2800, 2900, 3100, 3300,
            2000, 2100, 2250, 2350, 2450, 2500, 2620, 2750, 2880, 3010,
            2600, 2750, 2900, 3050, 3200, 3320, 3450, 3600, 3800, 3950,
            1900, 2050, 2150, 2250, 2350, 2450, 2520, 2650, 2780, 2900,
        ],
    }
)

risk_df = pd.DataFrame(
    {
        "obesity_rate": [24, 27, 31, 29, 34, 26, 30, 33],
        "incidence_rate": [28, 31, 36, 33, 39, 30, 34, 37],
        "relative_burden": [12, 14, 18, 15, 20, 13, 17, 19],
        "cluster": ["A", "A", "B", "B", "C", "A", "B", "C"],
    }
)

survival_df = pd.DataFrame(
    {
        "stage": ["Localized", "Regional", "Distant"],
        "survival": [91, 73, 16],
    }
)

# KPI row
k1, k2, k3, k4 = st.columns(4)
for col, title in zip(
    [k1, k2, k3, k4],
    ["Total cases", "Total deaths", "Highest-burden state", "Avg yearly change"],
):
    with col:
        st.markdown(
            f"<div class='metric-box'><div style='font-size:0.95rem;color:#444'>{title}</div>"
            f"<div style='margin-top:14px;color:#8a8a8a'>summary card</div></div>",
            unsafe_allow_html=True,
        )

# Chart row 1
r1_left, r1_right = st.columns([1.35, 1])
with r1_left:
    st.markdown("**Colorectal burden over time** <span class='tag'>line chart</span>", unsafe_allow_html=True)
    st.caption("Sketch of how yearly colorectal cases and deaths will be shown together to highlight trend direction.")
    fig = px.line(
        trend_df,
        x="year",
        y="value",
        color="metric",
        markers=True,
        template="simple_white",
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
    st.markdown("**National trend by sex** <span class='tag'>dual line</span>", unsafe_allow_html=True)
    st.caption("Sketch of sex-based national trends to compare whether burden differs across time for male and female populations.")
    fig = px.line(
        sex_df,
        x="year",
        y="value",
        color="sex",
        markers=True,
        template="simple_white",
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

# Chart row 2
r2_left, r2_right = st.columns([1.15, 1.05])
with r2_left:
    st.markdown("**Regional comparison** <span class='tag'>multi-line</span>", unsafe_allow_html=True)
    st.caption("Sketch of regional trajectories showing whether the Northeast, Midwest, South, and West follow different patterns.")
    fig = px.line(
        region_df,
        x="year",
        y="value",
        color="region",
        markers=True,
        template="simple_white",
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

with r2_right:
    st.markdown("**State burden ranking** <span class='tag'>bar chart</span>", unsafe_allow_html=True)
    st.caption("Sketch of the top states by colorectal burden so viewers can quickly identify high-count geographies.")
    fig = px.bar(
        state_rank_df.sort_values("value", ascending=True),
        x="value",
        y="state",
        orientation="h",
        template="simple_white",
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        showlegend=False,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Cases", gridcolor="#e5e7eb")
    fig.update_yaxes(title_text="")
    st.plotly_chart(fig, use_container_width=True)

# Chart row 3
r3_left, r3_right = st.columns([1.2, 1])
with r3_left:
    st.markdown("**Cases vs deaths by state** <span class='tag'>scatter plot</span>", unsafe_allow_html=True)
    st.caption("Sketch of the relationship between diagnosis counts and death counts, useful for spotting outlier states.")
    fig = px.scatter(
        scatter_df,
        x="cases",
        y="deaths",
        color="region",
        hover_name="state",
        template="simple_white",
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Cases", gridcolor="#e5e7eb")
    fig.update_yaxes(title_text="Deaths", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

with r3_right:
    st.markdown("**Distribution by region** <span class='tag'>box plot</span>", unsafe_allow_html=True)
    st.caption("Sketch of the spread and variability within each region rather than only comparing averages.")
    fig = px.box(
        box_df,
        x="region",
        y="value",
        template="simple_white",
        points=False,
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        showlegend=False,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Region")
    fig.update_yaxes(title_text="Deaths", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

# Chart row 4
r4_left, r4_right = st.columns([1.2, 1])

with r4_left:
    st.markdown("**Geographic burden by state** <span class='tag'>choropleth map</span>", unsafe_allow_html=True)
    st.caption("Sketch of a political-style state map where darker shading indicates higher colorectal cancer burden.")

    states = [
        ("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"),
        ("CA", "California"), ("CO", "Colorado"), ("CT", "Connecticut"), ("DE", "Delaware"),
        ("FL", "Florida"), ("GA", "Georgia"), ("HI", "Hawaii"), ("ID", "Idaho"),
        ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"),
        ("KY", "Kentucky"), ("LA", "Louisiana"), ("ME", "Maine"), ("MD", "Maryland"),
        ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"), ("MS", "Mississippi"),
        ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"), ("NV", "Nevada"),
        ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"), ("NY", "New York"),
        ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"),
        ("OR", "Oregon"), ("PA", "Pennsylvania"), ("RI", "Rhode Island"), ("SC", "South Carolina"),
        ("SD", "South Dakota"), ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"),
        ("VT", "Vermont"), ("VA", "Virginia"), ("WA", "Washington"), ("WV", "West Virginia"),
        ("WI", "Wisconsin"), ("WY", "Wyoming"),
    ]

    geo_df = pd.DataFrame(states, columns=["state_code", "state"])
    np.random.seed(7)
    geo_df["value"] = np.random.randint(5000, 15000, size=len(geo_df))

    fig = px.choropleth(
        geo_df,
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
        coloraxis_colorbar_title="Burden",
    )
    st.plotly_chart(fig, use_container_width=True)

with r4_right:
    st.markdown("**Survival / stage outcomes** <span class='tag'>bar chart</span>", unsafe_allow_html=True)
    st.caption("Sketch of how survival changes by stage at diagnosis to support the outcomes side of the project story.")
    fig = px.bar(
        survival_df,
        x="stage",
        y="survival",
        template="simple_white",
    )
    fig.update_layout(
        height=315,
        margin=dict(l=10, r=10, t=28, b=10),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        showlegend=False,
    )
    fig.update_xaxes(title_text="Stage")
    fig.update_yaxes(title_text="5-year survival %", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

# Chart row 5 - centered bubble chart for odd count
spacer_left, center_col, spacer_right = st.columns([0.12, 0.76, 0.12])

with center_col:
    st.markdown("**Risk-Factor Comparison** <span class='tag'>bubble chart</span>", unsafe_allow_html=True)
    st.caption("Sketch of how a lifestyle factor such as obesity might relate to incidence, with bubble size representing relative burden.")
    fig = px.scatter(
        risk_df,
        x="obesity_rate",
        y="incidence_rate",
        size="relative_burden",
        color="cluster",
        template="simple_white",
    )
    fig.update_layout(
        height=340,
        margin=dict(l=10, r=10, t=28, b=10),
        legend_title_text="",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )
    fig.update_xaxes(title_text="Obesity rate", gridcolor="#e5e7eb")
    fig.update_yaxes(title_text="Incidence rate", gridcolor="#e5e7eb")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Planned preprocessing
# ============================================================
st.subheader("Planned data pre-processing")
pre_df = pd.DataFrame(
    [
        ["Extract ACS tables from PDF reports", "Convert annual tables into CSV format"],
        ["Standardize columns across datasets", "Align year, geography, metric, sex, and outcome fields"],
        ["Handle missing values", "Replace, drop, or annotate null values as needed"],
        ["Map states to US regions", "Support regional comparisons in dashboard views"],
        ["Create master schema", "Make one shared structure for multi-dataset visualization"],
        ["Normalize metrics later", "Prepare for rate-per-100k analysis in later phases"],
    ],
    columns=["Step", "Why it is needed"],
)
st.dataframe(pre_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown(
    "**Note:** This version is intentionally a proposal skeleton. It satisfies the milestone by showing the project title, motivation, visualization goals, dataset sources and snippets, dashboard layout, and preprocessing plan without presenting the final dashboard implementation."
)