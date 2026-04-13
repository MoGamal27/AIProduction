from flask import Flask, request, jsonify
import joblib
import pandas as pd
import pickle
import os
import numpy as np

# Load the XGBoost model
print("Loading model...")
with open('model.pkl', 'rb') as f:
    model = joblib.load(f)
print(f"✓ Model loaded. Expects {model.n_features_in_} features")

# Load label encoders
print("Loading label encoders...")
if os.path.exists('label_encoders.pkl'):
    with open('label_encoders.pkl', 'rb') as f:
        label_encoders_raw = pickle.load(f)
    # Clean BOM characters from encoder keys
    label_encoders = {}
    for key, value in label_encoders_raw.items():
        clean_key = key.replace('ï»¿', '')
        label_encoders[clean_key] = value
    print(f"✓ Loaded label encoders for: {list(label_encoders.keys())}")
elif os.path.exists('encoders.pkl'):
    with open('encoders.pkl', 'rb') as f:
        label_encoders_raw = pickle.load(f)
    # Clean BOM characters from encoder keys
    label_encoders = {}
    for key, value in label_encoders_raw.items():
        clean_key = key.replace('ï»¿', '')
        label_encoders[clean_key] = value
    print(f"✓ Loaded encoders for: {list(label_encoders.keys())}")
else:
    print("✗ WARNING: No encoders found!")
    label_encoders = {}

# Load scaler
print("Loading scaler...")
if os.path.exists('scaler.pkl'):
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print(f"✓ Scaler loaded. Expects {scaler.n_features_in_} features")
else:
    print("✗ WARNING: No scaler.pkl found. Predictions will be incorrect!")
    scaler = None

# Load feature names if available
if os.path.exists('feature_names.pkl'):
    with open('feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    # Keep original feature names (with BOM) for scaler compatibility
    # But also create clean version for display
    feature_names_clean = [col.replace('ï»¿', '') for col in feature_names]
    print(f"✓ Feature names loaded: {feature_names_clean}")
else:
    feature_names = None
    feature_names_clean = None
    print("✗ No feature_names.pkl found")

# Create a Flask app
app = Flask(__name__)

# Expected input columns (what user sends)
INPUT_COLUMNS = ['Type', 'Bedrooms', 'Bathrooms', 'Area', 'Furnished', 
                 'Level', 'Compound', 'Payment_Option', 'Delivery_Date', 
                 'Delivery_Term', 'City']

def clean_numeric(x):
    """Clean numeric values"""
    if pd.isna(x) or x == 'Unknown':
        return np.nan
    try:
        return float(str(x).replace('+', '').replace(',', ''))
    except:
        return np.nan

def clean_categorical(x):
    """Clean categorical values"""
    if pd.isna(x) or str(x).strip() == '' or str(x) == 'Unknown':
        return 'Unknown'
    return str(x).strip()

def preprocess_data(data):
    """
    Apply the same preprocessing as in training:
    1. Clean numeric columns
    2. Clean categorical columns
    3. Feature engineering (create new features)
    4. Encode categorical columns
    5. Scale all features
    """
    # Make a copy to avoid modifying original
    df = data.copy()
    
    # DON'T clean column names yet - keep them as is for now
    
    # Clean numeric columns
    for col in ['Bedrooms', 'Bathrooms', 'Area']:
        if col in df.columns:
            df[col] = df[col].apply(clean_numeric)
            # Fill missing with median (ideally use training median)
            df[col].fillna(df[col].median(), inplace=True)
    
    # Clean categorical columns
    categorical_cols = ['Type', 'Furnished', 'Level', 'Compound', 
                       'Payment_Option', 'Delivery_Date', 'Delivery_Term', 'City']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_categorical)
    
    # ── FEATURE ENGINEERING (same as training) ────────────────────────────
    # These 3 features were created during training!
    df['Total_Rooms'] = df['Bedrooms'] + df['Bathrooms']
    df['Price_per_Area'] = 0  # Placeholder since we don't have Price during prediction
    df['Area_per_Room'] = df['Area'] / df['Total_Rooms']
    
    # Replace inf and -inf with 0
    df.replace([np.inf, -np.inf], 0, inplace=True)
    
    # Encode categorical columns
    for col in categorical_cols:
        if col in df.columns and col in label_encoders:
            # Handle unseen categories
            def safe_transform(x):
                if x in label_encoders[col].classes_:
                    return label_encoders[col].transform([x])[0]
                else:
                    # Return -1 for unseen categories (same as training)
                    return -1
            
            df[col] = df[col].apply(safe_transform)
    
    # NOW rename columns to match what scaler expects (with BOM if needed)
    if feature_names:
        # Create a mapping from clean names to original names with BOM
        original_feature_names = []
        with open('feature_names.pkl', 'rb') as f:
            original_feature_names = pickle.load(f)
        
        # Rename columns to match original feature names (with BOM)
        column_mapping = {}
        for orig_name in original_feature_names:
            clean_name = orig_name.replace('ï»¿', '')
            if clean_name in df.columns:
                column_mapping[clean_name] = orig_name
        
        df.rename(columns=column_mapping, inplace=True)
        
        # Reorder columns to match training
        df = df[original_feature_names]
    
    # Scale features
    if scaler is not None:
        df_scaled = scaler.transform(df)
        return df_scaled
    else:
        return df.values

@app.route('/')
def home():
    status_html = f"""
    <html>
    <head><title>XGBoost Price Prediction API</title></head>
    <body style="font-family: Arial, sans-serif; margin: 40px;">
        <h1>🏠 XGBoost Price Prediction API</h1>
        <p style="color: green; font-weight: bold;">✓ Status: Running Successfully!</p>
        
        <h2>Model Information:</h2>
        <ul>
            <li>Features expected: {model.n_features_in_}</li>
            <li>Encoders loaded: {len(label_encoders)}</li>
            <li>Scaler: {'✓ Loaded' if scaler else '✗ Not found'}</li>
            <li>Feature names: {'✓ Loaded' if feature_names else '✗ Not found'}</li>
        </ul>
        
        <h2>Usage:</h2>
        <p><strong>Endpoint:</strong> POST to <code>/predict</code></p>
        <p><strong>Required fields:</strong> {', '.join(INPUT_COLUMNS)}</p>
        
        <h3>Example Request:</h3>
        <pre style="background: #f4f4f4; padding: 15px; border-radius: 5px;">
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
    "Compound": "Unknown",
    "Payment_Option": "Cash",
    "Delivery_Date": "Ready to move",
    "Delivery_Term": "Finished",
    "City": "Nasr City"
  }}
]
        </pre>
    </body>
    </html>
    """
    return status_html

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Convert to DataFrame
        data = pd.DataFrame(json_data)
        
        # Check for required columns
        missing_cols = [col for col in INPUT_COLUMNS if col not in data.columns]
        if missing_cols:
            return jsonify({
                'success': False,
                'error': f'Missing required columns: {missing_cols}',
                'required_columns': INPUT_COLUMNS
            }), 400
        
        # Preprocess data (includes feature engineering, encoding, scaling)
        processed_data = preprocess_data(data)
        
        # Make prediction
        predictions = model.predict(processed_data)
        
        return jsonify({
            'success': True,
            'predictions': predictions.tolist(),
            'count': len(predictions)
        })
    
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 400

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Flask API on http://localhost:5000")
    print("="*60)
    print(f"Model ready with {model.n_features_in_} features")
    print(f"Send POST requests to http://localhost:5000/predict")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
