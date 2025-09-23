from marshmallow import Schema,fields,validate

class PaymentHistorySchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True,validate=validate.Range(min=0.0))
    due_date=fields.Date(required=True)
    paid=fields.Boolean(required=True)
    paid_at=fields.Date(required=True)
    expense_id=fields.Int(required=True)
    