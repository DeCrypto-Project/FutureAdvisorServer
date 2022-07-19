import requests

def test_requestsSystemInfo():
    url = "http://127.0.0.1:5000/v1/api/consulCluster/systemInfo"
    responses = requests.get(url)
    assert responses.status_code == 200
    response_body = responses.json()
    CpuPercent = float(response_body['CpuPercent'])
    assert CpuPercent < 100 or CpuPercent >= 0