from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db 

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #household_id = db.Column(db.Integer, db.ForeignKey('households.id'), nullable=False)
    #category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # Relationships
    payment_histories = db.relationship("PaymentHistory", back_populates="expense")

    # Validations can go here
    # Serializer rules can go here

    def __repr__(self):
        return f"<Expense {self.id}, {self.amount}, {self.description}>"
