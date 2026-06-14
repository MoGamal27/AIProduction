from flask import Flask, request, jsonify
import joblib
import pandas as pd
import json
import os
import numpy as np

# ── Load model ────────────────────────────────────────────────────────────────
print("Loading model...")
model = joblib.load('model.pkl')
print(f"✓ Model loaded. Expects {model.n_features_in_} features")

# ── Load scaler ───────────────────────────────────────────────────────────────
print("Loading scaler...")
scaler = joblib.load('scaler.pkl')
print(f"✓ Scaler loaded. Expects {scaler.n_features_in_} features")

# ── Load encoding maps ────────────────────────────────────────────────────────
print("Loading label encoders...")
with open('label_encoder.json', 'r', encoding='utf-8') as f:
    label_encoder = json.load(f)
print(f"✓ Encoders loaded for: {list(label_encoder.keys())}")

# ── Load feature order ────────────────────────────────────────────────────────
print("Loading feature names...")
with open('feature_names.json', 'r') as f:
    feature_names = json.load(f)
print(f"✓ Feature names: {feature_names}")

# ── Flask app ─────────────────────────────────────────────────────────────────
app = Flask(__name__)

# Fields the user must send
INPUT_COLUMNS = ['Type', 'Bedrooms', 'Bathrooms', 'Area',
                 'Furnished', 'Level', 'Payment_Option', 'Delivery_Term', 'City']

# ── Level normalisation (mirrors training logic) ───────────────────────────────
LEVEL_MAP = {'Ground': 0, '10+': 11, 'Highest': 12}

def normalise_level(val):
    """Convert Level string/int to the int used during training."""
    if pd.isna(val):
        return 1  # sensible default
    s = str(val).strip()
    if s in LEVEL_MAP:
        return LEVEL_MAP[s]
    try:
        return int(float(s))
    except ValueError:
        return 1  # fallback for unexpected strings


def preprocess(data: pd.DataFrame) -> np.ndarray:
    """
    Apply exactly the same transformations used during training:
      1. Numeric cleaning
      2. Level normalisation
      3. Categorical map-encoding (Type, Furnished, Payment_Option, Delivery_Term, City)
      4. Column reordering to match training feature order
      5. StandardScaler transform
    """
    df = data.copy()

    # ── 1. Numeric columns ────────────────────────────────────────────────────
    for col in ['Bedrooms', 'Bathrooms', 'Area']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].isna().any():
            df[col].fillna(df[col].median(), inplace=True)

    # ── 2. Level ─────────────────────────────────────────────────────────────
    df['Level'] = df['Level'].apply(normalise_level).astype(int)

    # ── 3. Map-encode categoricals ────────────────────────────────────────────
    map_cols = ['Type', 'Furnished', 'Payment_Option', 'Delivery_Term', 'City']
    for col in map_cols:
        mapping = label_encoder.get(col, {})
        unknown_default = -1  # unseen value → -1, consistent with training guard

        def encode(x, m=mapping):
            v = str(x).strip()
            return m.get(v, unknown_default)

        df[col] = df[col].apply(encode)

    # ── 4. Reorder to training column order ───────────────────────────────────
    df = df[feature_names]

    # ── 5. Scale ─────────────────────────────────────────────────────────────
    return scaler.transform(df)


@app.route('/')
def home():
    html = f"""
    <html>
    <head><title>Egypt House Price Prediction API</title></head>
    <body style="font-family: Arial, sans-serif; margin: 40px;">
        <h1>🏠 Egypt House Price Prediction API</h1>
        <p style="color: green; font-weight: bold;">✓ Status: Running</p>

        <h2>Model Info</h2>
        <ul>
            <li>Features expected: {model.n_features_in_}</li>
            <li>Feature order: {feature_names}</li>
            <li>Encoders loaded for: {list(label_encoder.keys())}</li>
        </ul>

        <h2>Endpoint</h2>
        <p><strong>POST</strong> <code>/predict</code> — Content-Type: application/json</p>
        <p>Send a JSON array of property objects. Each object must contain:</p>
        <pre style="background:#f4f4f4; padding:15px; border-radius:5px;">{json.dumps(INPUT_COLUMNS, indent=2)}</pre>

        <h3>Example Request</h3>
        <pre style="background:#f4f4f4; padding:15px; border-radius:5px;">
POST /predict
Content-Type: application/json

[
  {{
    "Type": "Apartment",
    "Bedrooms": 3,
    "Bathrooms": 2,
    "Area": 165,
    "Furnished": "No",
    "Level": "1",
    "Payment_Option": "Cash",
    "Delivery_Term": "Finished",
    "City": "Nasr City"
  }}
]
        </pre>

        <h3>Valid Values</h3>
        <ul>
            <li><strong>Type:</strong> Studio, Apartment, Duplex, Penthouse</li>
            <li><strong>Furnished:</strong> Yes, No</li>
            <li><strong>Level:</strong> Ground, 1–9, 10+, Highest (or integer)</li>
            <li><strong>Payment_Option:</strong> Cash, Installment, Cash or Installment</li>
            <li><strong>Delivery_Term:</strong> Core &amp; Shell, Not Finished, Semi Finished, Finished</li>
            <li><strong>City:</strong> see label_encoder.json for full list</li>
        </ul>
    </body>
    </html>
    """
    return html


@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()

        if not json_data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        # Accept both a single object and a list
        if isinstance(json_data, dict):
            json_data = [json_data]

        data = pd.DataFrame(json_data)

        # Validate required columns
        missing = [c for c in INPUT_COLUMNS if c not in data.columns]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing required columns: {missing}',
                'required_columns': INPUT_COLUMNS
            }), 400

        processed = preprocess(data)
        predictions = model.predict(processed)

        return jsonify({
            'success': True,
            'predictions': [round(float(p), 2) for p in predictions],
            'count': len(predictions)
        })

    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting Flask API on http://localhost:5000")
    print(f"   Model ready — {model.n_features_in_} features")
    print(f"   Features: {feature_names}")
    print("=" * 60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
