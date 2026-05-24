import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Sri Lanka Tourism Analytics Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0F172A;
}

h1, h2, h3, h4 {
    color: white;
}

[data-testid="metric-container"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 15px;
}

[data-testid="metric-container"] label {
    color: white;
}

.stDataFrame {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🌍 Sri Lanka Tourism Analytics Dashboard")
st.markdown("### Interactive Business Intelligence Dashboard using Python & Streamlit")

st.markdown("---")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_excel("data/tourism.xlsx")
    return df

try:
    df = load_data()

except Exception as e:
    st.error(f"Error Loading File: {e}")
    st.stop()

# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

df = df.dropna(axis=1, how='all')

numeric_cols = df.select_dtypes(include='number').columns.tolist()
object_cols = df.select_dtypes(include='object').columns.tolist()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("📌 Dashboard Filters")

if len(object_cols) > 0:

    selected_category = st.sidebar.selectbox(
        "Select Category",
        object_cols
    )

    selected_values = st.sidebar.multiselect(
        f"Filter {selected_category}",
        options=df[selected_category].dropna().unique(),
        default=df[selected_category].dropna().unique()
    )

    filtered_df = df[df[selected_category].isin(selected_values)]

else:
    filtered_df = df

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

if len(numeric_cols) > 0:

    total_value = filtered_df[numeric_cols[0]].sum()
    average_value = filtered_df[numeric_cols[0]].mean()
    max_value = filtered_df[numeric_cols[0]].max()
    min_value = filtered_df[numeric_cols[0]].min()

    col1.metric(
        "Total Value",
        f"{total_value:,.0f}"
    )

    col2.metric(
        "Average Value",
        f"{average_value:,.2f}"
    )

    col3.metric(
        "Maximum Value",
        f"{max_value:,.0f}"
    )

    col4.metric(
        "Minimum Value",
        f"{min_value:,.0f}"
    )

st.markdown("---")

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview",
    "📊 Analytics",
    "🔥 Correlations",
    "📄 Raw Data"
])

# ---------------------------------------------------
# TAB 1 — OVERVIEW
# ---------------------------------------------------

with tab1:

    st.subheader("📈 Trend Analysis")

    if len(numeric_cols) > 0:

        fig_line = px.line(
            filtered_df,
            y=numeric_cols[0],
            markers=True,
            title="Tourism Growth Trend"
        )

        fig_line.update_layout(
            template="plotly_dark",
            height=500
        )

        st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("📊 Category Distribution")

    if len(object_cols) > 0 and len(numeric_cols) > 0:

        pie_data = filtered_df.groupby(object_cols[0])[numeric_cols[0]].sum().reset_index()

        fig_pie = px.pie(
            pie_data,
            names=object_cols[0],
            values=numeric_cols[0],
            hole=0.5
        )

        fig_pie.update_layout(
            template="plotly_dark",
            height=500
        )

        st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------
# TAB 2 — ANALYTICS
# ---------------------------------------------------

with tab2:

    st.subheader("📊 Bar Chart Analysis")

    if len(object_cols) > 0 and len(numeric_cols) > 0:

        grouped_df = filtered_df.groupby(object_cols[0])[numeric_cols[0]].sum().reset_index()

        fig_bar = px.bar(
            grouped_df,
            x=object_cols[0],
            y=numeric_cols[0],
            color=numeric_cols[0],
            title="Category Wise Performance"
        )

        fig_bar.update_layout(
            template="plotly_dark",
            height=600
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("📉 Area Chart")

    if len(numeric_cols) > 0:

        fig_area = px.area(
            filtered_df,
            y=numeric_cols[0],
            title="Area Trend Visualization"
        )

        fig_area.update_layout(
            template="plotly_dark",
            height=500
        )

        st.plotly_chart(fig_area, use_container_width=True)

# ---------------------------------------------------
# TAB 3 — CORRELATION
# ---------------------------------------------------

with tab3:

    st.subheader("🔥 Correlation Heatmap")

    if len(numeric_cols) >= 2:

        corr = filtered_df[numeric_cols].corr()

        fig_heat = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Blues"
        )

        fig_heat.update_layout(
            template="plotly_dark",
            height=600
        )

        st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("🧠 AI Style Insights")

    st.info("""
    • Dashboard reveals tourism performance trends over time.
    
    • Interactive filtering enables category-level analysis.
    
    • Correlation analysis helps identify relationships between metrics.
    
    • Visual analytics supports data-driven tourism insights.
    """)

# ---------------------------------------------------
# TAB 4 — RAW DATA
# ---------------------------------------------------

with tab4:

    st.subheader("📄 Dataset Preview")

    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇ Download Filtered Data",
        csv,
        "tourism_dashboard_data.csv",
        "text/csv"
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption("Developed by Ramesh Krishan using Python, Streamlit, Pandas & Plotly")