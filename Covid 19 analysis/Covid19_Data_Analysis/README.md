# Design and Implementation of an Interactive COVID-19 Forecasting System using Django Framework

**Author:** Raghavendra T  
**Course:** Mini Project, 5th Semester, CSE  

---

## Project Overview

This project is an **Interactive COVID-19 Forecasting System** built using the **Django framework**. The system provides a user-friendly interface to visualize and analyze COVID-19 data, helping users understand trends, cases, and forecasts interactively.  

Key features include:  
- Real-time COVID-19 data visualization  
- Interactive graphs and charts  
- Forecasting future cases using historical data  
- User-friendly and responsive web interface  

---

## Technologies Used

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Data Visualization:** Matplotlib / Plotly / Chart.js  
- **Database:** SQLite (default for Django projects)  
- **Other:** Pandas for data manipulation  

---

## Setup Instructions (Windows + VS Code)

1. **Clone the project** or extract the ZIP file.  
2. **Open the project folder in VS Code**.  
3. **Create a virtual environment** (recommended):  
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate # macOS/Linux

**Install dependencies:**

bash
Copy code
pip install -r requirements.txt
Run migrations:

bash
Copy code
python manage.py migrate
Start the server:

bash
Copy code
python manage.py runserver
Open the web app in your browser:

cpp
Copy code
http://127.0.0.1:8000/

**Usage**
Navigate through the dashboard to view COVID-19 statistics.

Use interactive charts to compare cases and trends.

Forecast future COVID-19 cases using the forecasting feature.

**License**
No license required. For academic use only.

