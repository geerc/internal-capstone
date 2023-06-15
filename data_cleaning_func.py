import pandas as pd
import numpy as np


def clean_season_data(raw_data):
    # cut out 2023
    raw_data = raw_data[raw_data['Season'] != 2023]

    # subset to only winning and losing teams
    wTeams_FF = raw_data[['Season', 'WTeamID','WScore','LScore','WFGM','LFGM','WFGA','LFGA','WFGM3','LFGM3','WFTM','LFTM','WFTA','LFTA','WTO','LTO','WOR','LOR','WDR','LDR']]
    lTeams_FF = raw_data[['Season', 'LTeamID','WScore','LScore','WFGM','LFGM','WFGA','LFGA','WFGM3','LFGM3','WFTM','LFTM','WFTA','LFTA','LTO','WTO','WOR','LOR','WDR','LDR']]

    wTeams_basic = raw_data[['Season','WTeamID','WScore','LScore','WFGM','WFGA','WFGM3','WFGA3','WFTM','WFTA','WOR','WDR','WAst','WTO','WStl','WBlk','WPF']]
    lTeams_basic = raw_data[['Season','LTeamID','WScore','LScore','LFGM','LFGA','LFGM3','LFGA3','LFTM','LFTA','LOR','LDR','LAst','LTO','LStl','LBlk','LPF']]

    # rename columns
    wTeams_FF = wTeams_FF.rename(columns={'WTeamID':'TeamID','WScore':'PointScored','LScore':'PointAllow','WFGM':'FG','LFGM':'oppFG','WFGA':'FGA','LFGA':'oppFGA','WFGM3':'3P','LFGM3':'opp3P','WFTM':'FT','LFTM':'oppFT','WFTA':'FTA','LFTA':'oppFTA','WOR':'ORB','LOR':'oppORB','WDR':'DRB','LDR':'oppDRB','WTO':'TO','LTO':'oppTO'})
    lTeams_FF = lTeams_FF.rename(columns={'LTeamID':'TeamID','LScore':'PointScored','WScore':'PointAllow','LFGM':'FG','WFGM':'oppFG','LFGA':'FGA','WFGA':'oppFGA','LFGM3':'3P','WFGM3':'opp3P','LFTM':'FT','WFTM':'oppFT','LFTA':'FTA','WFTA':'oppFTA','LOR':'ORB','WOR':'oppORB','LDR':'DRB','WDR':'oppDRB','LTO':'TO','WTO':'oppTO'})
    
    wTeams_basic = wTeams_basic.rename(columns={'WTeamID':'TeamID','WScore':'PointScored','LScore':'PointAllowed','WFGM':'FG','WFGA':'FGA','WFGM3':'3P','WFGA3':'3PA','WFTM':'FT','WFTA':'FTA','WOR':'ORB','WDR':'DRB','WAst':'Ast','WTO':'TO','WStl':'Stl','WBlk':'Blk','WPF':'PF'})
    lTeams_basic = lTeams_basic.rename(columns={'LTeamID':'TeamID','LScore':'PointScored','WScore':'PointAllowed','LFGM':'FG','LFGA':'FGA','LFGM3':'3P','LFGA3':'3PA','LFTM':'FT','LFTA':'FTA','LOR':'ORB','LDR':'DRB','LAst':'Ast','LTO':'TO','LStl':'Stl','LBlk':'Blk','LPF':'PF'})

    # concatanate together
    frames = (wTeams_FF, lTeams_FF)
    concat_data_FF = pd.concat(frames)

    frames = (wTeams_basic, lTeams_basic)
    concat_data_basic = pd.concat(frames)

    # rest index
    concat_data_FF = concat_data_FF.reset_index(drop=True)
    concat_data_basic = concat_data_basic.reset_index(drop=True)

    # Agg statistics by team
    grouped_FF = concat_data_FF.groupby(by=['Season','TeamID']).mean().round(2)
    grouped_basic = concat_data_basic.groupby(by=['Season','TeamID']).mean().round(2)

    # write to csv
    grouped_FF.to_csv('cleaned_data/TeamSeasonAveragesFF.csv')
    grouped_basic.to_csv('cleaned_data/TeamSeasonAveragesBasic.csv')

    # return grouped_FF, grouped_basic
    return grouped_FF, grouped_basic

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

    # write to csv
    full_teams.to_csv('cleaned_data/tournament_wins.csv')

    return full_teams

def combining_data(cleaned_season_FF,cleaned_season_basic, cleaned_tourn_wins):
    # join the two data tables
    combined_FF = cleaned_season_FF.merge(cleaned_tourn_wins, how='right', on=['TeamID','Season'])
    combined_basic = cleaned_season_basic.merge(cleaned_tourn_wins, how='right', on=['TeamID','Season'])

    # remove extra index col from merge
    # combined = combined.drop(columns=['Unnamed: 0'])

    # write to csv
    combined_FF.to_csv('cleaned_data/combined_data_FF.csv')
    combined_basic.to_csv('cleaned_data/final_data_basic.csv')
    
    # return combined
    return combined_FF, combined_basic

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

    data.to_csv('cleaned_data/final_data_FF')
    return data