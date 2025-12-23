
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="India Cricket Analysis",
    layout="wide"
)

st.title("🇮🇳 India Cricket Performance & Toss Impact Analysis")
st.markdown("End-to-End Data Analysis using **Python, Power BI & Streamlit**")

# ---------------------------------
# LOAD DATA
# ---------------------------------
matches = pd.read_csv("final_india_matches.csv")
venue_runs = pd.read_csv("india_venue_runs.csv")
points = pd.read_csv("points_table_clean.csv")

matches['date'] = pd.to_datetime(matches['date'])

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.header(" Filters")

match_type_filter = st.sidebar.selectbox(
    "Select Match Type",
    options=["All"] + sorted(matches['match_type'].unique().tolist())
)

venue_filter = st.sidebar.selectbox(
    "Select Venue",
    options=["All"] + sorted(matches['venue'].unique().tolist())
)

# Apply filters
filtered_matches = matches.copy()

if match_type_filter != "All":
    filtered_matches = filtered_matches[
        filtered_matches['match_type'] == match_type_filter
    ]

if venue_filter != "All":
    filtered_matches = filtered_matches[
        filtered_matches['venue'] == venue_filter
    ]

# ---------------------------------
# KPI METRICS
# ---------------------------------
total_matches = filtered_matches.shape[0]
total_wins = filtered_matches['india_win'].sum()
win_percentage = round((total_wins / total_matches) * 100, 2) if total_matches > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", total_matches)
col2.metric("Matches Won", total_wins)
col3.metric("Win Percentage", f"{win_percentage}%")

# ---------------------------------
# RECENT MATCHES TABLE
# ---------------------------------
st.subheader(" Recent Matches Played by India")
st.dataframe(
    filtered_matches.sort_values("date", ascending=False).head(10),
    use_container_width=True
)

# ---------------------------------
# VENUE PERFORMANCE
# ---------------------------------
st.subheader(" Venue-wise Runs Scored by India")

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.bar(
    venue_runs['venue'],
    venue_runs['runs_off_bat']
)
ax1.set_xlabel("Venue")
ax1.set_ylabel("Total Runs")
ax1.set_xticklabels(venue_runs['venue'], rotation=45, ha='right')
st.pyplot(fig1)

# ---------------------------------
# TOSS IMPACT ANALYSIS
# ---------------------------------
st.subheader(" Impact of Toss on India’s Match Outcomes")

toss_won = filtered_matches[
    filtered_matches['toss_winner'] == "India"
]

matches_after_toss = toss_won.shape[0]
wins_after_toss = toss_won[toss_won['winner'] == "India"].shape[0]
toss_win_percentage = round(
    (wins_after_toss / matches_after_toss) * 100, 2
) if matches_after_toss > 0 else 0

c1, c2 = st.columns(2)
c1.metric("Matches After Winning Toss", matches_after_toss)
c2.metric("Win % After Winning Toss", f"{toss_win_percentage}%")

# ---------------------------------
# TOSS DECISION CHART
# ---------------------------------
st.subheader(" India Wins by Toss Decision")

toss_decision_df = toss_won[toss_won['winner'] == "India"] \
    .groupby('toss_decision') \
    .size() \
    .reset_index(name='Wins')

fig2, ax2 = plt.subplots()
ax2.bar(
    toss_decision_df['toss_decision'],
    toss_decision_df['Wins']
)
ax2.set_xlabel("Toss Decision")
ax2.set_ylabel("Matches Won")
st.pyplot(fig2)

# ---------------------------------
# POINTS TABLE
# ---------------------------------
st.subheader(" Tournament Points Table")
st.dataframe(points, use_container_width=True)

# ---------------------------------
# FOOTER
# ---------------------------------
st.markdown("---")
st.markdown(
    " **Project:** India Cricket Performance & Toss Impact Analysis  \n"
    " **Tools:** Python | Pandas | Power BI | Streamlit"
)
