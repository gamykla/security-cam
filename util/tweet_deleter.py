import json
import httplib
import logging
import sys

from TwitterAPI import TwitterAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterStatusDeleter(object):
    """ Delete all tweets """

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.deleted_count = 0
        self.api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def _get_statuses(self):
        response = self.api.request("statuses/user_timeline")
        response_json = json.loads(response.text)
        logger.info("Loaded {} statuses".format(len(response_json)))
        return response_json

    def _delete(self, tweet_id):
        response = self.api.request("statuses/destroy/:{}".format(tweet_id), )
        if response.status_code != httplib.OK:
            raise Exception("There was a problem deleting tweets. {} {}".format(response.status_code, response.text))
        self.deleted_count += 1

    def do_it(self):
        while True:
            statuses = self._get_statuses()
            if len(statuses) > 0:
                for item in statuses:
                    self._delete(item['id'])
            else:
                break

            if self.deleted_count % 20 == 0:
                logger.info("Deleted {} tweets..".format(self.deleted_count))

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise RuntimeError(
            "Arguments not provided: consumer_key, consumer_secret, access_token_key, access_token_secret")
    TwitterStatusDeleter(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]).do_it()
