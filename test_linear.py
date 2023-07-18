import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from data_cleaning_func import *
from tabulate import tabulate
import queue

import mlflow



# Load the data
# data = pd.read_csv('cleaned_data/final_data.csv')
tourney_data = pd.read_csv('data/MNCAATourneyCompactResults.csv')
tourney_teams = pd.read_csv('data/MNCAATourneySeeds.csv')
print(tourney_teams[tourney_teams['Season'] == 2023])
season_data = pd.read_csv('data/MRegularSeasonDetailedResults.csv')

cleaned_season_FF, cleaned_season_basic = clean_season_data(season_data, False)
cleaned_tourn = clean_tourn_data(tourney_data, tourney_teams, False)
print('cleaned_tourn the first time:\n', cleaned_tourn)
print('tourney_teams after first run:\n', tourney_teams)
combined_data_FF, combined_data_basic = combining_data(cleaned_season_FF, cleaned_season_basic, cleaned_tourn, False)
four_factor = four_factors(combined_data_FF)

mlflow.autolog()

# BASIC LINEAR REGRESSION
print('STARTING BASIC LINEAR REGRESSION')
# Select the relevant features and the target variable
print('Selecting features')
features = combined_data_basic[['Seed', 'PointScored', 'PointAllowed', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB', 'Ast', 'TO', 'Stl', 'Blk', 'PF']]
target = combined_data_basic['Wins']

# Split the data into training and testing sets
print('Splitting the Data')
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Create linear regression model
model_basic = LinearRegression()

# Train model
print('Training Model \n')
model_basic.fit(X_train, y_train)

# Make predictions on test set
print('Making Predictions \n')
y_pred = model_basic.predict(X_test)

# Coefficients
print('Model Results without Four Factor Data:\n')

print("Coefficients: \n", model_basic.coef_)

# Evaluate model using mean squared error
print('Evaluating Model')
print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
print('R2: ', r2_score(y_test, y_pred).round(2))


#Coefficient of Determination
# print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

# Plot outputs
plt.scatter(y_test, y_pred, color="black")
# plt.plot(X_test, y_pred, color="blue", linewidth=3)
plt.show

# FOUR FACTOR LINEAR REGRESSION
print('\nSTARTING FOUR FACTOR LINEAR REGRESSION')
print('Selecting features')
features = four_factor[['Seed','oEFG%','dEFG%','oTO%','dTO%','Reb%','dReb%','FT_rate','dFT_rate']]
target = four_factor['Wins']

# Split the data into training and testing sets
print('Splitting the Data')
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Create linear regression model
model_FF = LinearRegression()

# Train model
print('Training Model \n')
model_FF.fit(X_train, y_train)

# Make predictions on test set
print('Making Predictions \n')
y_pred = model_FF.predict(X_test)

# Coefficients
print('Model Results with Four Factor Data:\n')

print("Coefficients: \n", model_FF.coef_)

# Evaluate model using mean squared error
print('\nEvaluating Model')
print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
print('R2: ', r2_score(y_test, y_pred).round(2))


# Use trained models to make predictions on new data



_2023 = season_data[season_data['Season'] == 2023]
_,_2023_basic = clean_season_data(_2023, True)

_2023_tourn = clean_tourn_data(tourney_data, tourney_teams, True)

_, _2023_combined = combining_data(cleaned_season_FF, _2023_basic, _2023_tourn, True)
team_id = _2023_combined['TeamID']
teams = pd.read_csv('data/MTeams.csv')

features = _2023_combined[['Seed', 'PointScored', 'PointAllowed', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB', 'Ast', 'TO', 'Stl', 'Blk', 'PF']]
_2023_pred = model_basic.predict(features)

# convert pred into dataframe for concatentation
_2023_pred = pd.Series(_2023_pred)

# concatenate teams and pred together
_2023_pred = pd.concat([team_id, _2023_pred], axis=1)

# rename pred columns from '0' to 'Pred_wins'
_2023_pred = _2023_pred.rename(columns={0:'Pred_wins'})

# Merge with team names
_2023_pred = pd.merge(teams[['TeamID', 'TeamName']], _2023_pred,  how='right')
_2023_pred = pd.merge(_2023_pred, _2023_combined[['TeamID','Seed']], how='left')

print(tabulate(_2023_pred.sort_values(by='Pred_wins', ascending=False), headers='keys', tablefmt='psql'))
_2023_pred.to_csv('cleaned_data/PRED_2023.csv')

# CHECK PRED BRACKET AGAINST ACTUAL BRACKET
bracket_2023 = [[[1104, 1394], [1268, 1452], [1361, 1158], [1438, 1202], [1166, 1301], [1124, 1364], [1281, 1429], [1112, 1343]], [[1345, 1192], [1272 ,1194], [1181, 1331], [1397, 1418], [1246, 1344], [1243, 1286], [1277, 1425], [1266, 1436]], [[1222, 1297], [1234, 1120], [1274, 1179], [1231, 1245], [1235, 1338], [1462, 1244], [1401, 1336], [1400, 1159]], [[1242, 1224], [1116, 1228], [1388, 1433], [1163, 1233], [1395, 1113], [1211, 1213], [1321, 1129], [1417, 1421]]]

_2023_pred = _2023_pred.sort_values(by='Pred_wins', ascending=False).reset_index(drop=True)

reg_count = 0
round2 = queue.Queue()
sweet16 = queue.Queue()
elite8 = queue.Queue()
final4 = queue.Queue()
championship = queue.Queue()

for region in bracket_2023:
    if reg_count == 0:
        region_name = 'South'
    if reg_count == 1:
        region_name = 'East'
    if reg_count == 2:
        region_name = 'Midwest'
    if reg_count == 3:
        region_name = 'West'

    print('\nRegion: ', region_name)
    reg_count += 1



    for matchup in region:
        high_seed = _2023_pred.loc[_2023_pred['TeamID'] == matchup[0]]['TeamName'].values[0]
        high_seed_pred_wins = _2023_pred.loc[_2023_pred['TeamID'] == matchup[0]]['Pred_wins'].values[0]
        low_seed = _2023_pred.loc[_2023_pred['TeamID'] == matchup[1]]['TeamName'].values[0]
        low_seed_pred_wins = _2023_pred.loc[_2023_pred['TeamID'] == matchup[1]]['Pred_wins'].values[0]


        if high_seed_pred_wins > low_seed_pred_wins:
            winning_team = high_seed
            losing_team = low_seed
        elif high_seed_pred_wins < low_seed_pred_wins:
            winning_team = low_seed
            losing_team = high_seed
    
        print(winning_team.upper(), ' beats ', losing_team.lower())

        round2.put(winning_team)

print('\nROUND OF 32')
while (round2.qsize()) > 0:
    team1 = round2.get()
    team2 = round2.get()

    team1_pred = _2023_pred.loc[_2023_pred['TeamName'] == team1]['Pred_wins'].values[0]
    team2_pred = _2023_pred.loc[_2023_pred['TeamName'] == team2]['Pred_wins'].values[0]


    if team1_pred > team2_pred:
        winning_team = team1
        losing_team = team2
    elif team1_pred < team2_pred:
        winning_team = team2
        losing_team = team1

    print(team1.upper(), ' beats ', team2.lower())

    sweet16.put(team1)

print('\nSWEET SIXTEEN')
while sweet16.qsize() != 0:
    team1 = sweet16.get()
    team2 = sweet16.get()

    team1_pred = _2023_pred.loc[_2023_pred['TeamName'] == team1]['Pred_wins'].values[0]
    team2_pred = _2023_pred.loc[_2023_pred['TeamName'] == team2]['Pred_wins'].values[0]


    if team1_pred > team2_pred:
        winning_team = team1
        losing_team = team2
    elif team1_pred < team2_pred:
        winning_team = team2
        losing_team = team1

    print(team1.upper(), ' beats ', team2.lower())

    elite8.put(team1)

print('\nELITE EIGHT')
while elite8.qsize() != 0:
    team1 = elite8.get()
    team2 = elite8.get()

    team1_pred = _2023_pred.loc[_2023_pred['TeamName'] == team1]['Pred_wins'].values[0]
    team2_pred = _2023_pred.loc[_2023_pred['TeamName'] == team2]['Pred_wins'].values[0]


    if team1_pred > team2_pred:
        winning_team = team1
        losing_team = team2
    elif team1_pred < team2_pred:
        winning_team = team2
        losing_team = team1

    print(team1.upper(), ' beats ', team2.lower())

    final4.put(team1)

print('\nFINAL FOUR')
while final4.qsize() != 0:
    team1 = final4.get()
    team2 = final4.get()

    team1_pred = _2023_pred.loc[_2023_pred['TeamName'] == team1]['Pred_wins'].values[0]
    team2_pred = _2023_pred.loc[_2023_pred['TeamName'] == team2]['Pred_wins'].values[0]


    if team1_pred > team2_pred:
        winning_team = team1
        losing_team = team2
    elif team1_pred < team2_pred:
        winning_team = team2
        losing_team = team1

    print(team1.upper(), ' beats ', team2.lower())

    championship.put(team1)

print('\nCHAMPIONSHIP')
team1 = championship.get()
team2 = championship.get()

team1_pred = _2023_pred.loc[_2023_pred['TeamName'] == team1]['Pred_wins'].values[0]
team2_pred = _2023_pred.loc[_2023_pred['TeamName'] == team2]['Pred_wins'].values[0]


if team1_pred > team2_pred:
    winning_team = team1
    losing_team = team2
elif team1_pred < team2_pred:
    winning_team = team2
    losing_team = team1

print('NCAA NATIONAL CHAMPION: ', winning_team)
print('Runner up: ', losing_team)