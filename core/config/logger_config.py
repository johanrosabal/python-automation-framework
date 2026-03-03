import logging
import http.client as http_client


def setup_logger(name, enableDebug=False):
    logger = logging.getLogger(name)

    if enableDebug:
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

    if not enableDebug:
        logger.setLevel(logging.INFO)

    return logger
