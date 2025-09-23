from flask import request,jsonify
from flask_restful import Resource
from models.expense import Expense
from flask import make_response
from config import db
from schemas.expense_schema import ExpenseSchema

expense_schema = ExpenseSchema()
expenses_schema =ExpenseSchema(many=True)

class ExpenseResource(Resource):
    def get(self):
        response_dict={"message":"welcome to my app"}
        response =make_response(
            response_dict,200
        )
        return response
