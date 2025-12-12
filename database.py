import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception:
        os.makedirs(os.path.join('.', 'instance'), exist_ok=True)

    db_path = os.path.join(app.instance_path, 'finance.db')

    if not os.path.exists(db_path):
        open(db_path, 'a').close()
