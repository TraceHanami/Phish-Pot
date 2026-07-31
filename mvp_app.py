#!/usr/bin/env python3
"""
MVP Flask Application - Simple Phishing Detection Interface
Simplified version with essential functionality and basic UI
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime

app = Flask(__name__, template_folder='mvp_templates', static_folder='mvp_static')
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Global variables for model and features
model = None
features = None

def load_mvp_model():
    """Load the trained MVP model and features"""
    global model, features
    
    try:
        model = joblib.load("mvp_models/phishing_mvp_model.pkl")
        features = joblib.load("mvp_models/mvp_features.pkl")
        print("✅ MVP Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

# Feature descriptions for better user understanding
FEATURE_DESCRIPTIONS = {
    'having_IP_Address': {
        'question': 'Does the URL use an IP address instead of domain name?',
        'help': 'Legitimate websites typically use domain names, not IP addresses',
        'options': {-1: 'Yes (Suspicious)', 0: 'Unknown', 1: 'No (Normal)'}
    },
    'URL_Length': {
        'question': 'How long is the URL?',
        'help': 'Very long URLs are often used to hide malicious content',
        'options': {-1: 'Very Long (>75 chars)', 0: 'Medium (54-75 chars)', 1: 'Short (<54 chars)'}
    },
    'SSLfinal_State': {
        'question': 'What is the SSL certificate status?',
        'help': 'SSL certificates ensure secure connections',
        'options': {-1: 'Invalid/Missing', 0: 'Untrusted', 1: 'Valid & Trusted'}
    },
    'Domain_registeration_length': {
        'question': 'How long is the domain registered for?',
        'help': 'Legitimate sites typically register domains for longer periods',
        'options': {-1: 'Short term (<1 year)', 0: 'Medium term', 1: 'Long term (>1 year)'}
    },
    'age_of_domain': {
        'question': 'How old is the domain?',
        'help': 'Newer domains are more likely to be suspicious',
        'options': {-1: 'Very new (<6 months)', 0: 'Medium age', 1: 'Old (>6 months)'}
    },
    'HTTPS_token': {
        'question': 'Does the URL improperly use HTTPS in the path?',
        'help': 'Phishing sites sometimes put "https" in URL path to trick users',
        'options': {-1: 'Yes (Suspicious)', 0: 'Unclear', 1: 'No (Normal)'}
    },
    'URL_of_Anchor': {
        'question': 'Do page links point to external suspicious URLs?',
        'help': 'Check if links on the page redirect to other suspicious sites',
        'options': {-1: 'Many external links', 0: 'Some external links', 1: 'Mostly internal links'}
    },
    'Abnormal_URL': {
        'question': 'Does the URL structure look abnormal?',
        'help': 'Compare URL with legitimate versions of the site',
        'options': {-1: 'Very abnormal', 0: 'Somewhat abnormal', 1: 'Normal structure'}
    },
    'Google_Index': {
        'question': 'Is the website indexed by Google?',
        'help': 'Most legitimate websites are found in Google search results',
        'options': {-1: 'Not indexed', 0: 'Partially indexed', 1: 'Fully indexed'}
    },
    'Statistical_report': {
        'question': 'Is the website reported in phishing databases?',
        'help': 'Check if the site appears in known phishing/malware reports',
        'options': {-1: 'Reported as malicious', 0: 'Unknown/Mixed reports', 1: 'Clean reputation'}
    }
}

@app.route('/')
def home():
    """Home page with simple interface"""
    if model is None:
        if not load_mvp_model():
            flash("⚠️ Model not loaded. Please train the model first by running 'python mvp_train.py'", "warning")
    
    return render_template('home.html', features=features, descriptions=FEATURE_DESCRIPTIONS)

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction based on user input"""
    if model is None:
        flash("❌ Model not available. Please train the model first.", "error")
        return redirect(url_for('home'))
    
    try:
        # Get input data
        input_data = {}
        for feature in features:
            value = request.form.get(feature)
            if value is None:
                flash(f"⚠️ Missing value for: {feature}", "warning")
                return redirect(url_for('home'))
            input_data[feature] = int(value)
        
        # Create DataFrame for prediction
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        # Get confidence scores
        phishing_prob = probability[1] * 100  # Probability of being phishing
        legitimate_prob = probability[0] * 100  # Probability of being legitimate
        
        # Determine result
        result = "🚨 PHISHING DETECTED" if prediction == 1 else "✅ LIKELY LEGITIMATE"
        confidence = max(phishing_prob, legitimate_prob)
        
        # Get risk factors (features contributing to phishing classification)
        risk_factors = []
        for feature, value in input_data.items():
            if value == -1:  # Suspicious values
                risk_factors.append(FEATURE_DESCRIPTIONS[feature]['question'])
        
        return render_template('result.html', 
                             result=result,
                             prediction=prediction,
                             phishing_prob=phishing_prob,
                             legitimate_prob=legitimate_prob,
                             confidence=confidence,
                             risk_factors=risk_factors,
                             input_data=input_data,
                             descriptions=FEATURE_DESCRIPTIONS,
                             timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
    except Exception as e:
        flash(f"❌ Prediction error: {str(e)}", "error")
        return redirect(url_for('home'))

@app.route('/about')
def about():
    """About page explaining the MVP"""
    return render_template('about.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """JSON API endpoint for predictions"""
    if model is None:
        return jsonify({'error': 'Model not available'}), 500
    
    try:
        data = request.json
        input_df = pd.DataFrame([data])
        
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        return jsonify({
            'prediction': int(prediction),
            'result': 'phishing' if prediction == 1 else 'legitimate',
            'phishing_probability': float(probability[1]),
            'legitimate_probability': float(probability[0]),
            'confidence': float(max(probability)),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("🚀 Starting MVP Phishing Detection App...")
    
    # Load model on startup
    if load_mvp_model():
        print("✅ Ready to serve predictions!")
    else:
        print("⚠️ Starting without model. Train first with 'python mvp_train.py'")
    
    # Run the app
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(host=host, port=5001, debug=debug)
