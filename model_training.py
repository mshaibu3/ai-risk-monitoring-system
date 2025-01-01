from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_and_evaluate(X, y, logger):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    logger.info(f"Training completed. Accuracy: {model.score(X_train, y_train):.2f}")
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/risk_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
