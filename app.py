from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

# app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3308/money_tracker'
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


@app.route('/')
def index():
    return "Flask MySQL Database Setup is Complete!"

@app.route('/workspace', methods=['GET'])
def workspace():
    return jsonify({"msg": "berhasil kehubung yey"})

@app.route('/form', methods=['GET', 'POST'])
def form():
    response_object = {'status':'success'}
    if request.method == "POST":
     post_data = request.get_json()
     name   = post_data.get('name'),
     date  = post_data.get('date')
     category = post_data.get('category')
     amount = post_data.get('amount')
     desc = post_data.get('desc')
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


if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Transaction table created successfully!")
        except Exception as e:
            print(f"Error creating table: {e}")
    app.run(debug=True)

