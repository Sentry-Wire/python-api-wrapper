from sentrywire.base import EndpointHandler
from os.path import basename


class IDSRules(EndpointHandler):
    path = "/idsruleset"

    def __init__(self, sw):
        """IDS rule handler
        """
        super(IDSRules, self).__init__(sw, self.path)

    def create(self, file_path):
        """Upload a rule set. New rules are deactivated by default. Will override an existing rule with the same name.
        Args:
            file_path (str): path to the .rules file
        Returns:
            (dict): success message, or raise exception
            {
                "uploaded": "rules411.rules"
            }
        """
        files = {"rest_token": (None, self.sw.rest_token),
                 "fileUploadName": (basename(file_path), open(file_path, 'rb'))
                 }
        message = self.sw.http_post(self.path, files=files)
        return message

    def delete(self, rule_set_name):
        """Delete a rule set
        Args:
            rule_set_name (str): name of the rule set including ".rules"
        Returns:
            (dict): status in message
            {
              "message": "precapture filter reset."
            }
        """
        params = {"rest_token": self.sw.rest_token,
                  "rulesetname": rule_set_name}
        message = self.sw.http_delete(self.path, params=params)
        return message

    def list(self, list_type):
        """Lists rule sets
        Args:
            list_type (str): "activated" or "deactivated"
        Returns:
            (list of dict): list of triggers and their information
            Example
            [
              {
                "name": "UserRules1.rules",
                "count": 3,
                "error": "false"
              },
              {
                "name": "Now.rules",
                "count": 5,
                "error": "true"
              },
              {
                "name": "emerging-web_specific_apps.rules",
                "count": 4723,
                "error": "false"
              },
              ...
            ]
        """
        params = {"rest_token": self.sw.rest_token,
                  "type": list_type}
        list_of_filters = self.sw.http_get(self.path, params=params).json()
        return list_of_filters

    def activate(self, rule_set_name):
        """Activate a rule set
        Returns:
            (dict): list of triggers and their information
            Example
            {
                "message": "activated rules411.rules"
            }
        """
        params = {"rest_token": self.sw.rest_token,
                  "rulesetname": rule_set_name,
                  "action": "activate"}
        message = self.sw.http_put(self.path, params=params)
        return message

    def deactivate(self, rule_set_name):
        """Deactivate a rule set
        Returns:
            (dict): list of triggers and their information
            Example
            {
                "message": "deactivated rules411.rules"
            }
        """
        params = {"rest_token": self.sw.rest_token,
                  "rulesetname": rule_set_name,
                  "action": "deactivate"}
        message = self.sw.http_put(self.path, params=params)
        return message

    def get(self, rule_set_name, file_path):
        file_handler = open(file_path, 'wb+')

        params = {
            "rest_token": self.sw.rest_token,
            "rulesetname": rule_set_name
        }

        response = self.sw.http_get(self.path + "content", params=params)

        file_handler.write(response.content)
        file_handler.close()

        return response.content

    # Aliases for documentation terminology
    upload = create
    download = get
