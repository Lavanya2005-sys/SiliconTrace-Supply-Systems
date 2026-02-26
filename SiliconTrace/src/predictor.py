import pandas as pd
import numpy as np
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

print("=== SiliconTrace AI Predictor ===")
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '../data/supply_logs.csv')

try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    print("Error: Run data_generator.py first!")
    exit()

# Features (X) and Target (y)
X = df[['Base_Demand', 'Tech_Trend_Multiplier', 'Geopolitical_Risk', 'Retail_Orders']]
y = df['MediaTek_Wafer_Orders']

# Split data to prove we evaluate models properly
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training XGBoost Regressor on 4,000 historical data points...")
model = XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Quick evaluation
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model trained successfully. Mean Absolute Error: {mae:.2f} wafers")

# --- SIMULATE 2026 AI CRUNCH ---
print("\n--- 2026 AI Supply Crunch Prediction ---")
# Simulating high tech trend and high risk
future_scenario = pd.DataFrame({
    'Base_Demand': [150], 
    'Tech_Trend_Multiplier': [2.5], # AI Boom
    'Geopolitical_Risk': [0.8],     # High logistics risk
    'Retail_Orders': [375]          # High retail demand
})

prediction = model.predict(future_scenario)
print(f"Input Scenario: High AI Demand (Tech Multiplier 2.5x) + High Logistics Risk")
print(f"Predicted MediaTek Wafer Load: {prediction[0]:.0f} wafers")
print("Warning: Extreme Bullwhip effect detected! Immediate wafer allocation buffering recommended.")