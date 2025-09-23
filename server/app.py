#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import Expense, PaymentHistory 
from routes.expense_routes import ExpenseResource

# Views go here!

api.add_resource(ExpenseResource, '/expenses')

#@app.route('/')
#def index():
    #return '<h1>Project Server</h1>'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # only for dev/testing
    app.run(port=5555, debug=True)


