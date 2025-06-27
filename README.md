
# 📊 Data Visualization with Flask

A **Data Visualization** web application built using **Flask**, **Dash**, **Pandas**, **Matplotlib**, **SciPy**, **NumPy**, and more.

This project provides interactive dashboards and statistical visualizations for data analysis using modern Python web technologies.

---

## 🔧 Technologies Used

- **Flask** - Lightweight web framework
- **Dash** - Interactive data visualization dashboards
- **Pandas** - Data analysis and manipulation
- **Matplotlib**, **Seaborn**, **Plotly** - Data visualization libraries
- **NumPy**, **SciPy**, **Scikit-learn**, **Statsmodels** - Scientific computing & machine learning
- **Flask-SQLAlchemy**, **Flask-Migrate** - Database ORM & migrations
- **JupyterLab**, **IPython** - Development utilities

---

## 👨‍💻 Author

**ABDULLAH al numan**

---

## ⚙️ Setup Instructions (Windows)

### 1️⃣ Install Python (If not installed)

✅ Download Python from the official website:

➡️ [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

During installation, ensure **"Add Python to PATH"** is checked.

---

### 2️⃣ Add Python to Environment Variables (If missed during install)

- Open **Start Menu → Search: Environment Variables**
- Edit **System variables → Path**
- Add the path to Python and Scripts (Example):

```
C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python311\
C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python311\Scripts\
```

---

### 3️⃣ Clear Python Cache (If needed)

If you have a corrupted install or facing issues:

```powershell
py -m pip cache purge
```

Or manually delete the cache folder:

```
%LocalAppData%\pip\Cache
```

---

## 🏗️ Creating the Python Project

### 4️⃣ Project Directory Structure Example

```
NPY
├── app_modules
│   ├── __pycache__
│   ├── assets
│   │   ├── css
│   │   │   └── style.css
│   │   ├── data
│   │   │   └── cmdb_ci_computer.csv
│   │   ├── img
│   │   └── js
│   │       └── app.js
│   ├── ci_computer.ipynb
│   ├── ci_computer.py
│   ├── init_anotherApp.py
│   └── init_ilocApp.py
├── app_settings
│   ├── __pycache__
│   ├── static
│   │   └── css
│   │       └── style.css
│   ├── templates
│   │   └── index.html
│   ├── __init__.py
│   └── routes.py
├── venv
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run.py

```

---

## 🐍 Virtual Environment Setup

### 5️⃣ Create Virtual Environment

```powershell
py -m venv venv
```

### 6️⃣ Activate Virtual Environment

```powershell
venv\Scripts\activate
```

Your terminal should show `(venv)` indicating it's active.

---

## 📦 Install Dependencies

Make sure you're in the project directory and `venv` is activated:

```powershell
py -m pip install -r requirements.txt --no-cache-dir
```

---

## 📄 `requirements.txt` Contents

```txt
# Flask and Web Development
Flask
Dash>=3.0.4
Flask-SQLAlchemy>=3.0.0
Flask-Migrate>=4.0.0
python-dotenv>=1.0.0

# Database Connectors (Optional)
psycopg2-binary>=2.9.0   # PostgreSQL
PyMySQL>=1.0.0           # MySQL/MariaDB

# Data Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0

# Scientific Computing
numpy>=1.24.0
scipy>=1.10.0
pandas>=2.0.0
scikit-learn>=1.3.0
statsmodels>=0.14.0

# Development Utilities
ipython>=8.10.0
jupyterlab>=4.0.0

# Optional Extras
openpyxl>=3.1.0
```

---

### ```app_settings\__init__.py```
```
from flask import Flask


def create_app():
    app = Flask(__name__)

    # Register Flask routes
    from .routes import main
    app.register_blueprint(main)

    # Register Dash apps from app_module
    from app_modules.ci_computer import init_dataTbl
    init_dataTbl(app)


    return app
```

---
### ```app_settings\routes.py```
```
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

```
---

### ```run.py```
```
from app_settings import create_app # Import create_app method from app directory..
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

app_settings = create_app()

if __name__ == "__main__":
    app_settings.run(host='0.0.0.0', port=8051, debug=True)


```

## 🚀 Running the Flask Application

Ensure your environment is activated:

```powershell
venv\Scripts\activate
```

Then, run the app:

```powershell
python run.py
```

---

### ```Output in Terminal```
```
(venv) PS C:\Users\numan\Apps\DevProject\nPy> py run.py
 * Serving Flask app 'app_settings'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8051
 * Running on http://11.161.4.50:8051
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 398-157-483
```
---

## 🎨 Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📃 License

This project is open-source under standard license terms.

---

