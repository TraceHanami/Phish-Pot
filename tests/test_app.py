import unittest
import json
import os
import pandas as pd
import joblib
from app import app as flask_app
from mvp_app import app as mvp_app, load_mvp_model

class TestPhishingDetector(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.flask_client = flask_app.test_client()
        cls.mvp_client = mvp_app.test_client()
        flask_app.testing = True
        mvp_app.testing = True
        load_mvp_model()

    def test_model_label_mapping_logic(self):
        """Verify that safe feature inputs map to Legitimate and suspicious to Phishing"""
        model = joblib.load("models/phishing_model_rf.pkl")
        features = list(model.feature_names_in_)
        
        safe_input = pd.DataFrame([{f: 1 for f in features}])
        phish_input = pd.DataFrame([{f: -1 for f in features}])
        
        pred_safe = model.predict(safe_input)[0]
        pred_phish = model.predict(phish_input)[0]
        
        # In train_and_evaluate_all_models.py: -1 -> 0 (Phishing), 1 -> 1 (Legitimate)
        self.assertEqual(pred_safe, 1, "Safe inputs must yield prediction class 1 (Legitimate)")
        self.assertEqual(pred_phish, 0, "Suspicious inputs must yield prediction class 0 (Phishing)")

    def test_flask_home_route(self):
        """Test Flask home endpoint response"""
        response = self.flask_client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Flask API is running", response.data)

    def test_flask_form_route(self):
        """Test Flask input form rendering"""
        response = self.flask_client.get('/form')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Phishing Detection Form", response.data)

    def test_flask_predict_form(self):
        """Test Flask prediction submit endpoint with safe inputs"""
        form_data = {"model_choice": "rf"}
        model = joblib.load("models/phishing_model_rf.pkl")
        for feature in model.feature_names_in_:
            form_data[feature] = "1"
            
        response = self.flask_client.post('/predict_form', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Legitimate Website", response.data)

    def test_mvp_api_predict_endpoint(self):
        """Test MVP JSON API prediction endpoint"""
        payload = {
            "having_IP_Address": -1,
            "URL_Length": -1,
            "SSLfinal_State": -1,
            "Domain_registeration_length": -1,
            "age_of_domain": -1,
            "HTTPS_token": -1,
            "URL_of_Anchor": -1,
            "Abnormal_URL": -1,
            "Google_Index": -1,
            "Statistical_report": -1
        }
        response = self.mvp_client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result'], 'phishing')
        self.assertIn('phishing_probability', data)
        self.assertIn('confidence', data)

if __name__ == '__main__':
    unittest.main()
