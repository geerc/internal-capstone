# import packages
import pandas as pd

# load season stats and tournament wins data
season_stats = pd.read_csv('cleaned_data/TeamSeasonAverages.csv')
tourn_wins = pd.read_csv('cleaned_data/tournament_wins.csv')

# join the two data tables
combined = season_stats.merge(tourn_wins, how='right', on=['TeamID','Season'])

# remove extra index col from merge
combined = combined.drop(columns=['Unnamed: 0'])

# write to csv
combined.to_csv('cleaned_data/final_data.csv')