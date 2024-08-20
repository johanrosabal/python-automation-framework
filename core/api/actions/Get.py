import requests
from core.config.logger_config import setup_logger
logger = setup_logger('Get')


class Get:
    def __init__(self, base_url):
        self.base_url = base_url
        self.endpoint = ""
        self.headers = {}
        self.params = None
        self.allow_redirects = True
        self.auth = None
        self.cert = None
        self.cookies = None
        self.proxies = None
        self.stream = False
        self.timeout = None
        self.verify = False
        self.response = None

    def set_endpoint(self, endpoint):
        """Set the API endpoint."""
        self.endpoint = endpoint
        return self

    def add_header(self, key, value):
        """Add a header to the request."""
        self.headers[key] = value
        return self

    def set_params(self, params):
        """Set the query parameters to be sent in the request."""
        self.params = params
        return self

    def set_allow_redirects(self, allow):
        """Set whether to allow redirects."""
        self.allow_redirects = allow
        return self

    def set_auth(self, username, password):
        """Set the authentication for the request."""
        self.auth = (username, password)
        return self

    def set_cert(self, cert):
        """Set the certificate or key file for the request."""
        self.cert = cert
        return self

    def set_cookies(self, cookies):
        """Set the cookies to be sent in the request."""
        self.cookies = cookies
        return self

    def set_proxies(self, proxies):
        """Set the proxies to be used for the request."""
        self.proxies = proxies
        return self

    def set_stream(self, stream):
        """Set whether to stream the response."""
        self.stream = stream
        return self

    def set_timeout(self, timeout):
        """Set the timeout for the request."""
        self.timeout = timeout
        return self

    def set_verify(self, verify):
        """Set whether to verify the server's TLS certificate."""
        self.verify = verify
        return self

    def build_url(self, **kwargs):
        """Insert dynamic values into the endpoint URL."""
        self.endpoint = self.endpoint.format(**kwargs)
        return self

    def send(self):
        """Send the GET request and return the response."""
        url = f"{self.base_url}/{self.endpoint}"
        logger.info(
            f"Sending GET to: {url} With params: {self.params}, headers: {self.headers}")

        try:
            # Send the GET request
            self.response = requests.get(
                url,
                params=self.params,
                headers=self.headers,
                allow_redirects=self.allow_redirects,
                auth=self.auth,
                cert=self.cert,
                cookies=self.cookies,
                proxies=self.proxies,
                stream=self.stream,
                timeout=self.timeout,
                verify=self.verify
            )
            self.response.raise_for_status()  # Raise an error for 4xx or 5xx status codes
            logger.info("Response received successfully")
        except requests.exceptions.HTTPError as err:
            logger.error(f"Error in GET request: {err}")
            self.response = None

        return self

    def get_response(self):
        """Get the response from the GET request."""
        return self.response

    def get_response_json(self):
        """Get the JSON response from the GET request."""
        if self.response is not None:
            return self.response.json()
        return None
