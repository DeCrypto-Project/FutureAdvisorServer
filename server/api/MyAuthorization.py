from importlib.resources import Resource

from flask import jsonify
from flask_apispec import MethodResource


class MyAuthorization(MethodResource, Resource):
    def post(self):
        message = {'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im5wb3JhdEBvdXRicmFpbi5jb20iLCJmaXJzdE5hbWUiOiJOYWRhdiIsImxhc3ROYW1lIjoiUG9yYXQiLCJkZXBhcnRtZW50IjoiQ2xvdWQgUGxhdGZvcm0gKENMRFBMVEZNKSIsInVpZCI6Im5wb3JhdCIsImdyb3VwcyI6WyJrYWZrYV9hZG1pbnMiLCJzcGFya19hZG1pbnMiLCJwbGF0Zm9ybV9hZG1pbnMiLCJ3b3JrZmxvd19hZG1pbnMiXSwiaWF0IjoxNjQ1OTUyMzEzLCJleHAiOjE2NDY1NTcxMTN9.fG-Qedu1MhZm5bJZpzoiUunRxKNZvyL4fvbmlFkGLQE"}
        return jsonify(message)
