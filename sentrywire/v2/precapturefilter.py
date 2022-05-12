from sentrywire.base import EndpointHandler


class PrecaptureFilter(EndpointHandler):
    path = "/precapturefilters"

    def __init__(self, sw):
        """Precapture filter handler
        """
        super(PrecaptureFilter, self).__init__(sw, self.path)

    def create(self, search_filter):
        """Creates a pre-capture filter
        Args:
            search_filter (str): Valid BPF filter e.g. "dst port 80"
        Returns:
            (dict): success message, or raise exception
            {
                "message": "precapture filter set."
            }
        """
        post_data = {"rest_token": self.sw.rest_token,
                     "search_filter": search_filter}
        message = self.sw.http_post(self.path, post_data=post_data)
        return message

    def delete(self):
        """Reset ALL pre-capture filter configurations
        Returns:
            (dict): status in message
            {
              "message": "precapture filter reset."
            }
        """
        params = {"rest_token": self.sw.rest_token}
        message = self.sw.http_delete(self.path, params=params)
        return message

    def list(self):
        """Lists items in pre-capture filter
        Returns:
            (list of dict): list of triggers and their information
        """
        params = {"rest_token": self.sw.rest_token}
        list_of_filters = self.sw.http_get(self.path, params=params)
        return list_of_filters

    # Alias for documentation terminology
    set = create
    get = list
    reset = delete
