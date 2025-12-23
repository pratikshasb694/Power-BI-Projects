import pandas as pd

deliveries=pd.read_csv(r"C:\Users\QSP-Trainer\Desktop\INDIAN_CRICKET_PROJECT\INDIAN_CRICKET_DATASET\deliveries.csv")
matches=pd.read_csv(r"C:\Users\QSP-Trainer\Desktop\INDIAN_CRICKET_PROJECT\INDIAN_CRICKET_DATASET\matches.csv")
points_table=pd.read_csv(r"C:\Users\QSP-Trainer\Desktop\INDIAN_CRICKET_PROJECT\INDIAN_CRICKET_DATASET\points_table.csv")

print("files loaded sucessfully!")

print("deliveries:",deliveries.shape)
print("matches:",matches.shape)
print("points_table:",points_table.shape)

#filter india matches 
india_matches=matches[(matches['team1']=="India")|(matches['team2']=="India")]
print("India amtches:",india_matches.shape)

#create india win column
india_matches['india_win']=india_matches['winner'].apply(lambda x: 1 if x== 'India' else 0)

#Basic analysis
total_matches=india_matches.shape[0]
total_wins=india_matches['india_win'].sum()
win_percentage=round((total_wins/total_matches)*100,2)


print("Total Matches:",total_matches)
print("Total Wins:",total_wins)
print("Win Percentage",win_percentage)

#Deliveries analysis 
#filter where india batted
india_batting=deliveries[deliveries['batting_team']=="India"]

#total runs by india
total_runs=india_batting['runs_off_bat'].sum()

#total wickets lost by india
total_wickets=india_batting['player_dismissed'].notna().sum()

print('Total runs by India: ',total_runs)
print('Total Wickets Lost:', total_wickets)

#venue wise performance

venue_runs=india_batting.groupby('venue')['runs_off_bat'].sum().reset_index()
venue_wickets=india_batting.groupby('venue')['player_dismissed'].count().reset_index()

india_matches.to_csv("final_india_matches.csv", index=False)
venue_runs.to_csv("india_venue_runs.csv", index=False)
points_table.to_csv("points_table_clean.csv", index=False)

print("Final CSV files cretaed")