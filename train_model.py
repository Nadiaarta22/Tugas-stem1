import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import json

# Set seed for reproducibility
np.random.seed(42)

# Generate 1000 synthetic samples
num_samples = 1000

# Features:
# 1. nutrient_runoff: 0 to 100 %
# 2. co2_emissions: 0 to 1000 ppm (ambient CO2 is ~400, but local emissions can go higher)
# 3. water_temp: 15 to 35 C
# 4. industrial_waste: 0 to 100 %
nutrient_runoff = np.random.uniform(0, 100, num_samples)
co2_emissions = np.random.uniform(200, 1000, num_samples)
water_temp = np.random.uniform(15, 35, num_samples)
industrial_waste = np.random.uniform(0, 100, num_samples)

# Formula for Risk Percentage (base)
# CO2 emission and industrial waste have high impact on acidification/pollution
co2_norm = (co2_emissions - 200) / 800.0
runoff_norm = nutrient_runoff / 100.0
temp_norm = (water_temp - 15.0) / 20.0
waste_norm = industrial_waste / 100.0

# Base Risk (0 - 100 %)
base_risk = (
    0.40 * co2_norm +
    0.25 * runoff_norm +
    0.20 * temp_norm +
    0.15 * waste_norm
) * 100.0

# Add noise (standard deviation of 4%)
noise = np.random.normal(0, 4, num_samples)
risk_percentage = np.clip(base_risk + noise, 0.0, 100.0)

# Create DataFrame
df = pd.DataFrame({
    'nutrient_runoff': nutrient_runoff,
    'co2_emissions': co2_emissions,
    'water_temp': water_temp,
    'industrial_waste': industrial_waste,
    'risk_probability': risk_percentage
})

# Separate features and target
X = df[['nutrient_runoff', 'co2_emissions', 'water_temp', 'industrial_waste']]
y = df['risk_probability']

# Train Random Forest Regressor
model = RandomForestRegressor(n_estimators=50, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, 'model.joblib')
print("Model saved to model.joblib")

# Save feature importances and basic stats for offline mode config
importances = model.feature_importances_
features = list(X.columns)
model_info = {
    'features': features,
    'importances': {features[i]: float(importances[i]) for i in range(len(features))},
    'intercept_reference': 0.0,
}

with open('model_info.json', 'w') as f:
    json.dump(model_info, f, indent=4)
print("Model info saved to model_info.json")
