from __future__ import unicode_literals

import os.path
import time
import zipfile
from datetime import datetime, timedelta
from os import getenv
from scapy.all import rdpcap

import pytest

from sentrywire.const import TIMEOUT
from sentrywire.client import Sentrywire
from sentrywire.exceptions import *
from sentrywire.tests import DOWNLOADS_FOLDER


class TestSearchSuccess:

    def test_new_search(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))
        sw.enable_debug()
        response = sw.searches.create("test_new_search",
                                      datetime.now() - timedelta(minutes=45),
                                      datetime.now() - timedelta(minutes=30),
                                      search_filter="tcp or udp",
                                      max_packets=100
                                      )
        sw.disable_debug()
        print(response)
        assert response["searchname"] is not None
        try:
            sw.searches.delete(response["searchname"])
        except:
            pass

        try:
            sw.authentication.logout()
        except:
            pass

    def test_delete_search(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))
        response = sw.searches.create("test_delete_search",
                                      datetime.now() - timedelta(minutes=45),
                                      datetime.now() - timedelta(minutes=30),
                                      search_filter="tcp or udp",
                                      max_packets=100
                                      )

        time.sleep(3)

        sw.enable_debug()
        sw.searches.delete(response["searchname"])
        sw.disable_debug()
        try:
            sw.searches.status(getenv("NODE_NAME"), response["searchname"])
            print("Could not validate that search was deleted.")
        except:
            pass

        try:
            sw.authentication.logout()
        except:
            pass

    def test_search_status_pending(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))
        response = sw.searches.create("test_search_status_pending",
                                      datetime.now() - timedelta(minutes=45),
                                      datetime.now() - timedelta(minutes=30),
                                      search_filter="tcp or udp",
                                      max_packets=100
                                      )
        time.sleep(5)
        sw.enable_debug()
        response = sw.searches.status(getenv("NODE_NAME"),  response["searchname"])
        sw.disable_debug()
        print(response)
        assert isinstance(response, dict)
        assert response["SearchStatus"] == "Pending"
        try:
            sw.searches.delete(response["searchname"])
        except:
            pass
        try:
            sw.authentication.logout()
        except:
            pass

    #@pytest.mark.skip(reason="Test not implemented")
    def test_get_pcap_list(self):
        start_time = time.time()
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))
        response = sw.searches.create("test_get_pcap_list",
                                      datetime.now() - timedelta(minutes=45),
                                      datetime.now() - timedelta(minutes=30),
                                      search_filter="tcp or udp",
                                      max_packets=100
                                      )
        search_token = response["searchname"]
        while True:
            response = sw.searches.status(getenv("NODE_NAME"), search_token)
            if "SearchStatus" in response:
                current_time = time.time()
                time_delta = current_time - start_time
                if time_delta > TIMEOUT:
                    assert 0, "Timed out"
                time.sleep(5)
            elif "SearchResult" in response:
                break
            else:
                raise Exception("Unexpected search state: " + str(response))

        sw.enable_debug()
        response = sw.searches.pcaps.list(getenv("NODE_NAME"), search_token)
        sw.disable_debug()

        print(response)

        assert response

        try:
            assert not response["msg"]
        except ValueError as e:
            raise e

        assert isinstance(response, list)

        try:
            sw.searches.delete(search_token)
        except:
            pass
        try:
            sw.authentication.logout()
        except:
            pass

    def test_get_pcap(self):
        file_name = DOWNLOADS_FOLDER + "get_pcap.zip"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))
        response = sw.searches.create("test_get_pcap",
                                      datetime.now() - timedelta(minutes=45),
                                      datetime.now() - timedelta(minutes=30),
                                      search_filter="tcp or udp",
                                      max_packets=100
                                      )
        search_token = "continuum_1645157014_124_test_get_pcap"#response["searchname"]
        while True:
            response = sw.searches.status(getenv("NODE_NAME"), search_token)
            if "SearchStatus" in response:
                time.sleep(5)
            elif "SearchResult" in response:
                break
            else:
                raise Exception("Unexpected search state: " + str(response))

        sw.enable_debug()
        response = sw.searches.pcaps.get(getenv("NODE_NAME"), search_token, 1, file_name)
        print(response)
        sw.disable_debug()

        try:
            sw.searches.delete(search_token)
        except:
            pass
        try:
            sw.authentication.logout()
        except:
            pass

        assert os.path.exists(file_name)

        try:  # Plenty of things can go wrong here
            with zipfile.ZipFile(file_name, "r") as zip_file:
                # Get a list of all archived file names from the zip
                file_names = zip_file.namelist()
                # Iterate over the file names
                for file_ in file_names:
                    # Check filename endswith csv
                    if file_.endswith('.pcap'):
                        # Extract a single file from zip
                        print(file_)
                        zip_file.extract(file_, DOWNLOADS_FOLDER + os.path.splitext(os.path.basename(file_name))[0])
        except Exception as e:
            assert 0, "Error unzipping file: " + str(e)

        for file_ in file_names:
            try:
                cap = rdpcap(DOWNLOADS_FOLDER + os.path.splitext(os.path.basename(file_name))[0] + "/" + file_)
                if len(cap) < 1:
                    assert 0, "Zero length pcap: " + file_
            except Exception as e:
                if str(e) == "No data could be read!":
                    assert 0, "Error reading pcap. Does the server have any traffic?"
                assert 0, "Error reading pcap: " + str(e)

    def test_list_pending_searches(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        # Ensure that something is pending
        response = sw.searches.create("test_get_pending",
                                      datetime.now() - timedelta(minutes=45),
                                      datetime.now() - timedelta(minutes=30),
                                      search_filter="tcp or udp",
                                      max_packets=1000
                                      )
        search_token = response["searchname"]

        sw.enable_debug()
        response = sw.searches.pending()
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, list)
        assert len(response) > 0
        assert response[0]["SearchKey"]

    def test_list_completed_searches(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

        sw.enable_debug()
        response = sw.searches.completed()
        sw.disable_debug()

        try:
            sw.authentication.logout()
        except:
            pass

        print(response)
        assert isinstance(response, list)
        assert len(response) > 0
        assert response[0]["SearchKey"]

    @pytest.mark.skip(reason="Test not implemented")
    def test_get_log_data(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="Test not implemented")
    def test_get_object_list(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="Test not implemented")
    def test_get_object_data(self):
        raise NotImplementedError


class TestSearchFailures:

    def test_new_search_invalid_auth(self):
        sw = Sentrywire(getenv("TARGET"), rest_token="bad", ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.searches.create("test_new_search_invalid_auth",
                               datetime.now() - timedelta(minutes=45),
                               datetime.now() - timedelta(minutes=30),
                               search_filter="tcp or udp",
                               max_packets=100
                               )
        sw.disable_debug()

    def test_new_search_null_auth(self):
        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)

        sw.enable_debug()
        with pytest.raises(InvalidAuthentication):
            sw.searches.create("test_new_search_no_auth",
                               datetime.now() - timedelta(minutes=45),
                               datetime.now() - timedelta(minutes=30),
                               search_filter="tcp or udp",
                               max_packets=100
                               )
        sw.disable_debug()


class TestLogsSuccess:

    def test_get_logs_success(self):
        start_time = time.time()
        file_name = DOWNLOADS_FOLDER + "get_logs.zip"

        sw = Sentrywire(getenv("TARGET"), ssl_verify=False)
        sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))
        response = sw.searches.create("test_get_log_data",
                                      datetime.now() - timedelta(minutes=45),
                                      datetime.now() - timedelta(minutes=30),
                                      search_filter="logsearch",
                                      max_packets=100
                                      )
        search_token = response["searchname"]
        while True:
            response = sw.searches.status(getenv("NODE_NAME"), search_token)
            if "SearchStatus" in response:
                current_time = time.time()
                time_delta = current_time - start_time
                if time_delta > TIMEOUT:
                    assert 0, "Timed out"
                time.sleep(5)
            elif "SearchResult" in response:
                break
            else:
                raise Exception("Unexpected search state: " + str(response))

        sw.enable_debug()
        response = sw.logs.get(getenv("NODE_NAME"), search_token, file_name)
        print(response)
        sw.disable_debug()

        assert os.path.exists(file_name)

        # try:
        #     sw.searches.delete(search_token)
        # except:
        #     pass

        try:
            sw.authentication.logout()
        except:
            pass

        try:  # Plenty of things can go wrong here
            with zipfile.ZipFile(file_name, "r") as zip_file:
                # Get a list of all archived file names from the zip
                file_names = zip_file.namelist()
                # Iterate over the file names
                for file_ in file_names:
                    zip_file.extract(file_, DOWNLOADS_FOLDER + os.path.splitext(os.path.basename(file_name))[0])
        except Exception as e:
            assert 0, "Error unzipping file: " + str(e)

        for file_ in file_names[1:]:
            try:
                file_handler = open(DOWNLOADS_FOLDER + "get_logs/" + file_, 'r')
                print(file_handler.read(200))
                # if len(dat) < 1:
                #     assert 0, "Zero length data: " + file_
            except Exception as e:
                assert 0, "Error reading data: " + str(e)
