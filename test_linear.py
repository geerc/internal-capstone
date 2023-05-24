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

cleaned_season = clean_season_data(season_data)
cleaned_tourn = clean_tourn_data(tourney_data, tourney_teams)
data = combining_data(cleaned_season, cleaned_tourn)

# Select the relevant features and the target variable
print('Selecting features')
features = data[['PointScored', 'PointAllow', 'FGM', 'FGA', 'FGM3', 'FTM', 'FTA', 'OR', 'DR', 'Ast', 'TO', 'Stl', 'Blk', 'PF']]
target = data['Wins']

# Split the data into training and testing sets
print('Splitting the Data')
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Create linear regression model
model = LinearRegression()

# Train model
print('Training Model')
model.fit(X_train, y_train)

# Make predictions on test set
print('Making Predictions')
y_pred = model.predict(X_test)

# Coefficients
print("Coefficients: \n", model.coef_)
# Evaluate model using mean squared error
print('Evaluating Model')
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)
#Coefficient of Determination
print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

# Plot outputs
plt.scatter(y_test, y_pred, color="black")
# plt.plot(X_test, y_pred, color="blue", linewidth=3)
plt.show

# # Use trained model to make predictions on new data
# new_data = pd.DataFrame({'PointScored': [], 'PointAllow': [], 'FGM': [], 'FGA': [], 'FGM3': [], 'FTM': [], 'FTA': [], 'OR': [], 'DR': [], 'Ast': [], 'TO': [], 'Stl': [], 'Blk': [], 'PF': []})
# new_prediction = model.predict(new_data)
# print('Predicted Regular Season Wins:', new_prediction)
