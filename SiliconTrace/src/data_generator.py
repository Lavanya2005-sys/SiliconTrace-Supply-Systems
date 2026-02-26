import pandas as pd
import numpy as np
import os

print("Generating 5,000 rows of synthetic semiconductor supply data...")

# Set random seed for reproducibility
np.random.seed(42)

# Generate 5000 days of data (roughly 13 years)
days = np.arange(1, 5001)

# Feature 1: Base Retail Demand (with seasonal cycles)
base_demand = 100 + 20 * np.sin(days / 365.0 * 2 * np.pi) 

# Feature 2: Tech Trend Multiplier (AI booms, etc.)
# Every ~1000 days there is a new tech cycle
tech_trend = 1.0 + 0.5 * (days / 5000) + 0.3 * np.sin(days / 1000.0)

# Feature 3: Geopolitical/Logistics Risk Index (0 to 1)
# Random spikes in supply chain delays
risk_index = np.random.beta(a=2, b=10, size=5000)

# Calculate Final Retail Orders with some random noise
retail_orders = base_demand * tech_trend + np.random.normal(0, 5, 5000)

# The "Bullwhip Effect" Formula for MediaTek Wafer Orders
# Wafer orders overreact to retail orders and are worsened by the Risk Index
wafer_orders = (retail_orders * 1.3) + (retail_orders * risk_index * 0.5) + np.random.normal(0, 10, 5000)

# Create DataFrame
df = pd.DataFrame({
    'Day': days,
    'Base_Demand': np.round(base_demand, 2),
    'Tech_Trend_Multiplier': np.round(tech_trend, 2),
    'Geopolitical_Risk': np.round(risk_index, 3),
    'Retail_Orders': np.round(retail_orders, 0),
    'MediaTek_Wafer_Orders': np.round(wafer_orders, 0)
})

# Save to CSV
current_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(current_dir, '../data/supply_logs.csv')

# Ensure data directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

df.to_csv(output_path, index=False)
print(f"Success! Highly realistic dataset saved to {output_path}")