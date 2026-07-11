import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import json

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

MODEL_FILE = 'model.joblib'
INFO_FILE = 'model_info.json'

def load_or_train_model():
    if not os.path.exists(MODEL_FILE) or not os.path.exists(INFO_FILE):
        print("Model atau informasi tidak ditemukan. Melatih model sekarang...")
        try:
            # Run train_model.py
            subprocess.run(['python', 'train_model.py'], check=True)
        except Exception as e:
            print(f"Gagal melatih model melalui script: {e}")
            # Direct fallback training in-memory if script fails
            import numpy as np
            import pandas as pd
            from sklearn.ensemble import RandomForestRegressor
            
            print("Menjalankan pelatihan fallback di memori...")
            np.random.seed(42)
            nutrient_runoff = np.random.uniform(0, 100, 100)
            co2_emissions = np.random.uniform(200, 1000, 100)
            water_temp = np.random.uniform(15, 35, 100)
            industrial_waste = np.random.uniform(0, 100, 100)
            
            co2_norm = (co2_emissions - 200) / 800.0
            runoff_norm = nutrient_runoff / 100.0
            temp_norm = (water_temp - 15.0) / 20.0
            waste_norm = industrial_waste / 100.0
            
            base_risk = (0.40 * co2_norm + 0.25 * runoff_norm + 0.20 * temp_norm + 0.15 * waste_norm) * 100.0
            risk_percentage = np.clip(base_risk + np.random.normal(0, 4, 100), 0.0, 100.0)
            
            df = pd.DataFrame({
                'nutrient_runoff': nutrient_runoff,
                'co2_emissions': co2_emissions,
                'water_temp': water_temp,
                'industrial_waste': industrial_waste,
                'risk_probability': risk_percentage
            })
            
            X = df[['nutrient_runoff', 'co2_emissions', 'water_temp', 'industrial_waste']]
            y = df['risk_probability']
            
            model = RandomForestRegressor(n_estimators=10, random_state=42)
            model.fit(X, y)
            joblib.dump(model, MODEL_FILE)
            
            model_info = {
                'features': list(X.columns),
                'importances': {c: float(imp) for c, imp in zip(X.columns, model.feature_importances_)}
            }
            with open(INFO_FILE, 'w') as f:
                json.dump(model_info, f)

    return joblib.load(MODEL_FILE), json.load(open(INFO_FILE))

# Global model and info
try:
    model, model_info = load_or_train_model()
except Exception as e:
    print(f"Gagal memuat model pada startup: {e}")
    model, model_info = None, None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    global model, model_info
    if model is None:
        try:
            model, model_info = load_or_train_model()
        except Exception as e:
            return jsonify({"error": f"Model tidak dapat dimuat dan pelatihan gagal: {str(e)}"}), 500

    try:
        data = request.get_json(force=True)
        
        # Extract features
        nutrient_runoff = float(data.get('nutrient_runoff', 0))
        co2_emissions = float(data.get('co2_emissions', 400))
        water_temp = float(data.get('water_temp', 25))
        industrial_waste = float(data.get('industrial_waste', 0))
        
        # Predict
        features = [[nutrient_runoff, co2_emissions, water_temp, industrial_waste]]
        risk_probability = float(model.predict(features)[0])
        risk_probability = max(0.0, min(100.0, risk_probability))
        
        # Status classification
        if risk_probability < 35.0:
            status = "Rendah (Low)"
        elif risk_probability < 70.0:
            status = "Sedang (Medium)"
        else:
            status = "Kritis (Critical)"
            
        return jsonify({
            "risk_probability": round(risk_probability, 2),
            "status": status,
            "feature_importances": model_info.get('importances', {
                "co2_emissions": 0.40,
                "nutrient_runoff": 0.25,
                "water_temp": 0.20,
                "industrial_waste": 0.15
            })
        })
    except Exception as e:
        return jsonify({"error": f"Prediksi gagal: {str(e)}"}), 400

if __name__ == '__main__':
    # Run server on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
