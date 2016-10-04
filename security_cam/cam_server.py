import base64
import httplib
import logging
import sys
import json

from flask import Flask
from flask import request

import configuration
import twitter_handler
from authentication import authorization_required


root = logging.getLogger()
root.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

root.addHandler(stream_handler)

logger = logging.getLogger(__name__)

app = Flask(__name__)


config = configuration.Configuration()

try:
    img_store = twitter_handler.TwitterImageStore(
        config.get_value("TWITTER_CONSUMER_KEY"),
        config.get_value("TWITTER_CONSUMER_SECRET"),
        config.get_value("TWITTER_ACCESS_TOKEN_KEY"),
        config.get_value("TWITTER_ACCESS_TOKEN_SECRET"))
except:
    logger.exception("An error occurec creating twitter handler.")


@app.route("/health/", methods=['GET'])
def health_check():
    logger.debug("Health check endpoint.")
    return '{"status": "OK"}', httplib.OK, {}


@app.route("/captures/", methods=['POST'])
@authorization_required
def handle_image_capture():
    """Create an image capture."""
    logger.debug("Handling image capture request.")

    try:
        request_json = request.get_json()
        image_data_base64 = request_json['image_data_b64']
        image_bytes = base64.decodestring(image_data_base64)
        img_store.save_image(image_bytes)

        return json.dumps({"status": "ok"}), httplib.CREATED, {}
    except:
        logger.exception("An error has occured.")
        return '{"response": "Internal error."}', httplib.INTERNAL_SERVER_ERROR, {}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
