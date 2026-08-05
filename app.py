
from flask import Flask, request, render_template
import markupsafe
import joblib
import pandas as pd
import numpy as np
import os
os.environ['MPLBACKEND'] = 'Agg'
import uuid
import io
import base64

app = Flask(__name__, template_folder='templates', static_folder='static')

models = {
    "xgb": joblib.load("models/phishing_model_xgb.pkl"),
    "lr": joblib.load("models/phishing_model_lr.pkl"),
    "best": joblib.load("models/phishing_model_best.pkl"),
    "rf": joblib.load("models/phishing_model_rf.pkl")
}
features = list(models["best"].feature_names_in_)

# Cache background dataset once for SHAP explainers to optimize performance
try:
    bg_data = pd.read_csv("data/phishing.csv")
    X_bg = bg_data[features]
except Exception as e:
    X_bg = None

feature_expl_dict = {
    "having_IP_Address": "the URL uses an IP address",
    "URL_Length": "the URL is unusually long",
    "Shortining_Service": "a URL shortening service is used",
    "having_At_Symbol": "the URL contains an '@' symbol",
    "double_slash_redirecting": "contains double slashes (//) beyond the protocol",
    "Prefix_Suffix": "a hyphen is used in the domain",
    "having_Sub_Domain": "contains multiple subdomains",
    "SSLfinal_State": "SSL certificate is invalid or missing",
    "Domain_registeration_length": "short domain registration duration",
    "Favicon": "favicon is from external domain",
    "port": "non-standard port is used",
    "HTTPS_token": "HTTPS token is present in the URL path",
    "Request_URL": "page loads external resources",
    "URL_of_Anchor": "anchors point to suspicious URLs",
    "Links_in_tags": "tags point to suspicious resources",
    "SFH": "Server Form Handler is abnormal",
    "Submitting_to_email": "form submits to an email address",
    "Abnormal_URL": "URL structure is abnormal",
    "Redirect": "page has multiple redirections",
    "on_mouseover": "content changes on hover",
    "RightClick": "right-click is disabled",
    "popUpWidnow": "pop-up windows are triggered",
    "Iframe": "uses invisible iframe tags",
    "age_of_domain": "domain is newly registered",
    "DNSRecord": "no DNS record found",
    "web_traffic": "low site traffic",
    "Page_Rank": "poor page rank",
    "Google_Index": "not indexed by Google",
    "Links_pointing_to_page": "few backlinks",
    "Statistical_report": "known in phishing reports"
}

@app.route('/')
def home():
    return render_template('form.html', features=features)

@app.route('/form')
def form():
    return render_template('form.html', features=features)

@app.route('/predict_form', methods=['POST'])
def predict_form():
    model_key = request.form.get("model_choice", "best")
    model = models.get(model_key, models["best"])

    input_data = {}
    for feature in features:
        raw_val = request.form.get(feature, 0)
        try:
            input_data[feature] = int(raw_val)
        except ValueError:
            input_data[feature] = 0

    input_df = pd.DataFrame([input_data])[features]

    raw_prediction = model.predict(input_df)[0]
    # Corrected label mapping: train_and_evaluate_all_models.py mapped -1 (Phishing) -> 0 and 1 (Legitimate) -> 1
    label = "Legitimate" if raw_prediction == 1 else "Phishing"

    plot_url = None
    explanation = ""

    if X_bg is not None:
        try:
            import shap
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            if model_key in ["xgb", "best", "rf"]:
                explainer = shap.Explainer(model, X_bg, algorithm="tree")
            else:
                explainer = shap.Explainer(model, X_bg, algorithm="linear")

            shap_values = explainer(input_df)

            if hasattr(shap_values, "values"):
                val = shap_values.values
                if val.ndim == 3:
                    shap_val_row = val[0, :, 1]
                else:
                    shap_val_row = val[0]
            else:
                shap_val_row = shap_values[0].values[0]

            sorted_idx = np.argsort(np.abs(shap_val_row))[::-1]
            top_indices = sorted_idx[:10]
            top_features = [str(features[i]) for i in top_indices]
            top_values = shap_val_row[top_indices]

            buf = io.BytesIO()
            plt.figure(figsize=(8, 6))
            plt.barh(top_features[::-1], top_values[::-1])
            plt.xlabel("SHAP value")
            plt.title("Top 10 SHAP Feature Influences")
            plt.tight_layout()
            plt.savefig(buf, format="png")
            plt.close()
            buf.seek(0)

            plot_url = f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"

            nle_features = [features[i] for i in sorted_idx[:3]]
            reasons = [feature_expl_dict.get(f, f.replace('_', ' ')) for f in nle_features]
            explanation = (
                f"The model classified this input as {label} primarily because "
                f"{', '.join(reasons[:-1])}, and {reasons[-1]}."
            )
        except Exception as e:
            print(f"SHAP explanation disabled: {e}")
            plot_url = None
            explanation = f"The model classified this input as {label}."

    return render_template(
        'result.html',
        prediction_label=label,
        plot_url=plot_url,
        explanation=explanation
    )

if __name__ == '__main__':
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(host=host, port=5000, debug=debug)

