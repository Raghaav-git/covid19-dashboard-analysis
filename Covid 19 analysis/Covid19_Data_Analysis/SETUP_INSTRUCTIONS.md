 Complete Setup Instructions (Windows + VS Code)
1️⃣ Open the project in VS Code

Extract the ZIP file:
Covid_Dashboard.zip

Open the extracted folder in VS Code:

C:\Users\admin\Downloads\CovidDashboard_final_cleaned

2️⃣ Open a new terminal in VS Code

From the top menu:
Terminal → New Terminal

You’ll see a terminal open at the bottom (PowerShell or CMD).

3️⃣ Navigate to the folder containing manage.py

Run this command:

cd CovidDashboard


✅ You should now be in:

C:\Users\admin\Downloads\CovidDashboard_final_cleaned\CovidDashboard

4️⃣ (Optional) Create and activate a virtual environment

This keeps dependencies isolated.

python -m venv venv
venv\Scripts\activate

5️⃣ Install all dependencies

Install from the provided requirements.txt (located one folder up):

pip install -r ..\requirements.txt


If that fails, you can manually install the essentials:

pip install django pandas matplotlib

6️⃣ Make and apply migrations

This sets up your SQLite database.

python manage.py makemigrations
python manage.py migrate

7️⃣ Load the COVID-19 dataset into the database

This uses the built-in Django management command.

python manage.py load_covid_data

8️⃣ Run the development server

Start the Django web app:

python manage.py runserver

9️⃣ Open your browser

Go to:

http://127.0.0.1:8000/


You’ll see the COVID-19 Dashboard Home Page.
Click Compare to view cross-country comparisons.