
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load data from CSV file
file_path = 'data.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Assuming your CSV file has columns similar to the synthetic data
X = df[['DayOfWeek', 'TimeOfDay', 'IsSpecialDay', 'SlotNumber','Reservations', 'TotalAvailableSpots', 'PercentageAvailableSpots', 'CustomerType', 'MembershipStatus']]
y = df['DynamicPrice']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)


# Now, you can use the trained model to make predictions on new data
# For example, assuming 'new_reservation_features' is a new set of features
new_reservation_features = pd.DataFrame({
    'DayOfWeek': [2],
    'TimeOfDay': [1],
    'IsSpecialDay': [1],
    'SlotNumber' : [2],
    'Reservations': [1],
    'TotalAvailableSpots': [5],
    'PercentageAvailableSpots': [1],
    'CustomerType': [0],
    'MembershipStatus': [2]
})

predicted_price = model.predict(new_reservation_features)
new_reservation_features['DynamicPrice'] = predicted_price.flatten()

new_reservation_features.to_csv(file_path, mode='a', header=False, index=False)

print(f"Predicted Price: ${predicted_price[0]:.2f}")
