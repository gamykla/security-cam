import os
import httplib
import json
import requests
from nose.tools import eq_


def test_image_capture():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_image = os.path.join(current_dir, "resources", "test.jpg.b64")

    with open(test_image, "r") as f:
        image_data_b64 = f.read()

    headers = {'Content-Type': 'application/json'}
    data = {"image_data_b64": image_data_b64}

    response = requests.post("http://localhost:8080/captures/", headers=headers, data=json.dumps(data))
    eq_(response.status_code, httplib.CREATED)
