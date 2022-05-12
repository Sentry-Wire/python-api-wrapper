import time

import requests

import sentrywire.const
from sentrywire.exceptions import ErrorLookupTable, SentrywireException


class Sentrywire:
    """
    Tracks session for an API connection
    """

    def __init__(self,
                 host,
                 rest_token=None,
                 session=None,
                 api_version="2",
                 ssl_verify=True,
                 retry_transient_errors=False,
                 timeout=sentrywire.const.TIMEOUT,
                 server_port=sentrywire.const.SERVER_PORT,
                 user_agent=sentrywire.const.USER_AGENT
                 ):
        """
        Setup the client handler for the sentrywire API
        """
        self.host = host
        self.server_port = server_port

        self._base_url = self._get_base_url(host, server_port)
        self._api_version = str(api_version)
        self._url = "%s/v%s" % (self._base_url, self._api_version)

        self.verify = ssl_verify
        self.timeout = timeout
        self.retry_transient_errors = retry_transient_errors

        self.user_agent = user_agent
        self.headers = {"User-Agent": user_agent}

        self.rest_token = rest_token

        # Create a session object for requests
        self.session = session or requests.Session()

        # NOTE: We must delay import of sentrywire.v2 objects until now or
        # otherwise it will cause circular import errors
        import sentrywire.v2
        objects = sentrywire.v2
        self._objects = objects

        # Map functions
        # Active Triggers
        self.activetriggers = objects.ActiveTriggers(self)
        # Authentication functionality
        self.authentication = objects.Authentication(self)
        self.login = self.authentication.login
        self.logout = self.authentication.logout
        # Authorization functionality
        self.authorization = objects.Authorization(self)
        # Federation functionality
        self.federation = objects.Federation(self)
        # IDS Rule functionality
        self.idsrules = objects.IDSRules(self)
        # Pre-capture filter functions
        self.precapturefilter = objects.PrecaptureFilter(self)
        # Search functionality
        self.searches = objects.Search(self)
        # Log functionality
        self.logs = objects.Logs(self)
        # Server functionality
        self.server = objects.Server(self)

    def __exit__(self):
        if self.rest_token:
            self.authentication.logout()
        self.session.close()

    def login(self, username, password):
        self.rest_token = self.authentication.login(username, password)

    @staticmethod
    def _get_base_url(host, port):
        """Return the base URL with the trailing slash stripped.
        Returns:
            str: The base URL
        """
        if ":" in host:
            raise Exception("Specify non-default port in server_port")
        if "http" not in host:
            host = "https://" + host
        host = host.rstrip("/")

        return host + ":" + str(port)

    @property
    def url(self):
        """The user-provided server URL."""
        return self._base_url

    @property
    def api_url(self):
        """The computed API base URL."""
        return self._url

    @property
    def api_version(self):
        """The API version used: 1"""
        return self._api_version

    def http_delete(self, path, **kwargs):
        """Make a DELETE request to the server.
        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            **kwargs: Extra options to send to the server (e.g. sudo)
        Returns:
            The requests object.
        Raises:
            GitlabHttpError: When the return code is not 2xx
        """
        result = self.http_request("delete", path, **kwargs)
        if "Content-Type" in result.headers:
            if (
                    result.headers["Content-Type"] == "application/json"
            ):
                try:
                    return result.json()
                except Exception:
                    raise sentrywire.exceptions.SentrywireException("Failed to parse the server message")
            else:
                return result
        return result

    def http_get(
            self,
            path,
            query_data=None,
            raw=False,
            **kwargs
    ):
        """Make a GET request to the server.
        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            raw (bool): If True do not try to parse the output as json
            **kwargs: Extra options to send to the server (e.g. sudo)
        Returns:
            The parsed json data.
        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        query_data = query_data or {}
        result = self.http_request(
            "get", path, query_data=query_data, **kwargs
        )
        if "Content-Type" in result.headers:
            if (
                    result.headers["Content-Type"] == "application/json"
                    and not raw
            ):
                try:
                    return result.json()
                except Exception:
                    raise sentrywire.exceptions.SentrywireException("Failed to parse the server message")
            else:
                return result

    def http_put(
            self,
            path,
            query_data=None,
            post_data=None,
            raw=False,
            files=None,
            **kwargs
    ):
        """Make a PUT request to the Gitlab server.
        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            post_data (dict): Data to send in the body (will be converted to
                              json by default)
            raw (bool): If True, do not convert post_data to json
            files (dict): The files to send to the server
            **kwargs: Extra options to send to the server (e.g. sudo)
        Returns:
            The parsed json returned by the server.
        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        query_data = query_data or {}
        post_data = post_data or {}

        result = self.http_request(
            "put",
            path,
            query_data=query_data,
            post_data=post_data,
            files=files,
            raw=raw,
            **kwargs
        )
        try:
            return result.json()
        except Exception:
            raise sentrywire.exceptions.SentrywireException("Failed to parse the server message")

    def http_post(
            self,
            path,
            query_data=None,
            post_data=None,
            raw=False,
            files=None,
            **kwargs
    ):
        """Make a POST request to the server.
        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            post_data (dict): Data to send in the body (will be converted to
                              json by default)
            raw (bool): If True, do not convert post_data to json
            files (dict): The files to send to the server
            **kwargs: Extra options to send to the server (e.g. sudo)
        Returns:
            The parsed json returned by the server if json is return, else the
            raw content
        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        query_data = query_data or {}
        post_data = post_data or {}

        result = self.http_request(
            "post",
            path,
            query_data=query_data,
            post_data=post_data,
            files=files,
            raw=raw,
            **kwargs
        )
        try:
            if result.headers.get("Content-Type", None) == "application/json":
                return result.json()
        except Exception:
            raise sentrywire.exceptions.SentrywireException("Failed to parse the server message")
        return result

    def http_request(
            self,
            verb,
            path,
            params=None,
            post_data=None,
            raw=False,
            files=None,
            timeout=None,
            max_retries=10,
            **kwargs
    ):
        """Make an HTTP request to the server.
        Args:
            verb (str): The HTTP method to call ('get', 'post', 'put',
                        'delete')
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            params (dict): Data to send as query parameters
            post_data (dict): Data to send in the body (will be converted to
                              json by default)
            raw (bool): If True, do not convert post_data to json
            files (dict): The files to send to the server
            timeout (float): The timeout, in seconds, for the request
            max_retries (int): Max retries after 429 or transient errors,
                               set to -1 to retry forever. Defaults to 10.
        Returns:
            A requests result object.
        Raises:
            -
        """
        url = self._build_url(path)

        opts = self._get_session_opts()

        # If timeout was defined, allow it to override the default
        if timeout is None:
            timeout = self.timeout

        # We need to deal with json vs. data when uploading files
        json, data, content_type = self._prepare_send_data(files, post_data, raw)

        # Requests assumes that `.` should not be encoded as %2E and will make
        # changes to urls using this encoding. Using a prepped request we can
        # get the desired behavior.
        if files:
            req = requests.Request(verb, url, json=json, data=data, params=params, files=files, **opts)
        else:
            req = requests.Request(verb, url, json=json, data=data, params=params, **opts)

        prepped = self.session.prepare_request(req)
        settings = self.session.merge_environment_settings(
            prepped.url, {}, None, self.verify, None
        )

        cur_retries = 0
        while True:
            result = self.session.send(prepped, timeout=timeout, **settings)

            if 200 <= result.status_code < 300:
                return result

            retry_transient_errors = kwargs.get(
                "retry_transient_errors", self.retry_transient_errors
            )
            if result.status_code in [500, 502, 503, 504] and retry_transient_errors:
                if max_retries == -1 or cur_retries < max_retries:
                    wait_time = 2 ** cur_retries * 0.1
                    if "Retry-After" in result.headers:
                        wait_time = int(result.headers["Retry-After"])
                    cur_retries += 1
                    time.sleep(wait_time)
                    continue

            error_message = result.content
            try:
                error_json = result.json()
                for k in ("message", "error", "msg"):
                    if k in error_json:
                        error_message = error_json[k]
            except (KeyError, ValueError, TypeError):
                pass

            if result.status_code in ErrorLookupTable:
                if error_message:
                    raise ErrorLookupTable[result.status_code](error_message)
                else:
                    raise ErrorLookupTable[result.status_code]()

            raise SentrywireException(error_message)

    @staticmethod
    def _prepare_send_data(
            files=None,
            post_data=None,
            raw=False,
    ):
        if files:
            return None, files, "multipart/form-data"

        if raw and post_data:
            return None, post_data, "application/octet-stream"

        return post_data, None, "application/json"

    def _get_session_opts(self):
        return {
            "headers": self.headers.copy()
        }

    def _build_url(self, path):
        """Returns the full url from path.
        Appends path to the stored url.
        Returns:
            str: The full URL
        """
        return "%s%s" % (self._url, path)

    @staticmethod
    def enable_debug():
        import logging
        import sys
        if sys.version_info[0] == 3:
            from http.client import HTTPConnection
            from requests.packages.urllib3.exceptions import InsecureRequestWarning

            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

            HTTPConnection.debuglevel = 1
            logging.basicConfig()
            log = logging.getLogger()
            log.setLevel(logging.DEBUG)
            log.propagate = False
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
        elif sys.version_info[0] == 2:
            import httplib

            # Debug logging
            httplib.HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            req_log = logging.getLogger('requests.packages.urllib3')
            req_log.setLevel(logging.DEBUG)
            req_log.propagate = True
        else:
            raise Exception("Debugging is not supported in your python version")

    @staticmethod
    def disable_debug():
        import sys
        import logging
        if sys.version_info[0] == 3:
            from http.client import HTTPConnection

            HTTPConnection.debuglevel = 0
            logging.basicConfig()
            log = logging.getLogger()
            log.setLevel(logging.WARNING)
            log.propagate = False
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.WARNING)
            requests_log.propagate = False
        elif sys.version_info[0] == 2:
            import httplib

            # Debug logging
            httplib.HTTPConnection.debuglevel = 0
            logging.basicConfig()
            logging.getLogger().setLevel(logging.WARNING)
            req_log = logging.getLogger('requests.packages.urllib3')
            req_log.setLevel(logging.WARNING)
            req_log.propagate = False
