from __future__ import unicode_literals

import pytest
from os import getenv
from sentrywire.exceptions import *

from sentrywire.client import Sentrywire


class TestAuthenticationSuccess:

    def test_login_success(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.enable_debug()
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))
        sw.disable_debug()
        try:
            sw.authentication.logout()
        except:
            pass

    def test_logout_success(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        token = sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))
        sw.enable_debug()
        sw.authentication.logout()
        sw.disable_debug()

        sw = Sentrywire(getenv("TARGET"), rest_token=token, ssl_verify=False)
        with pytest.raises(InvalidAuthentication):
            sw.server.status()

    def test_manual_token_success(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        token = sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw1 = Sentrywire(getenv("TARGET"), rest_token=token, ssl_verify=False)
        try:
            sw1.enable_debug()
            sw1.logout()
            sw1.disable_debug()
        except:
            pass
        try:
            sw.authentication.logout()
        except:
            pass


class TestAuthenticationLoginFailure:

    def test_login_invalid_credentials(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.authentication.login("bad", "bad")
        sw.disable_debug()

    def test_login_null_username(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.authentication.login(None, "bad")
        sw.disable_debug()

    def test_login_blank_username(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.authentication.login("", "bad")
        sw.disable_debug()

    def test_login_null_password(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.authentication.login("bad", None)
        sw.disable_debug()

    def test_login_blank_password(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.enable_debug()
        with pytest.raises(InvalidParameters):
            sw.authentication.login("bad", "")
        sw.disable_debug()


class TestAuthenticationLogoutFailure:

    def test_logout_invalid_token(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.enable_debug()
        with pytest.raises(SentrywireException):
            sw.authentication.logout(rest_token="bad")
        sw.disable_debug()

    def test_logout_null_token(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.enable_debug()
        with pytest.raises(SentrywireException):
            sw.authentication.logout(rest_token=None)
        sw.disable_debug()

    def test_logout_blank_token(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.enable_debug()
        with pytest.raises(SentrywireException):
            sw.authentication.logout(rest_token="")
        sw.disable_debug()