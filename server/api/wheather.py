import json

import flask
import ipinfo
import requests
from flask import app, jsonify
from flask_apispec import MethodResource, marshal_with
from flask_cors import cross_origin
from flask_restful import Resource
from myResponses import ResponseSchemaWeather


class Weather(MethodResource, Resource):

    def getIpLocation(self):
        access_token = '79501d36df1fb7'
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails()
        return details

    # This function get url openweathermap to get current whether by location
    def getURLDegreesByLocation(self, cityname):
        APIkey = 'e6218798871579c48a7beede2da0c907'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={APIkey}&units=metric'
        return url

    # This function get current degree by city location
    def getDegreesFromUrl(self, city):
        url = self.getURLDegreesByLocation(city)
        response = requests.get(url)
        data_json = json.loads(response.text)
        return data_json['main']['temp']

    # This build the return dictionary with required data city, country, degrees
    def buildDictionary(self):
        details = self.getIpLocation()
        city = details.city
        country = details.country
        degrees = self.getDegreesFromUrl(city)
        dictionary = {'city': city, 'country': country, 'degrees': degrees}
        return dictionary

    # get /checkCurrentWeather
    @marshal_with(ResponseSchemaWeather)  # marshalling with marshmallow library
    def get(self):
        teachers = ["2","3", "4"]
        return jsonify(teachers)




