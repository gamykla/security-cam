import os
import httplib
import json
import requests
from requests.auth import HTTPBasicAuth
from nose.tools import eq_


def _get_server_base_url():
    if 'SECURITYCAM_SERVER_BASE_URL' in os.environ:
        return os.environ.get('SECURITYCAM_SERVER_BASE_URL')
    return 'http://localhost:8080'


def _get_secrets():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_file = os.path.join(current_dir, "..", "secrets.json")
    with open(secrets_file, "r") as f:
        return json.loads(f.read())


def test_health_endpoint():
    for _ in range(10):
        response = requests.get("{}/health/".format(_get_server_base_url()))
        eq_(httplib.OK, response.status_code)


def test_image_capture():
    secrets = _get_secrets()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_image = os.path.join(current_dir, "resources", "test.jpg.b64")

    with open(test_image, "r") as f:
        image_data_b64 = f.read()

    headers = {'Content-Type': 'application/json'}
    data = {"image_data_b64": image_data_b64}

    response = requests.post(
        "{}/captures/".format(_get_server_base_url()),
        headers=headers,
        data=json.dumps(data),
        auth=HTTPBasicAuth(secrets['CLIENT_KEY'], secrets['CLIENT_SECRET']))

    print response.content
    eq_(response.status_code, httplib.CREATED)


def test_no_auth_provided_is_unauthorized():
    headers = {'Content-Type': 'application/json'}
    data = {"image_data_b64": "10101"}

    response = requests.post(
        "{}/captures/".format(_get_server_base_url()),
        headers=headers,
        data=json.dumps(data))

    eq_(response.status_code, httplib.UNAUTHORIZED)


def test_bad_credentials_is_unauthorized():
    headers = {'Content-Type': 'application/json'}
    data = {"image_data_b64": "10101"}

    response = requests.post(
        "{}/captures/".format(_get_server_base_url()),
        headers=headers,
        data=json.dumps(data),
        auth=HTTPBasicAuth("foo", "bar"))

    eq_(response.status_code, httplib.UNAUTHORIZED)
