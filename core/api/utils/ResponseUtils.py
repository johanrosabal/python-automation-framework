from core.config.logger_config import setup_logger
logger = setup_logger('TestPost')


class ResponseUtils:

    def __init__(self, response):
        self._response = None
        self._response = response

    def get_cookies(self):
        logger.info(f"Response Cookies:\n{self._response.cookies}")
        return self._response.cookies

    def verify_content_type(self, content_type):
        if str(self._response.headers['Content-Type']) == str(content_type):
            logger.info(
                f"PASS: Content Type: Content Type:[{self._response.headers['Content-Type']}]")
        else:
            logger.error(f"FAIL: Content Type, expected [{content_type}] but actual code is [{self._response.headers['Content-Type']}]")
        return self

    def verify_status_success_code(self, status_code):
        try:
            logger.info(f"verify_status_success_code:[{self._response.status_code}]")
            if self._response.status_code == status_code:
                logger.info(
                    f"PASS: Status Code: Status:[{self._response.status_code}] | URl Endpoint:[{self._response.url}]")
                logger.info(f"Response Time (seconds): {self._response.elapsed.total_seconds()}")
                logger.info(f"Response Headers:\n{self._response.headers}")
                logger.info(f"Response Text:\n{self._response.text}")
            else:
                logger.error(f"FAIL: Status Code, expected 200 but actual code is [{self._response.status_code}]")
                logger.error(f"Response text: {self._response.text}")
                assert self._response.status_code == status_code, f"Unexpected status code: {self._response.status_code}"
        except ValueError as e:
            logger.error(f"JSON decoding failed: {e}")
            logger.error(f"Response text: {self._response.text}")
        return self

    def verify_json(self):
        data = self._response.json()
        logger.info(f"Data: {data}")
        return data

    def get_size(self):
        size = len(self._response.json())
        logger.info(f"Size: {size}")
        return size




