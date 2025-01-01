from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from src.data_processing import load_and_clean_data
from src.model_training import train_and_evaluate
from src.monitoring import monitor_risk
from src.visualizations import generate_dashboard
import os
import logging

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_risk_monitoring.db'
app.config['UPLOAD_FOLDER'] = 'data/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Logging setup
logging.basicConfig(filename='logs/app.log', level=logging.INFO)

# Models
from models import Patient, User

# Database initialization
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash("No file selected.")
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("File uploaded successfully.")
        return redirect(url_for('train'))
    return render_template('upload.html')

@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        X, y = load_and_clean_data(os.path.join(app.config['UPLOAD_FOLDER'], 'Meddataset.csv'))
        train_and_evaluate(X, y, logging.getLogger(__name__))
        flash("Model trained successfully.")
        return redirect(url_for('home'))
    return render_template('train.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        form_data = [float(request.form[field]) for field in ['age', 'biomarker_a', 'biomarker_b', 'symptoms_severity']]
        risk_level, risk_prob = monitor_risk(form_data, 'models/risk_model.pkl')
        return render_template('predict.html', risk_level=risk_level, risk_prob=risk_prob)
    return render_template('predict.html')

@app.route('/dashboard')
@login_required
def dashboard():
    dashboard_html = generate_dashboard()
    return render_template('dashboard.html', dashboard_html=dashboard_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.json
    patient_data = [
        data.get('age'),
        data.get('biomarker_a'),
        data.get('biomarker_b'),
        data.get('symptoms_severity'),
    ]
    risk_level, risk_prob = monitor_risk(patient_data, 'models/risk_model.pkl')
    return jsonify({
        'risk_level': risk_level,
        'risk_probability': risk_prob
    })

if __name__ == "__main__":
    app.run(debug=True)
