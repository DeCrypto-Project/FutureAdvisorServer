from marshmallow import Schema, fields


class ResponseSchema(Schema):
    volatile = fields.Str()
    pass
