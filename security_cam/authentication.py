from functools import wraps
from flask import request, Response
import logging
import httplib

import configuration

logger = logging.getLogger(__name__)


def is_authorized(client_key, client_secret):
    """Ghetto auth implementation"""
    config = configuration.Configuration()
    authorized_client_key = config.get_value("")
    authorized_client_secret = config.get_value("")
    return client_key == authorized_client_key and client_secret == authorized_client_secret


UNATHORIZED = Response('Unathorized', httplib.UNAUTHORIZED, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def authorization_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            logger.info("Authentication failure. No credentials provided on request.")
            return UNATHORIZED
        if not is_authorized(auth.username, auth.password):
            logger.info("Authentication failure for username {}".format(auth.username))
            return UNATHORIZED
        return f(*args, **kwargs)
    return decorated
