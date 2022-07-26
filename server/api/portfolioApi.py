import json
from flask import request
from flask_apispec import MethodResource, marshal_with, use_kwargs
from flask_restful import Resource
from myResponses import ResponseSchemaDriveStatus, SchemaDriveStatusPOST
from marshmallow import fields

class DriveStatus(MethodResource, Resource):

    @marshal_with(SchemaDriveStatusPOST)
    @use_kwargs(SchemaDriveStatusPOST, location=('json'))
    def post(self):
        inFile = request.get_json()
        message = {'message': 'success'}
        dictionary = {"drives": []}

        for key, value in inFile.items():
            temp = {}
            for val in value.split(','):
                x, *y = val.strip().split()
                temp[x] = ' '.join(elem for elem in y)
            dictionary["drives"].append(temp)

        with open("input.json", "w") as outFile:
            try:
                json.dump(dictionary, outFile)
            except ValueError:
                message = {'message': 'failure'}

        outFile.close()
        return message

    @marshal_with(ResponseSchemaDriveStatus)
    @use_kwargs({"status": fields.Str()}, location="query")
    def get(self, **kwargs):
        status = request.args.get('status')
        with open("input.json", "r") as file:
            data = json.load(file)
            file.close()
            driveFilterList = list(filter(lambda dictionary: dictionary['status'] == status, data['drives']))

        var = {'message': f"Found {len(driveFilterList)} {status} drives"}
        if len(driveFilterList) != 0:
            var['data'] = driveFilterList
        return var