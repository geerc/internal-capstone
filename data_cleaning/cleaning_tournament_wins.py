import pandas as pd

data = pd.read_csv('data/MNCAATourneyCompactResults.csv')

data = data[data['Season'] >= 2003]
data = data[['Season', 'WTeamID','WScore']]

grouped = data.groupby(by=['Season', 'WTeamID']).count()
grouped = grouped.rename(columns={'WScore':'Wins'})

print(grouped)
grouped.to_csv('cleaned_data/tournament_wins.csv')