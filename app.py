from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

# app.config['CORS_HEADERS'] = 'Content-Type'

# #Celine
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3308/money_tracker'

#Joanna
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/money_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Transaction Model
class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime)

    def __init__(self, name, date, description, category, amount):
        self.name = name
        self.description = description
        self.category = category
        self.amount = amount
        self.date = date
    
    def to_dict(self):
        """Converts a Transaction object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'amount': self.amount,
            'date': self.date.isoformat() if self.date else None,
        }




@app.route('/')
def index():
    return "Flask MySQL Database Setup is Complete!"

@app.route('/workspace', methods=['GET'])
def workspace():
    transactions = Transaction.query.all()
    grouped = {'A': [],
               'B': [],
               'C': [],
               'D': [],
               'E':[]}
    for transaction in transactions:
        category = transaction.category
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(transaction.to_dict())
    return jsonify(grouped)

@app.route('/form', methods=['GET', 'POST'])
def form():
    response_object = {'status':'success'}
    if request.method == "POST":
     post_data = request.get_json()
     print("Received data:", post_data)
     name   = post_data.get('name'),
     date  = post_data.get('date')
     category = post_data.get('category')
     amount = post_data.get('amount')
     desc = post_data.get('description')
     new_transaction = Transaction(
        name=name,
        description=desc,
        category=category,
        amount=amount,
        date=date)
     # Add to the session and commit to the database
     db.session.add(new_transaction)
     db.session.commit()
     response_object['message'] ='Data added!'
    return jsonify(response_object)
# Update or Delete a Transaction
@app.route('/workspace/<int:transaction_id>', methods=['PUT', 'DELETE'])
def modify_transaction(transaction_id):
    response_object = {'status': 'success'}
    transaction = Transaction.query.get(transaction_id)

    if not transaction:
        response_object['status'] = 'fail'
        response_object['message'] = 'Transaction not found'
        return jsonify(response_object), 404

    if request.method == 'PUT':
        put_data = request.get_json()
        transaction.name = put_data.get('name', transaction.name)
        transaction.date = put_data.get('date', transaction.date)
        transaction.category = put_data.get('category', transaction.category)
        transaction.amount = put_data.get('amount', transaction.amount)
        transaction.description = put_data.get('description', transaction.description)

        db.session.commit()
        response_object['message'] = 'Transaction updated!'

    elif request.method == 'DELETE':
        db.session.delete(transaction)
        db.session.commit()
        response_object['message'] = 'Transaction deleted!'

    return jsonify(response_object)

@app.route('/login', methods=['POST']) 
def login(): 
    data = request.get_json() 
    username = data.get('username') 
    password = data.get('password') 
    # Hardcoded credentials 
    if username == 'admin' and password == '123': 
        return jsonify({"message": "Login successful"}) 
    else: 
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Transaction table created successfully!")
        except Exception as e:
            print(f"Error creating table: {e}")
    app.run(debug=True)

