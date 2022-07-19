import requests

def test_requestsWheater():
    url = "http://127.0.0.1:5000/v1/api/checkCurrentWeather"
    responses = requests.get(url)
    assert responses.status_code == 200
    response_body = responses.json()
    degrees = float(response_body['degrees'])
    assert degrees < 100 or degrees > -100
