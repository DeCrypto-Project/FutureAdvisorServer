import requests


def test_requestsDriveStatus():

    # Arrange
    url = "http://127.0.0.1:5000/v1/api/driveStatus"

    # ACT
    responses = requests.get(url)

    #Asert
    assert responses.status_code == 200


