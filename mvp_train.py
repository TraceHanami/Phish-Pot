#!/usr/bin/env python3
"""
MVP Training Script - Simplified Phishing Detection Model
Creates a basic model using only the most important features for quick deployment
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import os

def create_mvp_model():
    """Create a simplified MVP model using only top features"""
    
    print("🚀 Starting MVP Model Training...")
    
    # Load dataset
    try:
        df = pd.read_csv("data/phishing.csv")
        print(f"✅ Dataset loaded: {len(df)} samples")
    except FileNotFoundError:
        print("❌ Error: data/phishing.csv not found!")
        return
    
    # Select top 10 most important features for MVP (based on domain knowledge)
    mvp_features = [
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
    
    # Prepare data
    X = df[mvp_features]
    y = df["Result"].map({-1: 1, 1: 0})  # Map -1(phishing) to 1, 1(legitimate) to 0
    
    print(f"📊 Using {len(mvp_features)} key features for MVP")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Create and train model
    model = RandomForestClassifier(
        n_estimators=50,  # Reduced for faster training
        max_depth=10,     # Simplified depth
        random_state=42
    )
    
    print("🎯 Training Random Forest model...")
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Model trained successfully!")
    print(f"📈 Accuracy: {accuracy:.2%}")
    
    # Create models directory
    os.makedirs("mvp_models", exist_ok=True)
    
    # Save model
    model_path = "mvp_models/phishing_mvp_model.pkl"
    joblib.dump(model, model_path)
    
    # Save feature names
    features_path = "mvp_models/mvp_features.pkl"
    joblib.dump(mvp_features, features_path)
    
    print(f"💾 Model saved to: {model_path}")
    print(f"💾 Features saved to: {features_path}")
    
    # Print detailed results
    print("\n📊 Detailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
    
    return model, mvp_features, accuracy

if __name__ == "__main__":
    model, features, accuracy = create_mvp_model()
    print(f"\n🎉 MVP Model Training Complete!")
    print(f"🎯 Final Accuracy: {accuracy:.2%}")
    print("🚀 Ready for deployment!")
