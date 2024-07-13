import streamlit as st
import pandas as pd

# Define the file paths
hitters_file_path = './hitters.csv'
pitchers_file_path = './pitchers.csv'

# Load the CSV files
hitters_df = pd.read_csv(hitters_file_path)
pitchers_df = pd.read_csv(pitchers_file_path)

# Define the statistics for each type of player based on the provided CSV files
hitters_stats = {
    'higher_is_better': ['wOBA', '90th Perc. EV'],
    'lower_is_better': ['K%', 'BB%', 'Chase %', 'Whiff %']
}

pitchers_stats = {
    'higher_is_better': ['GB%', 'Strike%', 'Avg. Velo', '90th Perc. Velo', 'K%'],
    'lower_is_better': ['wOBA', 'BB%']
}

def display_leaderboard(df, stat, higher_is_better=True):
    if higher_is_better:
        leaderboard = df.nlargest(5, stat)
    else:
        leaderboard = df.nsmallest(5, stat)
    return leaderboard[[df.columns[0], stat]]

# Streamlit app
st.title("Baseball Leaderboard Dashboard")

tab1, tab2, tab3 = st.tabs(["Leaderboards", "Team Stats", "Player Stats"])

with tab1:
    st.header("Hitters Leaderboard")
    for stat in hitters_stats['higher_is_better']:
        st.subheader(f"Top 5 for {stat}")
        st.dataframe(display_leaderboard(hitters_df, stat, higher_is_better=True))

    for stat in hitters_stats['lower_is_better']:
        st.subheader(f"Top 5 for {stat}")
        st.dataframe(display_leaderboard(hitters_df, stat, higher_is_better=False))

    st.header("Pitchers Leaderboard")
    for stat in pitchers_stats['higher_is_better']:
        st.subheader(f"Top 5 for {stat}")
        st.dataframe(display_leaderboard(pitchers_df, stat, higher_is_better=True))

    for stat in pitchers_stats['lower_is_better']:
        st.subheader(f"Top 5 for {stat}")
        st.dataframe(display_leaderboard(pitchers_df, stat, higher_is_better=False))

with tab2:
    st.header("Team Stats")
    st.write("Hitters Team Stats")
    st.dataframe(hitters_df.groupby(hitters_df.columns[0]).mean())

    st.write("Pitchers Team Stats")
    st.dataframe(pitchers_df.groupby(pitchers_df.columns[0]).mean())

with tab3:
    st.header("Player Stats")
    player_type = st.selectbox("Select Player Type", ["Hitter", "Pitcher"])
    if player_type == "Hitter":
        player_name = st.selectbox("Select Player", hitters_df[hitters_df.columns[0]].unique())
        player_stats = hitters_df[hitters_df[hitters_df.columns[0]] == player_name]
        st.subheader(f"Stats for {player_name}")
        st.dataframe(player_stats)
        st.write("Comparison with Team Averages")
        team_avg = hitters_df.mean(numeric_only=True).to_frame().T
        st.dataframe(team_avg)
    else:
        player_name = st.selectbox("Select Player", pitchers_df[pitchers_df.columns[0]].unique())
        player_stats = pitchers_df[pitchers_df[pitchers_df.columns[0]] == player_name]
        st.subheader(f"Stats for {player_name}")
        st.dataframe(player_stats)
        st.write("Comparison with Team Averages")
        team_avg = pitchers_df.mean(numeric_only=True).to_frame().T
        st.dataframe(team_avg)
