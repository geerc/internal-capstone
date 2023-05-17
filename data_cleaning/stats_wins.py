# import packages
import pandas as pd

# load season stats and tournament wins data
season_stats = pd.read_csv('cleaned_data/TeamSeasonAverages.csv')
tourn_wins = pd.read_csv('cleaned_data/tournament_wins.csv')

# join the two data tables
combined = season_stats.merge(tourn_wins, how='right', on=['TeamID','Season'])