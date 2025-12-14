Finance Tracker API (Backend)
This is a backend REST API built with Flask for tracking personal finances.

It allows users to:
Register and authenticate accounts
Create and manage income/expense transactions
Filter transactions by date
View monthly financial summaries


Features
The API supports:

-User registration and login
-Password reset (no email token)
-User-based transactions (each transaction belongs to a user)
-Add new transactions (income or expense)
-Get all user transactions
-Filter transactions by date range
-Update a transaction
-Monthly summary (income vs expense)
-SQLite database storage
-JSON-based API responses


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

1.Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate


2.Install dependencies

pip install -r requirements.txt


3.Run the backend server

python app.py


The API will be available at:
http://127.0.0.1:5000


The database file (finance.db) is automatically created inside the instance folder.



Authentication Endpoints

➤ Register a user

POST `/register`

json
{
  "email": "test@example.com",
  "password": "123456"
}



➤ Login

POST `/login`

json
{
  "email": "test@example.com",
  "password": "123456"
}


Response includes:
json
{
  "message": "login successful",
  "user_id": 1
}


The returned `user_id` must be sent in request headers for protected endpoints(forgot password and transaction endpoints)

Forgot password endpoint require this header

```
X-User-ID: <user_id>
```


➤ Forgot Password

POST `/forgot-password`

json
{
  "email": "test@example.com",
  "new_password": "newpassword123"
}



Transactions
All transaction endpoints require this header:

```
X-User-ID: <user_id>
```

---

➤ Add a transaction

POST `/transactions`

json
{
  "title": "Salary",
  "amount": 5000,
  "category": "Job",
  "type": "income",
  "date": "2025-01-10"
}



➤ Get all transactions

GET `/transactions`



➤ Filter transactions by date

GET`/transactions?from=2025-01-01&to=2025-01-31`



➤ Update a transaction

PUT `/transactions/<transaction_id>`

json
{
  "title": "Updated Salary",
  "amount": 5500
}



➤ Monthly summary (income vs expense)

GET `/summary/<year>/<month>`




Testing with Postman

-Ensure Postman is using the **Desktop Agent**
-All requests should be sent to:

```
http://127.0.0.1:5000
```

-Set request body type to **raw → JSON**
-Include `X-User-ID` header where required



