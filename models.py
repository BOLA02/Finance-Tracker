from database import db
from datetime import date

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(10), nullable=False)  
    date = db.Column(db.Date, nullable=False)

    def __init__(self, title, amount, category, type, date):
        self.title = title
        self.amount = amount
        self.category = category
        self.type = type
        self.date = date or date.today()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "type": self.type,
            "date": self.date.strftime('%Y-%m-%d')
        }
