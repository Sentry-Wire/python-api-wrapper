from sentrywire.base import EndpointHandler


class ActiveTriggers(EndpointHandler):
    path = "/activetriggers"

    def __init__(self, sw):
        """Active trigger handler
        """
        super(ActiveTriggers, self).__init__(sw, self.path)

    def create(self, trigger_name, search_filter, seconds_before, seconds_after):
        """Creates an active trigger
        Args:
            trigger_name (str): Must not be duplicate of any existing active filters
            search_filter (str): Valid BPF filter e.g. "dst port 80"
            seconds_before (non-neg int): Indicates the duration (in seconds) to go back from the time a trigger occurs.
            seconds_after (non-neg int): Indicates the duration (in seconds) of the search from the time a trigger occurs.
        Returns:
            (dict): number of current triggers and maximum number of triggers, or error message
            {
                "currTriggerCount": 2,
                "maxTriggerCount": 100
            }
        """
        post_data = {"rest_token": self.sw.rest_token,
                     "trigger_name": trigger_name,
                     "search_filter": search_filter,
                     "seconds_before": seconds_before,
                     "seconds_after": seconds_after}
        message = self.sw.http_post(self.path, post_data=post_data)
        return message

    def delete(self, trigger_name):
        """Delete an active trigger
        Args:
            trigger_name (str): a specific trigger name
        Returns:
            (dict): status in message
            {
              "message": "continuum_ac4 Deleted."
            }
        """
        params = {"rest_token": self.sw.rest_token,
                  "trigger_name": trigger_name}
        message = self.sw.http_delete(self.path, params=params)
        return message

    def list(self, trigger_name=None):
        """Lists active triggers
        Args:
            trigger_name (str): Optional, only get information about a specific trigger
        Returns:
            (list of dict): list of triggers and their information
            [
                {
                    'trigger_name': 'HTTP_nonstandard',
                    'search_filter': '(tcp[20:4] = 0x48545450) and (not port 80 and not port 8080)',
                    'seconds_before': '30',
                    'seconds_after': '30',
                    'createdtime': '2021-07-20T16:54:49.95Z'
                },
                {
                    'trigger_name': 'tcpflag_rst',
                    'search_filter': 'tcp[tcpflags] = tcp-rst',
                    'seconds_before': '30', 'seconds_after': '30',
                    'createdtime': '2021-07-20T16:55:28.842Z'
                },
                ...
            ]
        """
        params = {"rest_token": self.sw.rest_token,
                  "trigger_name": trigger_name}
        list_of_triggers = self.sw.http_get(self.path, params=params)
        if not isinstance(list_of_triggers, list):
            list_of_triggers = [list_of_triggers]
        return list_of_triggers
