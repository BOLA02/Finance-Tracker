from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date
from database import db, init_db
from models import Transaction

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ app.instance_path.replace('\\','/') + '/finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    db.init_app(app)
    CORS(app)

    @app.route('/transactions', methods=['POST'])
    def add_transaction():
        data = request.get_json() or {}
        title = data.get('title')
        amount = data.get('amount')
        category = data.get('category')
        ttype = data.get('type')
        datestr = data.get('date')

        if not title:
            return jsonify({"error": "title is required"}), 400
        if amount is None:
            return jsonify({"error": "amount is required"}), 400
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return jsonify({"error": "amount must be a number"}), 400
        if ttype not in ('income', 'expense'):
            return jsonify({"error": "type must be 'income' or 'expense'"}), 400

        if datestr:
            try:
                dt = datetime.strptime(datestr, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "date must be in YYYY-MM-DD format"}), 400
        else:
            dt = date.today()

        tx = Transaction(title=title, amount=amount, category=category or '', type=ttype, date=dt)
        db.session.add(tx)
        db.session.commit()

        return jsonify({"message": "Transaction added", "transaction": tx.to_dict()}), 201

    @app.route('/transactions', methods=['GET'])
    def get_transactions():
        transactions = Transaction.query.order_by(Transaction.id.desc()).all()
        return jsonify({"transactions": [t.to_dict() for t in transactions]}), 200

    @app.route('/transactions/income', methods=['GET'])
    def get_income():
        transactions = Transaction.query.filter_by(type='income').order_by(Transaction.id.desc()).all()
        return jsonify({"transactions": [t.to_dict() for t in transactions]}), 200

    @app.route('/transactions/expense', methods=['GET'])
    def get_expense():
        transactions = Transaction.query.filter_by(type='expense').order_by(Transaction.id.desc()).all()
        return jsonify({"transactions": [t.to_dict() for t in transactions]}), 200

    @app.route('/transactions/<int:tx_id>', methods=['GET'])
    def get_transaction(tx_id):
        tx = Transaction.query.get(tx_id)
        if not tx:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify(tx.to_dict()), 200

    @app.route('/transactions/<int:tx_id>', methods=['DELETE'])
    def delete_transaction(tx_id):
        tx = Transaction.query.get(tx_id)
        if not tx:
            return jsonify({"error": "Transaction not found"}), 404
        db.session.delete(tx)
        db.session.commit()
        return jsonify({"message": "Transaction deleted"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
