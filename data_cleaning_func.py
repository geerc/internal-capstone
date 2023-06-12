import pandas as pd

def clean_season_data(raw_data):
    # cut out 2023
    raw_data = raw_data[raw_data['Season'] != 2023]

    # subset to only winning and losing teams

    wTeams = raw_data[['Season', 'WTeamID','WScore','LScore','WFGM','LFGM','WFGA','LFGA','WFGM3','LFGM3','WFTM','LFTM','WFTA','LFTA','WOR','LOR','WDR','LDR','WAst','WTO','LTO','WStl','WBlk','WPF']]
    lTeams = raw_data[['Season', 'LTeamID','WScore','LScore','WFGM','LFGM','WFGA','LFGA','WFGM3','LFGM3','WFTM','LFTM','WFTA','LFTA','WOR','LOR','WDR','LDR','LAst','WTO','LTO','LStl','LBlk','LPF']]
    # wTeams = raw_data.drop(columns=['DayNum','LTeamID','WLoc','NumOT','WFGA3','LFGA3'])
    # lTeams = raw_data.drop(columns=['DayNum','WTeamID','WLoc','NumOT','WFGA3','LFGA3'])

    # rename columns
    wTeams = wTeams.rename(columns={'WTeamID':'TeamID','WScore':'PointScored','LScore':'PointAllow','WFGM':'FG','WFGA':'FGA','WFGM3':'3P','WFTM':'FT','WFTA':'FTA','WOR':'ORB','WDR':'DRB','WAst':'Ast','WTO':'TO','WStl':'Stl','WBlk':'Blk','WPF':'PF','LFGM':'oppFG','LFGA':'oppFGA','LFGM3':'opp3P','LFTM':'oppFT','LFTA':'oppFTA','LOR':'oppOR','LDR':'oppDR','LTO':'oppTO'})
    lTeams = lTeams.rename(columns={'LTeamID':'TeamID','LScore':'PointScored','WScore':'PointAllow','WFGM':'oppFG','WFGA':'oppFGA','WFGM3':'opp3P','WFTM':'oppFT','WFTA':'oppFTA','WOR':'oppORB','WDR':'oppDRB','LAst':'Ast','LTO':'TO','LStl':'Stl','LBlk':'Blk','LPF':'PF','LFGM':'FG','LFGA':'FGA','LFGM3':'3P','LFTM':'FT','LFTA':'FTA','LOR':'OR','LDR':'DR','LTO':'TO'})

    # concatanate together
    frames = [wTeams, lTeams]
    concat_data = pd.concat(frames)

    # rest index
    concat_data = concat_data.reset_index(drop=True)

    # Agg statistics by team
    grouped = concat_data.groupby(by=['Season','TeamID']).mean().round(2)

    # write to csv
    grouped.to_csv('cleaned_data/TeamSeasonAverages.csv')

    return grouped

def clean_tourn_data(raw_tourney, raw_teams):
    # retain only necessary columns
    # raw_teams = raw_teams[['Season','TeamID']]

    # Remove prefix for region in seed col
    raw_teams['Seed'] = raw_teams['Seed'].str[1:]

    # remove a and b seed suffixes
    raw_teams['Seed'] = raw_teams['Seed'].str.removesuffix('a')
    raw_teams['Seed'] = raw_teams['Seed'].str.removesuffix('b')

    # remove data before 2003 (no season data) and data for 2023 (no tourney data)
    raw_teams = raw_teams[(raw_teams['Season'] >= 2003) & (raw_teams['Season'] < 2023)]

    # remove data before 2003 (no season data) and data for 2023 (no tourney data)
    raw_tourney = raw_tourney[(raw_tourney['Season'] >= 2003) & (raw_tourney['Season'] < 2023)]
    # Retain only necessary columns
    raw_tourney = raw_tourney[['Season', 'WTeamID','WScore']]

    # group by season and winning team, provides count of all teams wins in tournament year
    grouped = raw_tourney.groupby(by=['Season', 'WTeamID']).count()
    # rename column
    grouped = grouped.rename(columns={'WScore':'Wins'})

    # right join to include teams that had 0 tournament wins
    full_teams = grouped.merge(raw_teams, how='right', left_on=['Season','WTeamID'], right_on=['Season','TeamID'])

    # fill na with 0
    full_teams['Wins'] = full_teams['Wins'].fillna(0)

    # cast to float to int for wins
    full_teams = full_teams.astype({'Wins':'int'})
    # print(full_teams)

    # write to csv
    full_teams.to_csv('cleaned_data/tournament_wins.csv')

    return full_teams

def combining_data(cleaned_season, cleaned_tourn_wins):
    # join the two data tables
    combined = cleaned_season.merge(cleaned_tourn_wins, how='right', on=['TeamID','Season'])

    # remove extra index col from merge
    # combined = combined.drop(columns=['Unnamed: 0'])

    # removing NaN rows
    combined.dropna(how='all')

    # write to csv
    combined.to_csv('cleaned_data/final_data.csv')
    
    return combined

def four_factors(data):
    data['oEFG%'] = (data['FG'] + 0.5 * data['3P']) / data['FGA']
    data['dEFG%'] = (data['oppFG'] + 0.5 * data['opp3P']) / data['oppFGA']
    data['oTO%'] = data['TO'] / (data['FGA'] + 0.44 * data['FTA'] + data['TO'])
    data['dTO%'] = data['oppTO'] / (data['oppFGA'] + 0.44 * data['oppFTA'] + data['oppTO'])
    data['Reb%'] = data['ORB'] / (data['ORB'] + data['oppDRB'])
    data['dReb%'] = data['DRB'] / (data['oppORB'] + data['DRB'])
    data['FT_rate'] = data['FTA'] / data['FGA']
    data['dFT_rate'] = data['oppFTA'] / data['oppFGA']

    data = data[['TeamID','Seed','oEFG%','dEFG%','oTO%','dTO%','Reb%','dReb%','FT_rate','dFT_rate']]

    return data