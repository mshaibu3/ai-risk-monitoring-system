import joblib
import numpy as np

def monitor_risk(patient_data, model_file):
    model = joblib.load(model_file)
    scaler = joblib.load('models/scaler.pkl')
    patient_data_scaled = scaler.transform([patient_data])
    risk_prob = model.predict_proba(patient_data_scaled)[0][1]
    risk_level = "High" if risk_prob > 0.5 else "Low"
    return risk_level, risk_prob
