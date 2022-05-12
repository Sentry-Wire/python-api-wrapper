from __future__ import unicode_literals

from os import getenv

import pytest

from sentrywire.client import Sentrywire
from sentrywire.exceptions import *


class TestRoleSuccess:

    def test_create_role(self):
        role_name = "test_role_create"
        permissions = "Groups,Licensing,Authentication,Authorization,Auditing,Search,Policy"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.authorization.roles.create(role_name, permissions)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response["message"] == "added role " + role_name

    def test_delete_role(self):
        role_name = "test_role_create"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        # Assume that the previous function succeeded, and delete the new role
        sw.enable_debug()
        response = sw.authorization.roles.delete(role_name)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response["message"] == "deleted role " + role_name

    def test_list_role(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.authorization.roles.list()
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, list)
        assert response[0]["rolename"]


class TestRoleFailures:

    def test_create_role_invalid_auth(self):
        group_name = "create_invalid_auth"
        permissions = "Groups,Licensing,Authentication,Authorization,Auditing,Search,Policy"

        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.authorization.roles.create(group_name, permissions)
        sw.disable_debug()

    def test_create_role_null_auth(self):
        group_name = "create_null_auth"
        permissions = "Groups,Licensing,Authentication,Authorization,Auditing,Search,Policy"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.authorization.roles.create(group_name, permissions)
        sw.disable_debug()

    def test_delete_role_invalid_auth(self):
        group_name = "delete_invalid_auth"
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.authorization.roles.delete(group_name)
        sw.disable_debug()

    def test_delete_role_null_auth(self):
        group_name = "delete_null_auth"
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.authorization.roles.delete(group_name)
        sw.disable_debug()

    def test_list_role_invalid_auth(self):
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.authorization.roles.list()
        sw.disable_debug()

    def test_list_role_null_auth(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.authorization.roles.list()
        sw.disable_debug()
