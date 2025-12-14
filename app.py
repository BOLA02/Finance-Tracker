from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date
from database import db, init_db
from models import User, Transaction

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.instance_path.replace('\\', '/') + '/finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)
    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()


    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "email and password required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "email already registered"}), 400

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "registration successful"}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"error": "invalid email or password"}), 401

        return jsonify({"message": "login successful", "user_id": user.id}), 200

    @app.route('/forgot-password', methods=['POST'])
    def forgot_password():
        data = request.get_json() or {}
        email = data.get('email')
        new_password = data.get('new_password')

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "email not registered"}), 404

        user.set_password(new_password)
        db.session.commit()
        return jsonify({"message": "password updated"}), 200


    def get_user():
        user_id = request.headers.get('X-User-ID')
        return User.query.get(user_id) if user_id else None

    @app.route('/transactions', methods=['POST'])
    def add_transaction():
        user = get_user()
        if not user:
            return jsonify({"error": "unauthorized"}), 401

        data = request.get_json()
        dt = datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else date.today()

        tx = Transaction(
            title=data['title'],
            amount=float(data['amount']),
            category=data.get('category', ''),
            type=data['type'],
            date=dt,
            user_id=user.id
        )

        db.session.add(tx)
        db.session.commit()
        return jsonify(tx.to_dict()), 201

    @app.route('/transactions', methods=['GET'])
    def get_transactions():
        user = get_user()
        if not user:
            return jsonify({"error": "unauthorized"}), 401

        start = request.args.get('from')
        end = request.args.get('to')

        query = Transaction.query.filter_by(user_id=user.id)

        if start and end:
            query = query.filter(Transaction.date.between(start, end))

        transactions = query.order_by(Transaction.id.desc()).all()
        return jsonify([t.to_dict() for t in transactions]), 200

    @app.route('/transactions/<int:tx_id>', methods=['PUT'])
    def update_transaction(tx_id):
        user = get_user()
        if not user:
            return jsonify({"error": "unauthorized"}), 401

        tx = Transaction.query.filter_by(id=tx_id, user_id=user.id).first()
        if not tx:
            return jsonify({"error": "transaction not found"}), 404

        data = request.get_json()
        tx.title = data.get('title', tx.title)
        tx.amount = float(data.get('amount', tx.amount))
        tx.category = data.get('category', tx.category)
        tx.type = data.get('type', tx.type)

        db.session.commit()
        return jsonify(tx.to_dict()), 200

    @app.route('/summary/<int:year>/<int:month>', methods=['GET'])
    def monthly_summary(year, month):
        user = get_user()
        if not user:
            return jsonify({"error": "unauthorized"}), 401

        transactions = Transaction.query.filter(
            Transaction.user_id == user.id,
            db.extract('year', Transaction.date) == year,
            db.extract('month', Transaction.date) == month
        ).all()

        income = sum(t.amount for t in transactions if t.type == 'income')
        expense = sum(t.amount for t in transactions if t.type == 'expense')

        return jsonify({"income": income, "expense": expense}), 200
    

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
