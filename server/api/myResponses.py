from marshmallow import Schema, fields


class InputSchema(Schema):
    riskScore = fields.Int()
    amountToInvest = fields.Float()
    pass
