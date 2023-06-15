import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from data_cleaning_func import *
from tabulate import tabulate
from bracket import bracket



# Load the data
# data = pd.read_csv('cleaned_data/final_data.csv')
tourney_data = pd.read_csv('data/MNCAATourneyCompactResults.csv')
tourney_teams = pd.read_csv('data/MNCAATourneySeeds.csv')
season_data = pd.read_csv('data/MRegularSeasonDetailedResults.csv')

cleaned_season_FF, cleaned_season_basic = clean_season_data(season_data, False)
cleaned_tourn = clean_tourn_data(tourney_data, tourney_teams, False)
combined_data_FF, combined_data_basic = combining_data(cleaned_season_FF, cleaned_season_basic, cleaned_tourn, False)
four_factor = four_factors(combined_data_FF)

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
print('Evaluating Model')
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
print('Predicted Regular Season Wins:', _2023_pred)

# convert pred into dataframe for concatentation
_2023_pred = pd.Series(_2023_pred)

# concatenate teams and pred together
_2023_pred = pd.concat([team_id, _2023_pred], axis=1)

# rename pred columns from '0' to 'Pred_wins'
_2023_pred = _2023_pred.rename(columns={0:'Pred_wins'})

# Merge with team names
_2023_pred = pd.merge(teams[['TeamID', 'TeamName']], _2023_pred,  how='right')

print(tabulate(_2023_pred, headers='keys', tablefmt='psql'))