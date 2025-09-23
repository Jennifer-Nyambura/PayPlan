from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config  import db

class PaymentHistory(db.Model,SerializerMixin):
    __tablename__ = 'payment_histories'
    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Numeric(10,2),nullable = False)
    due_date = db.Column(db.Date,nullable =False)
    paid = db.Column(db.Boolean,default = False)
    paid_at = db.Column(db.DateTime)
    expense_id = db.Column(db.Integer,db.ForeignKey('expenses.id'),nullable = False)


    #relationships
    expense = db.relationship("Expense", back_populates="payment_histories")
    
    #validations
    @validates('amount_paid')
    def validate_amount_paid(self,key,value):
        if value <=0:
            raise ValueError('Amount paid must be greater than 0')
        return value

    @validates('paid_at') 
    def validate_paid_at(self,key,value):
        if not isinstance (value,datetime):
           raise ValueError('paid_at must be a date_time object')

    #serializer rules
    serialize_rules =('-expense.payment_histories')

        


    def __repr__(self):
        return f"<PaymentHistory{self.id},{self.amount},{self.due_date},{self.paid},{self.paid_at}>"