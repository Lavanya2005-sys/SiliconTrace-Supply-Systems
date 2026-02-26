import streamlit as st
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import os
import subprocess
import json

# -------------------------------
# 1️⃣ Page Configuration
# -------------------------------
st.set_page_config(page_title="SiliconTrace | AI Supply Intelligence", layout="wide")

st.title("🏭 SiliconTrace: Semiconductor Supply Predictor")
st.markdown("AI-Driven Supply Chain Risk & Demand Forecasting System")

# -------------------------------
# 2️⃣ Run C++ Ledger & Read Status
# -------------------------------
def run_ledger():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    exe_path = os.path.join(project_root, "silicon_trace.exe")
    json_path = os.path.join(project_root, "ledger_output.json")

    # Run ledger executable
    if os.path.exists(exe_path):
        subprocess.run([exe_path], capture_output=True)

    # Read ledger output
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            return json.load(f)

    return {"status": "unknown", "total_stages": 0}


ledger_data = run_ledger()

# -------------------------------
# 3️⃣ Load Data & Train Model
# -------------------------------
@st.cache_resource
def load_and_train():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    data_path = os.path.join(project_root, "data", "supply_logs.csv")

    df = pd.read_csv(data_path)

    X = df[['Base_Demand', 'Tech_Trend_Multiplier', 'Geopolitical_Risk', 'Retail_Orders']]
    y = df['MediaTek_Wafer_Orders']

    model = XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        random_state=42
    )

    model.fit(X, y)
    return model


model = load_and_train()

# -------------------------------
# 4️⃣ Sidebar Controls
# -------------------------------
st.sidebar.header("⚙️ Market Simulation Controls")

base_demand = st.sidebar.slider("Base Retail Demand (Units)", 50, 300, 150)
tech_trend = st.sidebar.slider("Tech Trend Multiplier (AI Boom)", 1.0, 3.0, 2.0)
risk_index = st.sidebar.slider("Geopolitical Risk Index", 0.0, 1.0, 0.5)

# -------------------------------
# 5️⃣ Prediction Logic
# -------------------------------
retail_orders = base_demand * tech_trend

input_data = pd.DataFrame({
    'Base_Demand': [base_demand],
    'Tech_Trend_Multiplier': [tech_trend],
    'Geopolitical_Risk': [risk_index],
    'Retail_Orders': [retail_orders]
})

prediction = model.predict(input_data)[0]

# Multi-tier amplification (bullwhip simulation)
amplification_factor = 1.0
for _ in range(4):
    amplification_factor *= 1.15

shortage_risk_score = (prediction * amplification_factor) / retail_orders if retail_orders != 0 else 0

# -------------------------------
# 6️⃣ Dashboard Display
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Consumer Demand", f"{int(base_demand)} units")
col2.metric("Retail Orders", f"{int(retail_orders)} units")
col3.metric("Predicted Wafer Load", f"{int(prediction)} wafers")
col4.metric("Shortage Risk Score", f"{shortage_risk_score:.2f}")

st.divider()

# -------------------------------
# 7️⃣ Bullwhip Effect Visualization
# -------------------------------
st.subheader("📊 Bullwhip Effect Amplification")

chart_data = pd.DataFrame({
    "Supply Tier": [
        "1️⃣ Consumer Demand",
        "2️⃣ Retail Orders",
        "3️⃣ Wafer Allocation"
    ],
    "Volume": [
        base_demand,
        retail_orders,
        prediction
    ]
})

st.bar_chart(chart_data.set_index("Supply Tier"))

st.divider()

# -------------------------------
# 8️⃣ Ledger Status Display
# -------------------------------
st.subheader("🔗 Ledger Integrity Status")

if ledger_data["status"] == "verified":
    st.success(f"Ledger verified successfully. Total stages tracked: {ledger_data['total_stages']}")
elif ledger_data["status"] == "compromised":
    st.error("Ledger integrity compromised!")
else:
    st.warning("Ledger status unknown.")

# -------------------------------
# 9️⃣ System Risk Indicator
# -------------------------------
if shortage_risk_score > 1.2:
    st.error("⚠️ High systemic shortage risk detected. Buffer allocation recommended.")
else:
    st.success("✅ System operating within stable allocation range.")

st.caption("SiliconTrace | AI-Powered Semiconductor Supply Intelligence System")