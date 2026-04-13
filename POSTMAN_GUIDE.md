# Postman Testing Guide for XGBoost Price Prediction API

## Quick Start

1. **Start the API:**
   ```bash
   cd AI
   python app.py
   ```
   The API will run on `http://localhost:5000`

2. **Test in browser:**
   Open `http://localhost:5000` to see the API status page

## Postman Setup

### 1. Create New Request

- **Method:** POST
- **URL:** `http://localhost:5000/predict`

### 2. Set Headers

Click on "Headers" tab and add:
- **Key:** `Content-Type`
- **Value:** `application/json`

### 3. Set Body

Click on "Body" tab:
- Select **raw**
- Select **JSON** from dropdown
- Paste one of the examples below

---

## Example Requests

### Example 1: Single Apartment Prediction

```json
[
  {
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
  }
]
```

**Expected Response:**
```json
{
  "success": true,
  "predictions": [2250000.0],
  "count": 1
}
```

---

### Example 2: Luxury Villa

```json
[
  {
    "Type": "Standalone Villa",
    "Bedrooms": 5,
    "Bathrooms": 4,
    "Area": 450,
    "Furnished": "Yes",
    "Level": "Ground",
    "Compound": "Palm Hills New Cairo",
    "Payment_Option": "Cash",
    "Delivery_Date": "Ready to move",
    "Delivery_Term": "Finished",
    "City": "New Cairo - El Tagamoa"
  }
]
```

---

### Example 3: Budget Studio

```json
[
  {
    "Type": "Studio",
    "Bedrooms": 1,
    "Bathrooms": 1,
    "Area": 45,
    "Furnished": "No",
    "Level": "2",
    "Compound": "Unknown",
    "Payment_Option": "Installment",
    "Delivery_Date": "2024",
    "Delivery_Term": "Semi Finished",
    "City": "Shorouk City"
  }
]
```

---

### Example 4: Multiple Properties at Once

```json
[
  {
    "Type": "Apartment",
    "Bedrooms": 2,
    "Bathrooms": 1,
    "Area": 100,
    "Furnished": "No",
    "Level": "3",
    "Compound": "Unknown",
    "Payment_Option": "Cash",
    "Delivery_Date": "Ready to move",
    "Delivery_Term": "Finished",
    "City": "Nasr City"
  },
  {
    "Type": "Duplex",
    "Bedrooms": 4,
    "Bathrooms": 3,
    "Area": 300,
    "Furnished": "Yes",
    "Level": "Ground",
    "Compound": "Eastown",
    "Payment_Option": "Cash or Installment",
    "Delivery_Date": "Ready to move",
    "Delivery_Term": "Finished",
    "City": "New Cairo - El Tagamoa"
  },
  {
    "Type": "Penthouse",
    "Bedrooms": 3,
    "Bathrooms": 2,
    "Area": 200,
    "Furnished": "No",
    "Level": "10+",
    "Compound": "Maadi V",
    "Payment_Option": "Installment",
    "Delivery_Date": "2025",
    "Delivery_Term": "Core & Shell",
    "City": "Maadi"
  }
]
```

**Expected Response:**
```json
{
  "success": true,
  "predictions": [1500000.0, 4500000.0, 3200000.0],
  "count": 3
}
```

---

## Field Values Reference

### Type (Property Type)
- `Apartment`
- `Duplex`
- `Penthouse`
- `Studio`
- `Standalone Villa`
- `Twin house`
- `Town House`
- `Chalet`
- `Unknown`

### Bedrooms / Bathrooms
- Numbers: `1`, `2`, `3`, `4`, `5`, `6`, `7`, etc.
- Can use `Unknown` for missing data

### Area
- Number in square meters: `50`, `100`, `165`, `300`, `450`, etc.

### Furnished
- `Yes`
- `No`
- `Unknown`

### Level (Floor)
- Numbers: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`
- `Ground`
- `Highest`
- `10+`

### Compound (Community/Development)
- Any compound name or `Unknown`
- Examples: `Palm Hills`, `Eastown`, `Maadi V`, `90 Avenue`, etc.

### Payment_Option
- `Cash`
- `Installment`
- `Cash or Installment`
- `Unknown Payment`

### Delivery_Date
- `Ready to move`
- `2024`
- `2025`
- `2026`
- `2027`
- `soon`
- `within 6 months`
- `Unknown`

### Delivery_Term
- `Finished`
- `Semi Finished`
- `Core & Shell`
- `Not Finished`
- `Unknown`

### City
- `Nasr City`
- `New Cairo - El Tagamoa`
- `Sheikh Zayed`
- `Maadi`
- `New Capital City`
- `Shorouk City`
- `Camp Caesar`
- `Smoha`
- And many more Egyptian cities

---

## Common Errors

### Error: Missing columns
```json
{
  "success": false,
  "error": "Missing required columns: ['Area', 'City']",
  "required_columns": [...]
}
```
**Solution:** Make sure all 11 required fields are included

### Error: Invalid JSON
```json
{
  "success": false,
  "error": "No JSON data provided"
}
```
**Solution:** 
- Check that Content-Type header is set to `application/json`
- Verify JSON syntax is correct (use a JSON validator)

### Error: Connection refused
**Solution:** Make sure the Flask app is running (`python app.py`)

---

## Testing Tips

1. **Always use an array** `[]` even for single predictions
2. **Numbers can be integers or floats** - both work: `3` or `3.0`
3. **Test with unknown values** - the model handles `Unknown` gracefully
4. **Batch predictions** - send multiple properties to get multiple predictions at once
5. **Check the response** - `predictions` array matches the order of your input

---

## Integration Example (Python)

```python
import requests
import json

url = "http://localhost:5000/predict"
headers = {"Content-Type": "application/json"}

data = [
    {
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
    }
]

response = requests.post(url, headers=headers, json=data)
result = response.json()

if result['success']:
    print(f"Predicted Price: {result['predictions'][0]:,.0f} EGP")
else:
    print(f"Error: {result['error']}")
```

---

## Need Help?

- Check API status: `http://localhost:5000`
- View logs in the terminal where `app.py` is running
- Verify all preprocessing files exist: `model.pkl`, `label_encoders.pkl`, `scaler.pkl`, `feature_names.pkl`
