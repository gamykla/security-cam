import logging

from TwitterAPI import TwitterAPI

logger = logging.getLogger(__name__)


class TwitterImageStore(object):

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def save_image(self, image_data):
        """ Persist an image
        image_data - Byte array of image data
        """
        logger.debug("Saving image in twitter.")
        response = self.api.request('statuses/update_with_media', {'status': 'This is a test'}, {'media[]': image_data})
        logger.debug("Twitter response, status_code={} text={}".format(response.status_code, response.text))
