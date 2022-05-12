from sentrywire.client import Sentrywire


class SentrywireHandler(object):
    """
    A parent class for creating other sentrywire api calls
    Not to be instantiated by users
    """
    def __init__(self, sw):
        """Link to Sentrywire client to handle"""
        # if isinstance(sw, Sentrywire):
        #     raise ValueError("SentrywireHandler must have a valid Sentrywire unit")
        self.sw = sw


class EndpointHandler(SentrywireHandler):
    """
    A parent class for creating other sentrywire api calls
    Not to be instantiated by users
    """
    def __init__(self, sw, path):
        """Link to Sentrywire client to handle"""
        super(EndpointHandler, self).__init__(sw)
        if path[0] != '/':
            raise ValueError("Path must start with '/'")
        self.path = path
        self.params = None
        self.json_data = None
