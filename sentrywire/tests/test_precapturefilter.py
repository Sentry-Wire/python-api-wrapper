from __future__ import unicode_literals

import time
from os import getenv

import pytest

from sentrywire.client import Sentrywire
from sentrywire.exceptions import *


class TestSearchPrecaptureFilterSuccess:

    def test_create_precapture_filter(self):
        search_filter = "port 66"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.precapturefilter.create(search_filter)
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response["message"] == " pre-capture filter set "

    def test_delete_precapture_filter(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.precapturefilter.delete()
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response["message"] == "pre-capture filter reset"

    def test_list_precapture_filter(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.precapturefilter.list()
        sw.disable_debug()

        if not response:
            print("No filters in capture, adding some to verify output")
            search_filter = "port 66"
            sw.precapturefilter.create(search_filter)
            time.sleep(5)
            sw.enable_debug()
            response = sw.precapturefilter.list()
            sw.disable_debug()
            sw.precapturefilter.delete()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert response[0]["filtername"]
        assert response[0]["searchfilter"]
        assert response[0]["createdtime"]


class TestPrecaptureFilterFailures:

    def test_create_precapture_filter_invalid_auth(self):
        search_filter = "port 66"

        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.precapturefilter.create(search_filter)
        sw.disable_debug()

    def test_create_precapture_filter_null_auth(self):
        search_filter = "port 66"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.precapturefilter.create(search_filter)
        sw.disable_debug()

    def test_delete_precapture_filter_invalid_auth(self):
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.precapturefilter.delete()
        sw.disable_debug()

    def test_delete_precapture_filter_null_auth(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.precapturefilter.delete()
        sw.disable_debug()

    def test_list_precapture_filter_invalid_auth(self):
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.precapturefilter.list()
        sw.disable_debug()

    def test_list_precapture_filter_null_auth(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.precapturefilter.list()
        sw.disable_debug()
