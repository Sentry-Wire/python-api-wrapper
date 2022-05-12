from __future__ import unicode_literals

import time
from os import getenv

import pytest

from sentrywire.client import Sentrywire
from sentrywire.tests import TEST_DATA_FOLDER, DOWNLOADS_FOLDER


class TestIDSRulesSuccess:

    def test_create_ids_rule(self):
        import os
        print(os.getcwd())
        rule_set_name = "valid_rule_set.rules"
        rule_set_path = TEST_DATA_FOLDER + rule_set_name

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.idsrules.create(rule_set_path)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, dict)
        assert response["uploaded"] == rule_set_name

    def test_activate_ids_rule(self):
        rule_set = "valid_rule_set.rules"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.idsrules.activate(rule_set)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, dict)
        assert response["message"] == "activated " + rule_set

    def test_deactivate_ids_rule(self):
        rule_set = "valid_rule_set.rules"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.idsrules.deactivate(rule_set)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, dict)
        assert response["message"]

    def test_download_ids_rule(self):
        rule_set = "valid_rule_set.rules"
        file_path = DOWNLOADS_FOLDER + "ids_rule_download.rules"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.idsrules.get(rule_set, file_path)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response
        assert response[:5] == b"alert"

    def test_delete_ids_rule(self):
        rule_set = "valid_rule_set.rules"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.idsrules.delete(rule_set)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, dict)
        assert response["message"] == " deleted ruleset " + rule_set

    def test_list_activated_ids_rules(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.idsrules.list("activated")
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, list)

    def test_list_deactivated_ids_rules(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.idsrules.list("deactivated")
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, list)


