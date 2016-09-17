import httplib
import json
import requests
from nose.tools import eq_


def test_x():
    headers = {'Content-Type': 'application/json'}
    data = {"test": "hello world"}
    response = requests.post("http://localhost:8080/captures/", headers=headers, data=json.dumps(data))
    eq_(response.status_code, httplib.CREATED)
