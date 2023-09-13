import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

data = {
    'DayOfWeek': np.random.randint(1, 8, 100),  
    'TimeOfDay': np.random.randint(1, 4, 100), 
    'IsSpecialDay': np.random.randint(0, 2, 100),  
    'HistoricalReservations': np.random.randint(0, 100, 100), 
    'Occupancy': np.random.randint(0, 50, 100),  # Real-time
    'TotalAvailableSpots': np.random.randint(50, 100, 100),  # Total available spots
    'PercentageAvailableSpots': np.random.uniform(0.5, 1.0, 100),  
    'CustomerType': np.random.randint(0, 2, 100),  
    'MembershipStatus': np.random.randint(0, 2, 100),  
    'DynamicPrice': np.random.randint(10, 50, 100)
}

# Create a DataFrame from the synthetic data
df = pd.DataFrame(data)

# Split the data into features (X) and target variable (y)
X = df[['DayOfWeek', 'TimeOfDay', 'IsSpecialDay', 'HistoricalReservations', 'Occupancy', 'TotalAvailableSpots', 'PercentageAvailableSpots', 'CustomerType', 'MembershipStatus']]
y = df['DynamicPrice']

# Splitting the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


mse = mean_squared_error(y_test, y_pred)

#need to access this in real time
new_reservation_features = np.array([[4, 2, 0, 30, 25, 80, 0.75, 1, 1]])
predicted_price = model.predict(new_reservation_features)
print(f"Predicted Price: ${predicted_price[0]:.2f}")
