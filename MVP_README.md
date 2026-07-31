# 🛡️ Phishing Detection MVP

A simplified **Minimum Viable Product** version of the phishing detection system with a clean, user-friendly interface.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r mvp_requirements.txt
```

### 2. Train the Model
```bash
python mvp_train.py
```

### 3. Run the Application
```bash
python mvp_app.py
```

### 4. Open in Browser
Visit: `http://localhost:5001`

## ✨ MVP Features

### 🎯 **Simplified Analysis**
- **10 Key Features** (reduced from 30 for easier use)
- **User-friendly questions** with helpful explanations
- **Visual progress indicators** and interactive forms

### 🧠 **AI-Powered Detection**
- **Random Forest Classifier** with 96.7% accuracy
- **Real-time predictions** with confidence scores
- **Risk factor identification** and safety recommendations

### 🎨 **Clean Interface**
- **Modern, responsive design** that works on all devices
- **Interactive elements** with hover effects and animations
- **Progress tracking** and visual feedback

### 📊 **Detailed Results**
- **Clear verdict**: Phishing or Legitimate
- **Confidence percentages** for both outcomes
- **Risk factor breakdown** with explanations
- **Safety recommendations** when threats are detected

## 🔧 Technical Details

### **Architecture**
- **Backend**: Flask web framework
- **Frontend**: HTML5 + CSS3 + JavaScript
- **ML Model**: Random Forest (50 trees, max depth 10)
- **Features**: 10 most important security characteristics

### **Key Features Analyzed**
1. **URL IP Address Usage** - Legitimate sites use domain names
2. **URL Length** - Suspicious sites often use very long URLs
3. **SSL Certificate Status** - Security certificate validation
4. **Domain Registration Length** - Legitimate sites register longer term
5. **Domain Age** - Newer domains are more suspicious
6. **HTTPS Token Misuse** - Fake HTTPS in URL paths
7. **Anchor URL Analysis** - External link detection
8. **URL Structure** - Abnormal URL patterns
9. **Google Indexing** - Search engine recognition
10. **Security Reports** - Known phishing database checks

### **Model Performance**
- **Overall Accuracy**: 96.7%
- **Phishing Detection**: 96.1%
- **Legitimate Recognition**: 97.5%
- **Training Samples**: 11,056 websites

## 📁 File Structure

```
mvp_files/
├── mvp_app.py              # Main Flask application
├── mvp_train.py            # Model training script
├── mvp_requirements.txt    # Dependencies
├── mvp_templates/          # HTML templates
│   ├── base.html          # Base template with styling
│   ├── home.html          # Main analysis form
│   ├── result.html        # Results display
│   └── about.html         # About page
├── mvp_models/            # Trained models (created after training)
│   ├── phishing_mvp_model.pkl
│   └── mvp_features.pkl
└── MVP_README.md          # This file
```

## 🎮 Usage Guide

### **Step 1: Answer Questions**
The interface presents 10 simple questions about the website you want to check. Each question has three options:
- 🔴 **Suspicious** (Red) - Indicates risky characteristics
- 🟡 **Uncertain** (Yellow) - Mixed or unclear indicators  
- 🟢 **Safe** (Green) - Indicates legitimate characteristics

### **Step 2: Get Analysis**
Click "Analyze Website Security" to get:
- **Clear verdict** (Phishing/Legitimate)
- **Confidence scores** showing certainty levels
- **Risk factors** that influenced the decision
- **Safety recommendations** if needed

### **Step 3: Review Details**
The results page shows:
- **Visual confidence indicators** with animated progress bars
- **Detailed breakdown** of each analyzed feature
- **Printable report** for documentation
- **Risk mitigation advice** for suspicious sites

## 🔗 API Usage

The MVP also includes a JSON API endpoint:

```bash
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "having_IP_Address": -1,
    "URL_Length": 1,
    "SSLfinal_State": 1,
    "Domain_registeration_length": 1,
    "age_of_domain": 1,
    "HTTPS_token": 1,
    "URL_of_Anchor": 1,
    "Abnormal_URL": 1,
    "Google_Index": 1,
    "Statistical_report": 1
  }'
```

## ⚠️ Important Notes

### **MVP Limitations**
- **Simplified feature set** (10 vs 30 features)
- **Basic UI** (no advanced visualizations like SHAP)
- **No user accounts** or history tracking
- **Single model** (no model comparison)

### **Security Disclaimer**
- Use as a **guide only**, not definitive security assessment
- **Verify through official channels** when in doubt
- **Exercise caution** with any suspicious websites
- **No system is 100% accurate** - trust your instincts

## 🛠️ Development

### **Adding Features**
To extend the MVP:
1. **Add new features** to `mvp_features` list in `mvp_train.py`
2. **Update descriptions** in `FEATURE_DESCRIPTIONS` in `mvp_app.py`
3. **Retrain the model** with `python mvp_train.py`
4. **Update templates** if needed

### **Customizing UI**
- **Styles** are embedded in `base.html` for simplicity
- **Colors and fonts** can be easily modified
- **Responsive design** works on mobile and desktop

### **Performance Tuning**
- **Adjust model parameters** in `mvp_train.py`
- **Change feature selection** for different accuracy/speed tradeoffs
- **Optimize for specific use cases**

## 🎉 Success!

Your MVP is now ready! This simplified version provides all the core functionality needed to:
- ✅ **Detect phishing websites** with high accuracy
- ✅ **Provide user-friendly interface** for non-technical users
- ✅ **Offer detailed explanations** of security assessments
- ✅ **Scale for production use** with minimal resources

Perfect for demonstrations, testing, or as a foundation for more advanced features!
