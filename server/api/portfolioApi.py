# import json
# from flask import request, make_response
# from flask_apispec import MethodResource, marshal_with, use_kwargs
# from flask_restful import Resource
# from myResponses import ResponseSchemaDriveStatus, SchemaDriveStatusPOST
# from marshmallow import fields
#
#
# class PortfolioApi(MethodResource, Resource):
#
#     @marshal_with(ResponseSchemaDriveStatus)
#     @use_kwargs({"status": fields.Str()}, location="query")
#     def get(self, **kwargs):
#         try:
#             portfolio_by_algorithm = db.session.query(Portfolio).filter_by(link=link).first()
#             if not portfolio_by_algorithm:
#                 return make_response(jsonify(message="לינק לא תקין"), 400)
#             res = [ps.as_dict() for ps in portfolio_by_algorithm.portfolio_stocks]
#             return make_response(jsonify(message="Porfolio", data=res), 200)
#         except Exception as e:
#             response = make_response(jsonify(message=str(e)), 400)
#
#         return response
