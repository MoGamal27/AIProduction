# 🚀 Deploy XGBoost API to PythonAnywhere

Complete guide to deploy your Flask API on PythonAnywhere for free.

---

## 📋 Prerequisites

1. Create a free account at [PythonAnywhere](https://www.pythonanywhere.com)
2. Have all your files ready:
   - `app.py`
   - `requirements.txt`
   - `model.pkl`
   - `label_encoders.pkl`
   - `scaler.pkl`
   - `feature_names.pkl`
   - `Egypt_Houses_Price.csv` (optional, for reference)

---

## 🔧 Step-by-Step Deployment

### Step 1: Sign Up & Login

1. Go to [PythonAnywhere](https://www.pythonanywhere.com)
2. Create a free "Beginner" account
3. Login to your dashboard

---

### Step 2: Upload Your Files

#### Option A: Using Git (Recommended)

1. Push your code to GitHub first
2. In PythonAnywhere, open a **Bash console**
3. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/yourrepo.git
   cd yourrepo/AI
   ```

#### Option B: Manual Upload

1. Go to **Files** tab in PythonAnywhere
2. Navigate to `/home/yourusername/`
3. Create a new directory: `mkdir myapi`
4. Click **Upload a file** and upload:
   - `app.py`
   - `requirements.txt`
   - `model.pkl`
   - `label_encoders.pkl`
   - `scaler.pkl`
   - `feature_names.pkl`

---

### Step 3: Install Dependencies

1. Open a **Bash console** from the dashboard
2. Navigate to your project folder:
   ```bash
   cd ~/myapi
   ```

3. Create a virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

4. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - Flask
   - joblib
   - pandas
   - numpy
   - scikit-learn
   - xgboost

5. Wait for installation to complete (may take 5-10 minutes)

---

### Step 4: Create WSGI Configuration

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10**
5. Click through the setup

---

### Step 5: Configure WSGI File

1. In the **Web** tab, find the **Code** section
2. Click on the WSGI configuration file link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete all existing content** and replace with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/myapi'  # ⚠️ CHANGE 'yourusername' to your actual username
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variable for Flask
os.chdir(project_home)

# Import Flask app
from app import app as application
```

4. **Important:** Replace `yourusername` with your actual PythonAnywhere username
5. Click **Save**

---

### Step 6: Set Virtual Environment Path

1. Still in the **Web** tab, find **Virtualenv** section
2. Enter the path to your virtual environment:
   ```
   /home/yourusername/myapi/venv
   ```
   (Replace `yourusername` with your actual username)
3. Click the checkmark to save

---

### Step 7: Reload Web App

1. Scroll to the top of the **Web** tab
2. Click the big green **Reload** button
3. Wait for the reload to complete

---

### Step 8: Test Your API

Your API is now live at:
```
https://yourusername.pythonanywhere.com
```

#### Test in Browser:
Visit: `https://yourusername.pythonanywhere.com`

You should see the API status page.

#### Test with Postman:

**URL:** `https://yourusername.pythonanywhere.com/predict`  
**Method:** POST  
**Headers:** `Content-Type: application/json`

**Body:**
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

---

## 🔍 Troubleshooting

### Error: "Something went wrong"

1. Check the **Error log** in the Web tab
2. Common issues:
   - Wrong path in WSGI file
   - Virtual environment not set correctly
   - Missing .pkl files

### Error: "ModuleNotFoundError"

1. Open a Bash console
2. Activate virtual environment:
   ```bash
   cd ~/myapi
   source venv/bin/activate
   ```
3. Install missing package:
   ```bash
   pip install package-name
   ```
4. Reload web app

### Error: "FileNotFoundError: model.pkl"

1. Check files are in the correct directory:
   ```bash
   cd ~/myapi
   ls -la
   ```
2. You should see:
   - app.py
   - model.pkl
   - label_encoders.pkl
   - scaler.pkl
   - feature_names.pkl

### Large File Upload Issues

If `.pkl` files are too large (>100MB on free tier):

1. Use Git LFS (Large File Storage)
2. Or compress files:
   ```bash
   gzip model.pkl
   ```
3. Update app.py to decompress on load

---

## 📊 Free Tier Limitations

PythonAnywhere free tier includes:
- ✅ 512MB disk space
- ✅ 1 web app
- ✅ HTTPS enabled
- ✅ Daily CPU quota
- ⚠️ Whitelisted sites only for external API calls
- ⚠️ App sleeps after inactivity (wakes on request)

---

## 🔒 Security Best Practices

### 1. Add API Key Authentication (Optional)

Update `app.py`:

```python
from flask import request, jsonify
import os

API_KEY = os.environ.get('API_KEY', 'your-secret-key')

@app.before_request
def check_api_key():
    if request.endpoint == 'predict':
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401
```

Set environment variable in PythonAnywhere:
1. Go to **Web** tab
2. Find **Environment variables** section
3. Add: `API_KEY` = `your-secret-key-here`

### 2. Rate Limiting

Install Flask-Limiter:
```bash
pip install Flask-Limiter
```

Update `app.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/predict', methods=['POST'])
@limiter.limit("10 per minute")
def predict():
    # ... your code
```

---

## 📝 Updating Your Deployment

When you make changes:

1. **Update files** (via Git or manual upload)
2. **Reload web app** from Web tab
3. If you changed requirements:
   ```bash
   cd ~/myapi
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Reload web app again

---

## 🎯 Production Checklist

Before going live:

- [ ] Test all endpoints thoroughly
- [ ] Check error logs are clean
- [ ] Verify all .pkl files are uploaded
- [ ] Test with various input data
- [ ] Set up monitoring/logging
- [ ] Document API for users
- [ ] Consider adding authentication
- [ ] Set up rate limiting
- [ ] Test error handling

---

## 📞 Support

- **PythonAnywhere Help:** https://help.pythonanywhere.com
- **Forums:** https://www.pythonanywhere.com/forums/
- **Documentation:** https://help.pythonanywhere.com/pages/Flask/

---

## 🚀 Alternative Deployment Options

If PythonAnywhere doesn't meet your needs:

1. **Heroku** - Easy deployment, free tier available
2. **Railway** - Modern platform, generous free tier
3. **Render** - Simple deployment, free tier
4. **AWS EC2** - More control, requires setup
5. **Google Cloud Run** - Serverless, pay per use
6. **Azure App Service** - Enterprise option

---

## 📋 Quick Reference

### Your API URLs:
- **Home:** `https://yourusername.pythonanywhere.com`
- **Predict:** `https://yourusername.pythonanywhere.com/predict`

### Important Paths:
- **Project:** `/home/yourusername/myapi`
- **Venv:** `/home/yourusername/myapi/venv`
- **WSGI:** `/var/www/yourusername_pythonanywhere_com_wsgi.py`
- **Logs:** Check Web tab → Error log

### Useful Commands:
```bash
# Activate virtual environment
source ~/myapi/venv/bin/activate

# Check installed packages
pip list

# View files
ls -la ~/myapi

# Test app locally
cd ~/myapi
python app.py
```

---

## ✅ Success!

Your XGBoost Price Prediction API is now live and accessible worldwide! 🎉

Share your API URL with others:
```
https://yourusername.pythonanywhere.com/predict
```

Happy predicting! 🏠💰
