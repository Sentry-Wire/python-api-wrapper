from __future__ import unicode_literals

import time
from os import getenv

import pytest

from sentrywire.client import Sentrywire
from sentrywire.exceptions import *


class TestSearchActiveTriggersSuccess:

    def test_create_active_trigger(self):
        trigger_name = "test_trigger_create"
        trigger_token = getenv("SW_USERNAME") + "_" + trigger_name
        search_filter = "port 66"
        seconds_before = 60
        seconds_after = 60

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        # we are not testing delete, but we need it to not exist first
        try:
            sw.activetriggers.delete(trigger_token)
            time.sleep(5)
        except:
            pass

        sw.enable_debug()
        response = sw.activetriggers.create(trigger_name, search_filter, seconds_before, seconds_after)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response["currTriggerCount"]
        assert response["maxTriggerCount:"]

    def test_list_active_triggers_individual(self):
        trigger_name = "test_trigger_list"
        trigger_token = getenv("SW_USERNAME") + "_" + trigger_name

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.activetriggers.list(trigger_name=trigger_token)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response[0]["trigger_name"]
        assert response[0]["search_filter"]
        assert response[0]["seconds_before"]
        assert response[0]["seconds_after"]
        # assert response[0]["created_time"]

    def test_delete_active_trigger(self):
        trigger_name = "test_trigger_delete"
        trigger_token = getenv("SW_USERNAME") + "_" + trigger_name

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.activetriggers.delete(trigger_token)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response["message"] == "deleted active trigger " + trigger_token

    def test_list_active_triggers(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.activetriggers.list()
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response[0]["trigger_name"]
        assert response[0]["search_filter"]
        assert response[0]["seconds_before"]
        assert response[0]["seconds_after"]
        # assert response[0]["createdtime"]


class TestActiveTriggerFailures:

    def test_create_at_invalid_auth(self):
        trigger_name = "create_invalid_auth"
        search_filter = "port 66"
        seconds_before = 60
        seconds_after = 60

        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.activetriggers.create(trigger_name, search_filter, seconds_before, seconds_after)
        sw.disable_debug()

    def test_create_at_null_auth(self):
        trigger_name = "create_null_auth"
        search_filter = "port 66"
        seconds_before = 60
        seconds_after = 60

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.activetriggers.create(trigger_name, search_filter, seconds_before, seconds_after)
        sw.disable_debug()

    def test_delete_at_invalid_auth(self):
        trigger_name = "delete_invalid_auth"
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.activetriggers.delete(trigger_name)
        sw.disable_debug()

    def test_delete_at_null_auth(self):
        trigger_name = "delete_null_auth"
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.activetriggers.delete(trigger_name)
        sw.disable_debug()

    def test_list_at_invalid_auth(self):
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.activetriggers.list()
        sw.disable_debug()

    def test_list_at_null_auth(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.activetriggers.list()
        sw.disable_debug()
