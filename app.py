from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Hospital Readmission Performance",
    page_icon="🏥",
    layout="wide",
)


DATA_FILE = Path(__file__).parent / "data" / "FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv"

MEASURE_LABELS = {
    "READM-30-HIP-KNEE-HRRP": "Hip/Knee Replacement",
    "READM-30-CABG-HRRP": "CABG",
    "READM-30-AMI-HRRP": "Heart Attack (AMI)",
    "READM-30-COPD-HRRP": "COPD",
    "READM-30-PN-HRRP": "Pneumonia",
    "READM-30-HF-HRRP": "Heart Failure",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)
    df["Condition"] = df["Measure Name"].map(MEASURE_LABELS).fillna(df["Measure Name"])
    df["Excess Readmission Ratio"] = pd.to_numeric(
        df["Excess Readmission Ratio"], errors="coerce"
    )
    df["Predicted Readmission Rate"] = pd.to_numeric(
        df["Predicted Readmission Rate"], errors="coerce"
    )
    df["Expected Readmission Rate"] = pd.to_numeric(
        df["Expected Readmission Rate"], errors="coerce"
    )
    return df


df = load_data()
valid_df = df.dropna(subset=["Excess Readmission Ratio"]).copy()

st.title("Hospital Readmission Performance")
st.caption(
    "CMS Hospital Readmissions Reduction Program | Reporting period: July 2021–June 2024"
)

st.subheader("Where is excess readmission performance highest?")
st.write(
    "Use the controls to rank hospitals or states by their average Excess Readmission Ratio. "
    "A ratio above 1.00 means readmissions were higher than expected."
)

with st.sidebar:
    st.header("Ranking controls")
    ranking_level = st.radio("Rank by", ["Hospitals", "States"], horizontal=True)
    selected_conditions = st.multiselect(
        "Medical conditions",
        options=sorted(valid_df["Condition"].unique()),
        default=sorted(valid_df["Condition"].unique()),
    )
    selected_states = st.multiselect(
        "States",
        options=sorted(valid_df["State"].unique()),
        default=[],
        placeholder="All states",
    )
    top_n = st.slider("Number of places to display", min_value=5, max_value=25, value=10)

filtered = valid_df[valid_df["Condition"].isin(selected_conditions)].copy()
if selected_states:
    filtered = filtered[filtered["State"].isin(selected_states)]

if filtered.empty:
    st.warning("No records match the selected filters. Choose at least one condition and state.")
    st.stop()

if ranking_level == "Hospitals":
    ranking = (
        filtered.groupby(["Facility ID", "Facility Name", "State"], as_index=False)
        .agg(
            excess_readmission_ratio=("Excess Readmission Ratio", "mean"),
            conditions_reported=("Condition", "nunique"),
        )
        .sort_values("excess_readmission_ratio", ascending=False)
        .head(top_n)
    )
    ranking["Place"] = ranking["Facility Name"] + " (" + ranking["State"] + ")"
    y_column = "Place"
    detail_label = "hospital"
else:
    ranking = (
        filtered.groupby("State", as_index=False)
        .agg(
            excess_readmission_ratio=("Excess Readmission Ratio", "mean"),
            hospitals_reported=("Facility ID", "nunique"),
        )
        .sort_values("excess_readmission_ratio", ascending=False)
        .head(top_n)
    )
    ranking["Place"] = ranking["State"]
    y_column = "Place"
    detail_label = "state"

ranking = ranking.sort_values("excess_readmission_ratio", ascending=True)

fig = px.bar(
    ranking,
    x="excess_readmission_ratio",
    y=y_column,
    orientation="h",
    text="excess_readmission_ratio",
    color="excess_readmission_ratio",
    color_continuous_scale=["#2a9d8f", "#f4a261", "#e76f51"],
    labels={
        "excess_readmission_ratio": "Average Excess Readmission Ratio",
        "Place": ranking_level[:-1] if ranking_level.endswith("s") else ranking_level,
    },
    hover_data={
        "excess_readmission_ratio": ":.3f",
        "Place": False,
    },
)
fig.add_vline(
    x=1.0,
    line_dash="dash",
    line_color="#333333",
    annotation_text="Expected performance (1.00)",
    annotation_position="top",
)
fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
fig.update_layout(
    height=max(450, 34 * len(ranking) + 130),
    coloraxis_showscale=False,
    margin=dict(l=20, r=80, t=55, b=40),
    xaxis=dict(range=[min(0.85, ranking["excess_readmission_ratio"].min() - 0.02), None]),
)

st.plotly_chart(fig, use_container_width=True)

avg_ratio = filtered["Excess Readmission Ratio"].mean()
col1, col2, col3 = st.columns(3)
col1.metric("Records included", f"{len(filtered):,}")
col2.metric(f"{detail_label.title()}s shown", f"{len(ranking):,}")
col3.metric("Overall average ratio", f"{avg_ratio:.3f}")

with st.expander("How to interpret this chart"):
    st.write(
        "Higher values indicate more readmissions than expected relative to the CMS comparison "
        "standard. The chart uses only records with a reported Excess Readmission Ratio. "
        "Records suppressed by CMS because of small counts are excluded from the ranking."
    )

st.divider()
st.subheader("How does readmission performance differ by condition?")
st.write(
    "Compare the average Excess Readmission Ratio across the selected CMS conditions. "
    "This can help identify which conditions may require the greatest improvement focus."
)

condition_summary = (
    filtered.groupby("Condition", as_index=False)
    .agg(
        average_excess_readmission_ratio=("Excess Readmission Ratio", "mean"),
        hospitals_reported=("Facility ID", "nunique"),
    )
    .sort_values("average_excess_readmission_ratio", ascending=True)
)

condition_fig = px.bar(
    condition_summary,
    x="average_excess_readmission_ratio",
    y="Condition",
    orientation="h",
    text="average_excess_readmission_ratio",
    color="average_excess_readmission_ratio",
    color_continuous_scale=["#2a9d8f", "#f4a261", "#e76f51"],
    labels={
        "average_excess_readmission_ratio": "Average Excess Readmission Ratio",
        "Condition": "Medical Condition",
    },
    hover_data={
        "average_excess_readmission_ratio": ":.3f",
        "hospitals_reported": ":,",
    },
)
condition_fig.add_vline(
    x=1.0,
    line_dash="dash",
    line_color="#333333",
    annotation_text="Expected performance (1.00)",
    annotation_position="top",
)
condition_fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
condition_fig.update_layout(
    height=max(400, 60 * len(condition_summary) + 140),
    coloraxis_showscale=False,
    margin=dict(l=20, r=80, t=55, b=40),
    xaxis=dict(range=[min(0.85, condition_summary["average_excess_readmission_ratio"].min() - 0.02), None]),
)

st.plotly_chart(condition_fig, use_container_width=True)

condition_table = condition_summary.rename(
    columns={
        "Condition": "Medical Condition",
        "average_excess_readmission_ratio": "Average Excess Readmission Ratio",
        "hospitals_reported": "Hospitals Reported",
    }
).copy()
condition_table["Average Excess Readmission Ratio"] = condition_table[
    "Average Excess Readmission Ratio"
].round(3)
st.dataframe(condition_table, use_container_width=True, hide_index=True)

with st.expander("How to interpret this chart"):
    st.write(
        "Each bar shows the average Excess Readmission Ratio for a medical condition. "
        "The ratio compares a hospital's predicted readmissions with the number of "
        "readmissions expected for similar patients. A ratio above 1.00 means more "
        "readmissions than expected, while a ratio below 1.00 means fewer than expected. "
        "Conditions with higher bars may deserve greater quality-improvement attention. "
        "The comparison uses only records with reported ratios, so CMS-suppressed records "
        "are not included in the averages."
    )

st.divider()
st.subheader("How does predicted readmission compare with expected readmission?")
st.write(
    "Each point represents a hospital and medical condition. Points above the diagonal line "
    "have predicted readmission rates higher than expected and may require greater attention."
)

scatter_data = filtered.dropna(
    subset=["Predicted Readmission Rate", "Expected Readmission Rate"]
).copy()

if scatter_data.empty:
    st.warning("No records with both predicted and expected readmission rates match the selected filters.")
else:
    scatter_data["Performance"] = scatter_data["Excess Readmission Ratio"].apply(
        lambda ratio: "Above Expected" if ratio > 1 else "At or Below Expected"
    )

    scatter_fig = px.scatter(
        scatter_data,
        x="Expected Readmission Rate",
        y="Predicted Readmission Rate",
        color="Performance",
        color_discrete_map={
            "At or Below Expected": "#2a9d8f",
            "Above Expected": "#e76f51",
        },
        hover_name="Facility Name",
        hover_data={
            "State": True,
            "Condition": True,
            "Excess Readmission Ratio": ":.3f",
            "Expected Readmission Rate": ":.2f",
            "Predicted Readmission Rate": ":.2f",
        },
        labels={
            "Expected Readmission Rate": "Expected Readmission Rate (%)",
            "Predicted Readmission Rate": "Predicted Readmission Rate (%)",
            "Performance": "Performance",
        },
    )

    line_min = min(
        scatter_data["Expected Readmission Rate"].min(),
        scatter_data["Predicted Readmission Rate"].min(),
    )
    line_max = max(
        scatter_data["Expected Readmission Rate"].max(),
        scatter_data["Predicted Readmission Rate"].max(),
    )
    scatter_fig.add_shape(
        type="line",
        x0=line_min,
        y0=line_min,
        x1=line_max,
        y1=line_max,
        line=dict(color="#333333", dash="dash", width=2),
    )
    scatter_fig.add_annotation(
        x=line_max,
        y=line_max,
        text="Predicted = Expected",
        showarrow=False,
        xanchor="right",
        yanchor="bottom",
    )
    scatter_fig.update_traces(marker=dict(size=8, opacity=0.7))
    scatter_fig.update_layout(
        height=600,
        legend_title_text="Performance",
        margin=dict(l=20, r=30, t=55, b=40),
    )
    st.plotly_chart(scatter_fig, use_container_width=True)
    st.caption(
        "Points above the dashed diagonal line have predicted readmission rates higher than "
        "expected. The dataset does not include a payment-reduction percentage, so this chart "
        "shows a quality-performance comparison rather than direct financial risk."
    )

    with st.expander("How to interpret this chart"):
        st.write(
            "Each point represents a hospital and medical condition. The predicted "
            "readmission rate is CMS's estimate for that hospital based on the patients it "
            "treated. The expected readmission rate is a benchmark for similar patients at "
            "an average hospital. Points above the dashed diagonal line have predicted "
            "readmission rates higher than expected, which may signal a need for additional "
            "follow-up or quality-improvement attention. Points below the line have predicted "
            "rates lower than expected."
        )
