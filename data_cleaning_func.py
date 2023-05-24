import pandas as pd

def clean_season_data(raw_data):
    # cut out 2023
    raw_data = raw_data[raw_data['Season'] != 2023]

    # subset to only winning and losing teams

    # wTeams = raw_data[['Season', 'WTeamID','WScore','LScore','WFGM','WFGA','WFGM3','WFTM','WFTA','WOR','WDR','WAst','WTO','WStl','WBlk','WPF']]
    # lTeams = raw_data[['Season', 'LTeamID','WScore','LScore','LFGM','LFGA','LFGM3','LFTM','LFTA','LOR','LDR','LAst','LTO','LStl','LBlk','LPF']]
    wTeams = raw_data.drop(columns=['DayNum','WScore','LTeamID','LScore','WLoc','NumOT','WFGA3','WAst','WStl','WBlk','WPF','LFGA3','LAst','LStl','LBlk','LPF'])
    lTeams = raw_data.drop(columns=['DayNum','WScore','WTeamID','LScore','WLoc','NumOT','WFGA3','WAst','WStl','WBlk','WPF','LFGA3','LAst','LStl','LBlk','LPF'])

    # rename columns
    wTeams = wTeams.rename(columns={'WTeamID':'TeamID','WFGM':'FG','WFGA':'FGA','WFGM3':'3P','WFTM':'FT','WFTA':'FTA','WOR':'OR','WDR':'DR','WTO':'TO','LFGM':'oppFG','LFGA':'oppFGA','LFGM3':'opp3P','LFTM':'oppFT','LFTA':'oppFTA','LOR':'oppOR','LDR':'oppDR','LTO':'oppTO'})
    lTeams = lTeams.rename(columns={'LTeamID':'TeamID','WFGM':'oppFG','WFGA':'oppFGA','WFGM3':'opp3P','WFTM':'oppFT','WFTA':'oppFTA','WOR':'oppOR','WDR':'oppDR','WTO':'oppTO','LFGM':'FG','LFGA':'FGA','LFGM3':'3P','LFTM':'FT','LFTA':'FTA','LOR':'OR','LDR':'DR','LTO':'TO'})

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

    # write to csv
    combined.to_csv('cleaned_data/final_data.csv')
    
    return combined

# def four_factors(data):
#     data['oEFG'] = (data['FGM'] + 0.5 * data['FGM3']) / data['FGA']
#     data['oTO%'] = data['TO'] / (data['FGA'] + 0.44 * data['FTA'] + data['TO'])