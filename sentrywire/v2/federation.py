from sentrywire.base import EndpointHandler


class Policy(EndpointHandler):
    path = "/exportpolicy"

    def __init__(self, sw):
        """Policy handler
        """
        super(Policy, self).__init__(sw, self.path)

    def export(self):
        """This is a HTTP POST request to the server’s /v2/exportpolicy endpoint to save FM policy info such as list
of users, groups, nodes. This can be forwarded to federated nodes so that any such node is ready to be
designated HA node.

        Returns:
            (Dict):
            Example
            {
                "message": "FM policy exported",
            }
        """
        post_data = {"rest_token": self.sw.rest_token
                     }
        response = self.sw.http_post(self.path, post_data=post_data)
        return response


class Nodes(EndpointHandler):
    path = "/fmnode"

    def __init__(self, sw):
        """Node handler
        """
        super(Nodes, self).__init__(sw, self.path)

    def create(self, node_address, group_name):
        """Create a node
        Args:
            node_address (str): location of new node
            group_name (str): existing group to add node to
        Returns:
            (Dict):
            Example
            {
                'nodename': 'nc198',
            }
        """
        post_data = {"rest_token": self.sw.rest_token,
                     "nodeaddr": node_address,
                     "group_name": group_name
                     }
        response = self.sw.http_post(self.path, post_data=post_data).json()
        return response

    def delete(self, node_address):
        """Delete a node
        Args:
            node_address (str): location of node to be deleted
        Returns:
            (Dict):
            Example
            {
                "DeleteNode": "10.91.170.161"
            }
        """
        params = {"rest_token": self.sw.rest_token,
                  "nodeaddr": node_address
                  }
        response = self.sw.http_delete(self.path, params=params).json()
        return response

    add = create


class Groups(EndpointHandler):
    path = "/fmgroup"

    def __init__(self, sw):
        """Group handler
        """
        super(Groups, self).__init__(sw, self.path)

    def create(self, group_name):
        """Create a group
        Args:
            group_name (str): name of role to delete
        Returns:
            (Dict):
            Example
            {
                'message': 'group added',
            }
        """
        post_data = {"rest_token": self.sw.rest_token,
                     "group_name": group_name
                     }
        response = self.sw.http_post(self.path, post_data=post_data).json()
        return response

    def delete(self, group_name):
        """Delete a group
        Args:
            group_name (str): name of role to delete
        Returns:
            (Dict):
            Example
            {
                'message': 'Deleted auditor',
            }
        """
        params = {"rest_token": self.sw.rest_token,
                  "group_name": group_name
                  }
        response = self.sw.http_delete(self.path, params=params).json()
        return response

    def list(self):
        """List groups
        Returns:
            (list of dict):
            Example
            [
              {
                "GroupName": "Boston"
              },
              {
                "GroupName": "Nashua"
              },
              {
                "GroupName": "Concord"
              }
            ]
        """
        params = {"rest_token": self.sw.rest_token}
        response = self.sw.http_get(self.path, params=params)
        return response


class Federation(EndpointHandler):
    """
    A logical class to group the "group" and "node" endpoints
    """
    path = "/"

    def __init__(self, sw):
        """Federation function handler
        """
        self.groups = Groups(sw)
        self.nodes = Nodes(sw)
        self.policies = Policy(sw)
        super(Federation, self).__init__(sw, self.path)
