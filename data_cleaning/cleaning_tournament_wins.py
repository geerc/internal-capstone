# get the total wins for each team in the tournaments from 2003 - 2022

# import packages
import pandas as pd

# load data
tourney_data = pd.read_csv('data/MNCAATourneyCompactResults.csv')
tourney_teams = pd.read_csv('data/MNCAATourneySeeds.csv')

# reatain only necessary columns
tourney_teams = tourney_teams[['Season','TeamID']]
# remove data before 2003 (no season data) and data for 2023 (no tourney data)
tourney_teams = tourney_teams[(tourney_teams['Season'] >= 2003) & (tourney_teams['Season'] < 2023)]

# remove data before 2003 (no season data) and data for 2023 (no tourney data)
tourney_data = tourney_data[(tourney_data['Season'] >= 2003) & (tourney_data['Season'] < 2023)]
# Retain only necessary columns
tourney_data = tourney_data[['Season', 'WTeamID','WScore']]

# group by season and winning team, provides count of all teams wins in tournament year
grouped = tourney_data.groupby(by=['Season', 'WTeamID']).count()
# rename column
grouped = grouped.rename(columns={'WScore':'Wins'})

# right join to include teams that had 0 tournament wins
full_teams = grouped.merge(tourney_teams, how='right', left_on=['Season','WTeamID'], right_on=['Season','TeamID'])

# fill na with 0
full_teams['Wins'] = full_teams['Wins'].fillna(0)

# cast to float to int for wins
full_teams = full_teams.astype({'Wins':'int'})
print(full_teams)

# print(grouped)
full_teams.to_csv('cleaned_data/tournament_wins.csv')