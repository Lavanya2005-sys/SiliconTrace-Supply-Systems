SiliconTrace: High-Performance Semiconductor Supply & Resilience Ledger
SiliconTrace is an engineering utility designed to solve the "2026 AI Supply Crunch." It combines a low-level C++ Distributed Ledger for wafer-level provenance with an XGBoost-based Predictive Engine to mitigate the Bullwhip Effect in global chip manufacturing.

🛠 Problem Statement
As of early 2026, the semiconductor industry faces massive bottlenecks in CoWoS (Chip-on-Wafer-on-Substrate) packaging and 5nm wafer allocation. Small fluctuations in consumer AI demand are being amplified into massive factory backlogs (The Bullwhip Effect). SiliconTrace provides:

Immutable Transparency: Tracking every batch from Silicon Ingot → Fab → Packaging → MediaTek Quality Control.

Predictive Buffer Management: Using ML to forecast when to increase safety stock before a supply crunch hits.

🚀 Technical Architecture
1. Provenance Ledger (C++)
The core engine is built in C++ for maximum performance and memory efficiency. It utilizes a custom hashing algorithm to ensure that wafer data cannot be tampered with as it moves through the supply tiers.

Key Features: Custom WaferBatch objects, DJB2 hashing for data integrity, and linked-node architecture for stage tracking.
As proprietary foundry supply chain data is highly confidential, this project utilizes a custom Python-based Monte Carlo simulation (data_generator.py) to generate 5,000+ rows of synthetic data, accurately modeling real-world variables like seasonality, tech trend multipliers, and geopolitical logistics risks.

2. Supply Demand Predictor (Python/XGBoost)
A machine learning module that analyzes demand patterns to predict factory load.

Model: XGBoost Regressor.

Metric: "Shortage Risk Score" (calculated by simulating demand amplification across four supply tiers).
