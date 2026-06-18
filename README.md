# 🏠 Egypt House Price Prediction API

A machine learning REST API built with Flask that predicts property prices in Egypt based on key features like location, area, type, and finishing.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [API Usage](#api-usage)
- [Valid Input Values](#valid-input-values)
- [Project Structure](#project-structure)

---

## Project Overview

This project exposes a trained XGBoost regression model via a Flask API. Send property details as JSON and get back a predicted price in EGP.

The model was trained on the `House_Price_Egypt.csv` dataset and uses the following features:

| Feature | Description |
|---|---|
| `Type` | Property type (Apartment, Duplex, etc.) |
| `Bedrooms` | Number of bedrooms |
| `Bathrooms` | Number of bathrooms |
| `Area` | Area in m² |
| `Furnished` | Furnished or not |
| `Level` | Floor level |
| `Payment_Option` | Cash, Installment, or both |
| `Delivery_Term` | Finishing status |
| `City` | City in Egypt |

---

## Prerequisites

- Python **3.9** or higher
- `pip` package manager

---

## Installation

### 1. Clone or download the project

```bash
git clone <your-repo-url>
cd AIProduction
```

### 2. Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

| Package | Version |
|---|---|
| Flask | 3.0.0 |
| joblib | 1.3.2 |
| pandas | ≥ 2.2.0 |
| numpy | ≥ 1.26.0 |
| scikit-learn | ≥ 1.5.0 |
| xgboost | ≥ 2.1.0 |
| Werkzeug | 3.0.1 |

### 4. Verify required model files are present

Make sure these files exist in the project directory before starting:

```
model.pkl
scaler.pkl
label_encoder.json
feature_names.json
```

---

## Running the API

```bash
python app.py
```

You should see:

```
Loading model...
✓ Model loaded. Expects N features
Loading scaler...
✓ Scaler loaded.
Loading label encoders...
✓ Encoders loaded for: [...]
Loading feature names...
✓ Feature names: [...]

============================================================
🚀 Starting Flask API on http://localhost:5000
============================================================
```

Open your browser and go to `http://localhost:5000` to see the interactive API documentation page.

---

## API Usage

### Endpoint

```
POST /predict
Content-Type: application/json
```

### Request Body

Send a JSON array with one or more property objects:

```json
[
  {
    "Type": "Apartment",
    "Bedrooms": 3,
    "Bathrooms": 2,
    "Area": 165,
    "Furnished": "No",
    "Level": "1",
    "Payment_Option": "Cash",
    "Delivery_Term": "Finished",
    "City": "Nasr City"
  }
]
```

A single object (without the array) is also accepted.

### Example with `curl`

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d "[{\"Type\":\"Apartment\",\"Bedrooms\":3,\"Bathrooms\":2,\"Area\":165,\"Furnished\":\"No\",\"Level\":\"1\",\"Payment_Option\":\"Cash\",\"Delivery_Term\":\"Finished\",\"City\":\"Nasr City\"}]"
```

### Example with Python `requests`

```python
import requests

payload = [
    {
        "Type": "Apartment",
        "Bedrooms": 3,
        "Bathrooms": 2,
        "Area": 165,
        "Furnished": "No",
        "Level": "1",
        "Payment_Option": "Cash",
        "Delivery_Term": "Finished",
        "City": "Nasr City"
    }
]

response = requests.post("http://localhost:5000/predict", json=payload)
print(response.json())
```

### Response

```json
{
  "success": true,
  "predictions": [2450000.00],
  "count": 1
}
```

---

## Valid Input Values

| Field | Accepted Values |
|---|---|
| `Type` | `Studio`, `Apartment`, `Duplex`, `Penthouse` |
| `Furnished` | `Yes`, `No` |
| `Level` | `Ground`, `1` – `9`, `10+`, `Highest` (or any integer) |
| `Payment_Option` | `Cash`, `Installment`, `Cash or Installment` |
| `Delivery_Term` | `Core & Shell`, `Not Finished`, `Semi Finished`, `Finished` |
| `City` | See `label_encoder.json` for the full list of supported cities |

---

## Project Structure

```
AIProduction/
├── app.py                        # Flask API server
├── requirements.txt              # Python dependencies
├── model.pkl                     # Trained XGBoost model
├── scaler.pkl                    # Fitted StandardScaler
├── label_encoder.json            # Categorical encoding maps
├── feature_names.json            # Training feature order
├── training_columns.json         # Training column reference
├── House_Price_Egypt.csv         # Original dataset
├── Model_Project_Enhanced.ipynb  # Training & EDA notebook
└── *.png                         # EDA and evaluation plots
```
