import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the data
data = pd.read_csv('final_data.csv')

# Select the relevant features and the target variable
features = data[['PointsScored', 'PointsAllow', 'FGM', 'FGA', 'FGM3', 'FTM', 'FTA', 'OR', 'DR', 'Ast', 'TO', 'Stl', 'Blk', 'PF']]
target = data['Wins']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Create linear regression model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Make predictions on test set
y_pred = model.predict(X_test)

# Evaluate model using mean squared error
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)

# Use trained model to make predictions on new data
new_data = pd.DataFrame({'PointsScored': [], 'PointsAllow': [], 'FGM': [], 'FGA': [], 'FGM3': [], 'FTM': [], 'FTA': [], 'OR': [], 'DR': [], 'Ast': [], 'TO': [], 'Stl': [], 'Blk': [], 'PF': []})
new_prediction = model.predict(new_data)
print('Predicted Regular Season Wins:', new_prediction)
