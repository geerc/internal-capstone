# import packages
import pandas as pd

# load season stats and tournament wins data
stats = pd.read_csv('cleaned_data/TeamSeasonAverages.csv')
wins = pd.read_csv('cleaned_data/tournament_wins.csv')

# join the two data tables
combined = stats.merge(wins, how='right', left_on=['TeamID','Season'], right_on=['WTeamID', 'Season'])

count_teams = combined.groupby(by='Season').count()
print(count_teams)

# print
# print(combined)