# XGBoost Price Prediction API

## Setup

1. Install required packages:
```bash
pip install flask joblib pandas xgboost scikit-learn
```

2. Make sure `model.pkl` exists in the AI folder

3. Run the Flask app:
```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### GET /
Health check endpoint
- Returns: "XGBoost Price Prediction API - Running Successfully!"

### POST /predict
Predict house prices based on features

## Postman Request Format

**URL:** `http://localhost:5000/predict`

**Method:** POST

**Headers:**
- Content-Type: application/json

**Body (raw JSON):**
```json
[
  {
    "Type": "Apartment",
    "Bedrooms": 3.0,
    "Bathrooms": 2.0,
    "Area": 165.0,
    "Furnished": "No",
    "Level": "1",
    "Compound": "Unknown",
    "Payment_Option": "Cash",
    "Delivery_Date": "Ready to move",
    "Delivery_Term": "Finished",
    "City": "Nasr City"
  }
]
```

**Note:** The request body should be an array of objects, even for a single prediction.

## Required Features

Based on the Egypt_Houses_Price.csv dataset, the model expects these features:

1. **Type** (string): Property type (e.g., "Apartment", "Duplex", "Villa")
2. **Bedrooms** (float): Number of bedrooms (e.g., 3.0)
3. **Bathrooms** (float): Number of bathrooms (e.g., 2.0)
4. **Area** (float): Property area in square meters (e.g., 165.0)
5. **Furnished** (string): Furnishing status ("Yes" or "No")
6. **Level** (string): Floor level (e.g., "1", "2", "10+", "Ground")
7. **Compound** (string): Compound name (e.g., "Unknown", "Eastown")
8. **Payment_Option** (string): Payment method (e.g., "Cash", "Installment")
9. **Delivery_Date** (string): Delivery date (e.g., "Ready to move", "2024")
10. **Delivery_Term** (string): Delivery term (e.g., "Finished", "Semi Finished")
11. **City** (string): City name (e.g., "Nasr City", "New Cairo")

## Example Response

**Success:**
```json
{
  "success": true,
  "prediction": [2250000.0]
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error message here"
}
```

## Multiple Predictions

You can predict multiple properties at once:

```json
[
  {
    "Type": "Apartment",
    "Bedrooms": 3.0,
    "Bathrooms": 2.0,
    "Area": 165.0,
    "Furnished": "No",
    "Level": "1",
    "Compound": "Unknown",
    "Payment_Option": "Cash",
    "Delivery_Date": "Ready to move",
    "Delivery_Term": "Finished",
    "City": "Nasr City"
  },
  {
    "Type": "Villa",
    "Bedrooms": 4.0,
    "Bathrooms": 3.0,
    "Area": 300.0,
    "Furnished": "Yes",
    "Level": "Ground",
    "Compound": "Palm Hills",
    "Payment_Option": "Installment",
    "Delivery_Date": "2024",
    "Delivery_Term": "Finished",
    "City": "New Cairo"
  }
]
```

Response:
```json
{
  "success": true,
  "prediction": [2250000.0, 5500000.0]
}
```
