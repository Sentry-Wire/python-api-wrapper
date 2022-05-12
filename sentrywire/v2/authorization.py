from sentrywire.base import EndpointHandler


class Roles(EndpointHandler):
    path = "/authorization"

    def __init__(self, sw):
        """Role handler
        """
        super(Roles, self).__init__(sw, self.path)

    def create(self, role_name, permissions):
        """Create a new role
        Args:
            role_name (str): name of role to add
            permissions (str): Comma separated list of permissions:
                               Valid options are Groups,Licensing,Authentication,Authorization,Auditing,Search,Policy
        Returns:
            (Dict):
            Example
            {
            'message': 'added role: auditor',
             }
        """
        post_data = {"rest_token": self.sw.rest_token,
                     "rolename": role_name,
                     "permissions": permissions
                     }
        response = self.sw.http_post(self.path, post_data=post_data, v2_path=True)
        return response

    def delete(self, role_name):
        """Delete a role
        Args:
            role_name (str): name of role to delete
        Returns:
            (Dict):
            Example
            {
            'message': 'Deleted auditor',
             }
        """
        params = {"rest_token": self.sw.rest_token,
                  "rolename": role_name
                  }
        response = self.sw.http_delete(self.path, params=params, v2_path=True)
        return response

    def list(self):
        """Lists roles
        Returns:
            (list of dict): list of triggers and their information
            [
                {
                    "rolename": "Admin",
                    "Groups": true,
                    "Licensing": true,
                    "Authentication": true,
                    "Authorization": true,
                    "Auditing": true,
                    "Search": true,
                    "Policy": true
                }, {
                    "rolename": "Guest",
                    "Groups": false,
                    "Licensing": false,
                    "Authentication": false,
                    "Authorization": false,
                    "Auditing": false,
                    "Search": false,
                    "Policy": false
                },
                ...
            ]
        """
        params = {"rest_token": self.sw.rest_token}
        list_of_triggers = self.sw.http_get(self.path, params=params, v2_path=True)
        return list_of_triggers

    add = create


class Authorization(EndpointHandler):
    path = "/authorization"

    def __init__(self, sw):
        """Authorization handler
        """
        self.roles = Roles(sw)
        super(Authorization, self).__init__(sw, self.path)
