from sentrywire.base import EndpointHandler
from sentrywire.exceptions import SentrywireException


class Authentication(EndpointHandler):
    path = "/fmadmin"

    def __init__(self, sw):
        super(Authentication, self).__init__(sw, self.path)

    def login(self, username, password):
        """Create new rest token for current client
        Args:
            username (str): Username for Sentrywire system
            password (str): Password for username in Sentrywire system
        Returns:
            (str): rest_token bound to current Sentrywire client
        """
        post_data = {"username": username,
                     "password": password}
        json = self.sw.http_post(self.path, post_data=post_data).json()
        self.sw.rest_token = json["rest_token"]
        return self.sw.rest_token

    def logout(self, rest_token=None):
        """Invalidate current rest_token
        Args:
            rest_token (str): Token to invalidate, if none is provided, will use the token in the client
        """
        rest_token = rest_token or self.sw.rest_token
        if not rest_token:
            raise SentrywireException("No rest token to invalidate")

        params = {"rest_token": rest_token}
        response = self.sw.http_put(self.path, params=params)
        self.sw.rest_token = None
        return response
