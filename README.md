Finance Tracker API (Backend)

This is a simple backend API built with Flask.
It lets you save, view, filter, and delete financial transactions.
It uses SQLite as the database.

This project does not include a frontend.
It is only for backend practice.

Features
The API can:
-Add a new transaction (POST)
-Get all transactions (GET)
-Get only income transactions (GET)
-Get only expense transactions (GET)
-Get a single transaction by ID (GET)
-Delete a transaction by ID (DELETE)
-Store everything in a SQLite database (instance/finance.db)
-Return all responses in JSON format


Project Structure
finance-tracker/
│── app.py               
│── models.py            
│── database.py          
│── requirements.txt     
│── README.md            
│── instance/
│    └── finance.db      


Installation & Setup
1. Create and activate a virtual environment 

python -m venv venv
venv\Scripts\activate

2. Install all the required packages
pip install -r requirements.txt

3. Run the backend
python app.py

The server will start at:
http://127.0.0.1:5000

4. Create the database tables (only once)
Open Python shell:

python

Then run:

from app import create_app
from database import db
app = create_app()

with app.app_context():
    db.create_all()


This will create the transactions table in instance/finance.db.

NB: You do not need to do this again unless you delete your database.



Testing the API (Postman)
You can test your endpoints using Postman.

➤ Add a transaction (POST)

Method: POST

URL:

http://127.0.0.1:5000/transactions


Body → raw → JSON:

{
  "title": "Salary",
  "amount": 5000,
  "category": "Income",
  "type": "income",
  "date": "2025-01-10"
}


➤ Get all transactions (GET)
http://127.0.0.1:5000/transactions


➤ Get income transactions (GET)
http://127.0.0.1:5000/transactions/income


➤ Get expense transactions (GET)
http://127.0.0.1:5000/transactions/expense


➤ Get a transaction by ID (GET)

Example:
http://127.0.0.1:5000/transactions/1


➤ Delete a transaction (DELETE)

Example:
http://127.0.0.1:5000/transactions/1