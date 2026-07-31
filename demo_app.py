#!/usr/bin/env python3
"""
Demo Flask Application - Simplified Phishing Detection Interface
Demonstrates the UI and functionality without requiring ML dependencies
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import random
from datetime import datetime

app = Flask(__name__, template_folder='mvp_templates', static_folder='mvp_static')
app.secret_key = 'demo_secret_key_2024'

# Demo features (same as MVP but without actual ML)
DEMO_FEATURES = [
    'having_IP_Address',
    'URL_Length', 
    'SSLfinal_State',
    'Domain_registeration_length',
    'age_of_domain',
    'HTTPS_token',
    'URL_of_Anchor',
    'Abnormal_URL',
    'Google_Index',
    'Statistical_report'
]

# Feature descriptions (same as MVP)
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

def demo_predict(input_data):
    """
    Demo prediction function that simulates ML model behavior
    Based on simple heuristics for demonstration purposes
    """
    
    # Calculate risk score based on suspicious features
    suspicious_count = sum(1 for value in input_data.values() if value == -1)
    safe_count = sum(1 for value in input_data.values() if value == 1)
    
    # Simple scoring algorithm
    risk_score = (suspicious_count * 10) - (safe_count * 5)
    
    # Determine prediction based on risk score
    if risk_score > 15:
        # High risk - likely phishing
        prediction = 1
        phishing_prob = min(85 + random.randint(0, 10), 95)
        legitimate_prob = 100 - phishing_prob
    elif risk_score < -10:
        # Low risk - likely legitimate
        prediction = 0
        legitimate_prob = min(80 + random.randint(0, 15), 95)
        phishing_prob = 100 - legitimate_prob
    else:
        # Medium risk - could go either way, slight bias toward caution
        if suspicious_count > safe_count:
            prediction = 1
            phishing_prob = 60 + random.randint(0, 20)
            legitimate_prob = 100 - phishing_prob
        else:
            prediction = 0
            legitimate_prob = 60 + random.randint(0, 20)
            phishing_prob = 100 - legitimate_prob
    
    return prediction, phishing_prob, legitimate_prob

@app.route('/')
def home():
    """Home page with demo interface"""
    return render_template('home.html', features=DEMO_FEATURES, descriptions=FEATURE_DESCRIPTIONS)

@app.route('/predict', methods=['POST'])
def predict():
    """Make demo prediction based on user input"""
    try:
        # Get input data
        input_data = {}
        for feature in DEMO_FEATURES:
            value = request.form.get(feature)
            if value is None:
                flash(f"⚠️ Missing value for: {feature}", "warning")
                return redirect(url_for('home'))
            input_data[feature] = int(value)
        
        # Make demo prediction
        prediction, phishing_prob, legitimate_prob = demo_predict(input_data)
        
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
    """About page explaining the demo"""
    return render_template('about.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """JSON API endpoint for demo predictions"""
    try:
        data = request.json
        
        # Convert to our expected format
        input_data = {feature: data.get(feature, 0) for feature in DEMO_FEATURES}
        
        prediction, phishing_prob, legitimate_prob = demo_predict(input_data)
        
        return jsonify({
            'prediction': int(prediction),
            'result': 'phishing' if prediction == 1 else 'legitimate',
            'phishing_probability': phishing_prob / 100.0,
            'legitimate_probability': legitimate_prob / 100.0,
            'confidence': max(phishing_prob, legitimate_prob) / 100.0,
            'timestamp': datetime.now().isoformat(),
            'note': 'This is a demo version using simulated predictions'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("🚀 Starting Demo Phishing Detection App...")
    print("✅ Demo mode - using simulated AI predictions")
    print("🌐 Open http://localhost:5001 in your browser")
    print("📝 This demonstrates the UI and functionality without requiring ML dependencies")
    
    # Run the app
    app.run(host='127.0.0.1', port=5001, debug=True)
