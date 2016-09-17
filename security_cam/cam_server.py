import httplib
import logging
import sys

from flask import Flask
from flask import request

root = logging.getLogger()
root.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
root.addHandler(stream_handler)

app = Flask(__name__)


@app.route("/captures/", methods=['POST'])
def hello():
    print ">>>>>{}".format(request.get_json())
    return "", httplib.CREATED, {}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
