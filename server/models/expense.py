from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db 

class Expense(db.Model,SerializerMixin):
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
    @validates('amount_paid')
    def validate_amount(self,key,value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value

    @validates('description')    
    def validate_description(self,key,value):
        if  not value or len(value.strip()) == 0:
            raise ValueError('Description cannot be empty')
        return value  
    @validates('timestamp')
    def validates_timestamp(self,key,value):
        if not isinstance(value,datetime):
            raise ValueError('Timestamp must be a datatime object')
        return value    


    # Serializer rules can go here
    serializer_rules =('-payment_histories.expense',)


    def __repr__(self):
        return f"<Expense {self.id}, {self.amount}, {self.description}>"
