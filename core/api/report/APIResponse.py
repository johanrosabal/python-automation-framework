import requests


class ApiResponse:
    def __init__(self, response):
        self._request_method = response.request.method
        self._request_url = response.url
        self._response_elapsed = response.elapsed
        self._response_status_code = response.status_code
        self._response_text = response.text
        self._response_reason = response.reason
        self._response = response

    @property
    def request_method(self):
        """Return the request method."""
        return self._request_method

    @property
    def request_url(self):
        """Return the request URL."""
        return self._request_url

    @property
    def response_elapsed(self):
        """Return the time taken for the request."""
        return self._response_elapsed

    @property
    def response_status_code(self):
        """Return the response status code."""
        return self._response_status_code

    @property
    def response_text(self):
        """Return the response text."""
        return self._response_text

    @property
    def response_reason(self):
        """Return the reason phrase associated with the response status code."""
        return self._response_reason

    @property
    def response(self):
        """Return the reason phrase associated with the response status code."""
        return self._response
