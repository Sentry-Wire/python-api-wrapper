from __future__ import unicode_literals

import pytest
from os import getenv
from sentrywire.exceptions import *

from sentrywire.client import Sentrywire

class TestPolicySuccesses:

    def test_export_policy(self):

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.federation.policies.export()
        sw.disable_debug()

        print(response)
        assert "message" in response
        assert response["message"] == "FM policy exported"


class TestPoliciesAuthenticationFailure:

    def test_export_policy_invalid_authentication(self):

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False, rest_token="bad")

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            response = sw.federation.policies.export()
        sw.disable_debug()


    def test_export_policy_null_authentication(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            response = sw.federation.policies.export()
        sw.disable_debug()


class TestGroupSuccess:

    def test_create_group(self):
        group_name = "test_group_create"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.federation.groups.create(group_name)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response["message"] == "added group " + group_name

    def test_delete_group(self):
        group_name = "test_group_create"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.federation.groups.delete(group_name)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass
        print(response)
        assert response["message"] == "deleted group  " + group_name

    def test_list_groups(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.federation.groups.list()
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, list)
        assert response[0]["groupname"]


class TestGroupFailures:

    def test_create_group_invalid_auth(self):
        group_name = "create_invalid_auth"
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.federation.groups.create(group_name)
        sw.disable_debug()

    def test_create_group_null_auth(self):
        group_name = "create_null_auth"
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.federation.groups.create(group_name)
        sw.disable_debug()

    def test_delete_group_invalid_auth(self):
        group_name = "delete_invalid_auth"
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.federation.groups.delete(group_name)
        sw.disable_debug()

    def test_delete_group_null_auth(self):
        group_name = "delete_null_auth"
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.federation.groups.delete(group_name)
        sw.disable_debug()

    def test_list_group_invalid_auth(self):
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.federation.groups.list()
        sw.disable_debug()

    def test_list_group_null_auth(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.federation.groups.list()
        sw.disable_debug()


@pytest.mark.skipif(not getenv("SECOND_NODE_IP"), reason="Second node undefined")
class TestNodeSuccess:

    def test_create_node(self):
        if not getenv("SECOND_NODE_IP"):
            raise Exception("SECOND_NODE_IP environment variable not found")

        group_name = "test_node_group"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        try:
            response = sw.federation.groups.list()
            found = False
            for group in response:
                if group["groupname"] == group_name:
                    found = True
                    break
            if not found:
                sw.federation.groups.create(group_name)
        except Exception as e:
            raise Exception("Could not create group for new node " + str(e))

        sw.enable_debug()
        response = sw.federation.nodes.create(getenv("SECOND_NODE_IP"), group_name)
        sw.disable_debug()

        sw.authentication.logout()

        print(response)
        assert isinstance(response, dict)
        assert response[0]["nodename"]

    def test_delete_node(self):
        if not getenv("SECOND_NODE_IP"):
            raise Exception("SECOND_NODE_IP environment variable not found")

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.federation.nodes.delete(getenv("SECOND_NODE_IP"))
        sw.disable_debug()

        sw.authentication.logout()

        print(response)
        assert isinstance(response, dict)
        assert response[0]["DeleteNode"]
