import pandas as pd

def clean_season_data(raw_data):
    # cut out 2023
    raw_data = raw_data[raw_data['Season'] != 2023]

    # subset to only winning and losing teams
    wTeams = raw_data[['Season', 'WTeamID','WScore','LScore','WFGM','WFGA','WFGM3','WFTM','WFTA','WOR','WDR','WAst','WTO','WStl','WBlk','WPF']]
    lTeams = raw_data[['Season', 'LTeamID','WScore','LScore','LFGM','LFGA','LFGM3','LFTM','LFTA','LOR','LDR','LAst','LTO','LStl','LBlk','LPF']]

    # rename W and L score columns
    wTeams = wTeams.rename(columns={'WTeamID':'TeamID','WScore':'PointScored', 'LScore':'PointAllow'})
    lTeams = lTeams.rename(columns={'LTeamID':'TeamID','WScore':'PointAllow','LScore':'PointScored'})

    wTeams.columns = ['Season','TeamID','PointScored','PointAllow','FGM','FGA','FGM3','FTM','FTA','OR','DR','Ast','TO','Stl','Blk','PF']
    lTeams.columns = ['Season','TeamID','PointAllow','PointScored','FGM','FGA','FGM3','FTM','FTA','OR','DR','Ast','TO','Stl','Blk','PF']

    # concatanate together
    frames = [wTeams, lTeams]
    concat_data = pd.concat(frames)

    # rest index
    concat_data = concat_data.reset_index(drop=True)

    # Agg statistics by team
    grouped = concat_data.groupby(by=['Season','TeamID']).mean().round(2)

    # write to csv
    # grouped.to_csv('cleaned_data/TeamSeasonAverages.csv')

    return grouped

def clean_tourn_data(raw_data)