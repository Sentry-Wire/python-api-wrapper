from __future__ import unicode_literals

import time

import pytest
from os import getenv
from sentrywire.exceptions import *

from sentrywire.client import Sentrywire


class TestServerStatusSuccess:

    def test_server_status(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.server.status()
        sw.disable_debug()

        print(response)
        # assert isinstance(response, list)
        assert response["ServerInfo"]["NodeName"] == getenv("NODE_NAME")
        try:
            sw.authentication.logout()
        except:
            pass


class TestServerCaptureSuccess:
    def test_server_stop_capture(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.server.capture.stop()
        sw.disable_debug()

        print(response)
        assert isinstance(response, dict)
        assert response["message"] == "pause request submitted"

        # time.sleep(60)
        # response = sw.server.status()
        # for server in response:
        #     if server["nodename"] == getenv("NODE_NAME"):
        #         assert server["status"] == "Stopped"

        try:
            sw.authentication.logout()
        except:
            pass

    def test_server_start_capture(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        # response = sw.server.status()
        # for server in response:
        #     if server["nodename"] == getenv("NODE_NAME"):
        #         if server["status"] == "Running":
        #             sw.server.capture.stop()
        #             time.sleep(5)

        sw.enable_debug()
        response = sw.server.capture.start()
        sw.disable_debug()

        print(response)
        assert isinstance(response, dict)
        assert response["message"] == "resume request submitted"

        # time.sleep(60)
        # response = sw.server.status()
        # for server in response:
        #     if server["nodename"] == getenv("NODE_NAME"):
        #         assert server["status"] == "Running"

        try:
            sw.authentication.logout()
        except:
            pass


class TestServerStatusFailures:

    def test_server_status_invalid_auth(self):
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.server.status()
        sw.disable_debug()

    def test_server_status_null_auth(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.server.status()
        sw.disable_debug()


class TestServerCaptureFailures:

    def test_stop_capture_invalid_auth(self):
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.server.capture.stop()
        sw.disable_debug()

    def test_stop_capture_no_auth(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.server.capture.stop()
        sw.disable_debug()

    def test_start_capture_invalid_auth(self):
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.server.capture.start()
        sw.disable_debug()

    def test_start_capture_no_auth(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.server.capture.start()
        sw.disable_debug()
