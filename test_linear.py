import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from data_cleaning_func import *


# Load the data
# data = pd.read_csv('cleaned_data/final_data.csv')
tourney_data = pd.read_csv('data/MNCAATourneyCompactResults.csv')
tourney_teams = pd.read_csv('data/MNCAATourneySeeds.csv')
season_data = pd.read_csv('data/MRegularSeasonDetailedResults.csv')

cleaned_season_FF, cleaned_season_basic = clean_season_data(season_data)
cleaned_tourn = clean_tourn_data(tourney_data, tourney_teams)
combined_data_FF, combined_data_basic = combining_data(cleaned_season_FF, cleaned_season_basic, cleaned_tourn)
four_factor = four_factors(combined_data_FF)

# BASIC LINEAR REGRESSION
print('STARTING BASIC LINEAR REGRESSION')
# Select the relevant features and the target variable
print('Selecting features')
features = combined_data_basic[['Seed', 'PointScored', 'PointAllowed', 'FG', 'FGA', '3P', 'FT', 'FTA', 'ORB', 'DRB', 'Ast', 'TO', 'Stl', 'Blk', 'PF']]
target = combined_data_basic['Wins']

# Split the data into training and testing sets
print('Splitting the Data')
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Create linear regression model
model = LinearRegression()

# Train model
print('Training Model \n')
model.fit(X_train, y_train)

# Make predictions on test set
print('Making Predictions \n')
y_pred = model.predict(X_test)

# Coefficients
print('Model Results without Four Factor Data:\n')

print("Coefficients: \n", model.coef_)

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
model = LinearRegression()

# Train model
print('Training Model \n')
model.fit(X_train, y_train)

# Make predictions on test set
print('Making Predictions \n')
y_pred = model.predict(X_test)

# Coefficients
print('Model Results with Four Factor Data:\n')

print("Coefficients: \n", model.coef_)

# Evaluate model using mean squared error
print('Evaluating Model')
print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
print('R2: ', r2_score(y_test, y_pred).round(2))


# Use trained models to make predictions on new data

_2023 = season_data[season_data['Season'] == 2023]
print(_2023)

new_prediction = model.predict(new_data)
print('Predicted Regular Season Wins:', new_prediction)
