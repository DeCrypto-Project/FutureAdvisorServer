from marshmallow import Schema, fields


class ResponseSchemaWeather(Schema):
    pass


class ResponseSchemaDriveStatus(Schema):
    message = fields.Str(default=" ")
    data = fields.List(fields.Dict())


class SchemaDriveStatusPOST(Schema):
    mes = fields.Dict()

class ResponseSchemaSystemInfo(Schema):
    Users = fields.Str()
    MemoryGB = fields.Str()
    MemoryFullInfo = fields.Str()
    vCpus = fields.Str()
    CpuPercent = fields.Str()
