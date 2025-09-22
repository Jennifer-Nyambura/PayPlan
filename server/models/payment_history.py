from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config  import db

class PaymentHistory(db.Model):
    __tablename__ = 'payment_histories'
    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Numeric(10,2),nullable = False)
    due_date = db.Column(db.Date,nullable =False)
    paid = db.Column(db.Boolean,default = False)
    paid_at = db.Column(db.DateTime)
    expense_id = db.Column(db.Integer,db.ForeignKey('expenses.id'),nullable = False)


    #relationships
    expense = db.relationship("Expense", back_populates="payment_histories")


    def __repr__(self):
        return f"<PaymentHistory{self.id},{self.amount},{self.due_date},{self.paid},{self.paid_at}>"