from marshmallow import Schema, fields


class ResponseSchemaWeather(Schema):
    city = fields.Str()
    country = fields.Str()
    degrees = fields.Str()


class ResponseSchemaDriveStatus(Schema):
    message = fields.Str(default=" ")
    data = fields.List(fields.Dict())


class SchemaDriveStatusPOST(Schema):
    mes = fields.Str()

class ResponseSchemaSystemInfo(Schema):
    Users = fields.Str()
    MemoryGB = fields.Str()
    MemoryFullInfo = fields.Str()
    vCpus = fields.Str()
    CpuPercent = fields.Str()
