import io
import zipfile
from json import loads

from sentrywire.exceptions import SentrywireException, NotFound
from sentrywire.base import EndpointHandler


class Search(EndpointHandler):
    path = "/fmsearch"

    def __init__(self, sw):
        """HTTP POST request to the /v2/fmsearch endpoint to start a new search.
        """
        self.objects = Objects(sw)
        self.pcaps = Pcaps(sw)
        self.logs = Logs(sw)
        super(Search, self).__init__(sw, self.path)

    def create(self, search_name, begin_time, end_time, search_filter=None, max_packets=1000):
        """Create new rest token for current client
        Args:
            search_name (str): Username for Sentrywire system
            search_filter (str): Optional - Default: tcp or udp
                                    bpf <bpffilter> logtext <logsearchfilter> payload <payloadfilter> extends bpf
                                    <bpffilter> logtext <logsearchfilter> payload
                                    logtext is optional. If specified, gets only entries that have the logsearchfilter.
                                    Otherwise, gets all the alert/dpi data of the search.
                                    payload is optional. If specified, gets only those packets that satisfy bpffilter AND
                                    have the payload specified by payloadfilter.  Otherwise, gets all packets that satisfy
                                    bpffilter
                                    extends is optional. This allows multiple independent search filters to be combined
                                    Examples:
                                    bpf tcp or udp logtext example.com payload HTTP
                                    tcp or udp logtext example.com
                                    port 80 payload example.com
                                    host 1.2.3.4 and port 110
                                    port 80 payload example.com extends port 53 payload abcd
            begin_time (datetime.datetime): Search for packets after begin_time
            end_time (datetime.datetime): Search for packets before end_time
            max_packets (int): maximum number of packets to include in results
        Returns:
            (Dict): json response as a python dictionary
            Example:
                {
                  "searchname": "continuum_1631377579_1_rest2"
                }
        """
        post_data = {
            "rest_token": self.sw.rest_token,
            "search_name": search_name,
            "search_filter": search_filter,
            "begin_time": begin_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "max_packets": max_packets
        }

        response = self.sw.http_post(self.path, post_data=post_data)
        return response

    def cancel(self, search_token):
        """Cancel a search in progress
        Args:
            search_token (str): search token to cancel
        """
        pass

    def delete(self, search_token):
        """delete a search
        Args:
            search_token (str): search token
        Returns:
            (Dict):
            Example
            {
            'message': 'continuum_1635031643_10_test_createsw152 Deleted',
             }
        """
        params = {"rest_token": self.sw.rest_token,
                  "searchname": search_token}
        response = self.sw.http_get(self.path, params=params)
        return response

    def status(self, node_name, search_name):
        """Get the status of a search
        Args:
            search_name (str): search token
            node_name (str): node to retrieve search from
        Returns:
            (list of dict): List of searches and their information
            Example
            [
              {
                "PayloadSearchFilter": "",
                "CaseName": "fms_2020_11_27_22_04_07_797",
                "SearchName": "fms_2020_11_27_22_04_07_797",
                "Begintime": "2020-11-12 02:49:07",
                "Endtime": "2020-11-28 03:04:07",
                "SearchFilter": "PcapData,host 100.100.100.100",
                "LogSearchFilter": "",
                "SearchStatus": "Pending"
              }
        """
        params = {"rest_token": self.sw.rest_token,
                  "searchname": search_name,
                  "nodename": node_name}
        response = self.sw.http_get(self.path + "/status", params=params)
        return response

    def pending(self, count=0):
        """Get the list of pending searches
        Args:
            count (int): Optional, limit the number of pending searches returned to this number. Returns all by default
        Returns:
            (list of dict): List of searches and their information
            Example
            [
              {
                "PayloadSearchFilter": "",
                "CaseName": "fms_2020_11_27_22_04_07_797",
                "SearchName": "fms_2020_11_27_22_04_07_797",
                "Begintime": "2020-11-12 02:49:07",
                "Endtime": "2020-11-28 03:04:07",
                "SearchFilter": "PcapData,host 100.100.100.100",
                "LogSearchFilter": "",
                "SearchStatus": "Pending"
              },
              {
                "PayloadSearchFilter": "",
                "CaseName": "fms_2020_11_27_22_05_20_646",
                "SearchName": "fms_2020_11_27_22_05_20_646",
                "Begintime": "2020-11-12 02:50:20",
                "Endtime": "2020-11-28 03:05:20",
                "SearchFilter": "PcapData,host 100.100.100.100",
                "LogSearchFilter": "",
                "SearchStatus": "Pending"
              },
              ...
        """
        params = {"rest_token": self.sw.rest_token,
                  "count": count}
        response = self.sw.http_get(self.path + "/pending", params=params)
        if not response:
            raise NotFound("No pending searches found")
        return response

    def completed(self, count=0):
        """Get the status of a search
        Args:
            count (int): Optional, limit the number of pending searches returned to this number. Returns all by default
        Returns:
            (list of dict): List of searches and their information
            Example
            [
                {
                    'SearchKey': 'continuum_1635109402_72_test_get_pcap_listsw152',
                    'MasterToken': '',
                    'SearchPorts': '',
                    'CaseName': 'continuum_1635109402_72_test_get_pcap_list',
                    'SearchName': 'continuum_1635109402_72_test_get_pcap_list',
                    'SubmittedTime': '1635109416091',
                    'Begintime': '2021-10-24 16:18:14',
                    'Endtime': '2021-10-24 16:33:14',
                    'SearchFilter': 'PcapData,tcp or udp',
                    'MaxPacketCount': '100',
                    'SearchResult': '',
                    'MaxChunk': '0',
                    'NodeName': 'sw152'
                },
                ...
            ]
              ...
        """
        params = {"rest_token": self.sw.rest_token,
                  "count": count}
        response = self.sw.http_get(self.path + "/completed", params=params)
        return response


class Objects(EndpointHandler):
    path = "/fmsearch/data"

    def __init__(self, sw):
        """Search objects function handler
        """
        super(Objects, self).__init__(sw, self.path)

    def list(self,  node_name, search_token, file_path):
        """Get the object list from a search
        Args:
            search_token (str): search token
            node_name (str): node to retrieve search from
            file_path (str): path to zip file destination
        Returns:
            (None): Downloads file to file_path
        """
        file_handler = open(file_path, 'wb+')

        params = {
            "rest_token": self.sw.rest_token,
            "searchname": search_token,
            "type": "ObjectList",
            "nodename": node_name
        }

        response = self.sw.http_get(self.path, params=params)

        if isinstance(response, dict):
            file_handler.close()
            return response

        file_handler.write(response.content)
        file_handler.close()

    def get(self,  node_name, search_token, file_path):
        """Get the object list from a search
        Args:
            search_token (str): search token
            node_name (str): node to retrieve search from
            file_path (str): path to zip file destination
        Returns:
            (None): Downloads file to file_path
        """
        file_handler = open(file_path, 'wb+')

        params = {
            "rest_token": self.sw.rest_token,
            "searchname": search_token,
            "type": "SearchObjects",
            "nodename": node_name
        }

        response = self.sw.http_get(self.path, params=params)

        if isinstance(response, dict):
            file_handler.close()
            return response

        file_handler.write(response.content)
        file_handler.close()


class Pcaps(EndpointHandler):
    path = "/fmsearch/data"

    def __init__(self, sw):
        """Search pcaps function handler
        """
        super(Pcaps, self).__init__(sw, self.path)

    def list(self, node_name, search_token):
        """list pcaps in search
        Args:
            search_token (str): search token
            node_name (str): node from which to retrieve search data
        """
        params = {
            "rest_token": self.sw.rest_token,
            "searchname": search_token,
            "type": "PcapList",
            "nodename": node_name
        }

        response = self.sw.http_get(self.path, params=params)

        try:
            json_response = response.json()
            if "Exist" in json_response["msg"]:
                raise NotFound("No PCAPs found")
            return json_response
        except NotFound as e:
            raise e
        except:
            pass

        # This should not be a permanent inclusion, but for now it is.
        try:  # Plenty of things can go wrong here
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                for filename in zip_file.namelist():
                    if filename == "chunklist.json":
                        # read the file
                        with zip_file.open(filename) as f:
                            return loads(f.read())
        except:
            raise SentrywireException("Error in server response")

    def get(self, node_name, search_name, index, file_path):
        file_handler = open(file_path, 'wb+')

        params = {
            "rest_token": self.sw.rest_token,
            "searchname": search_name,
            "type": index,
            "nodename": node_name
        }

        response = self.sw.http_get(self.path, params=params)

        if not response:
            raise NotFound("PCAP not found")

        if isinstance(response, dict):
            file_handler.close()
            return response

        file_handler.write(response.content)
        file_handler.close()


class Logs(EndpointHandler):
    path = "/fmsearch/data"

    def __init__(self, sw):
        """HTTP POST request to the /v2/fmsearch/data endpoint to get log results in a search.
        """
        super(Logs, self).__init__(sw, self.path)

    def get(self, node_name, search_name, file_path):
        """Create new rest token for current client
        Args:
            search_name (str): Name of the search to retrieve logs from
            node_name (str): Name of node to retrieve logs from
            file_path (str): Path to put downloaded file
        Returns:
            (Dict): json response as a python dictionary
            Example:
                {
                  "searchname": "continuum_1631377579_1_rest2"
                }
        """
        file_handler = open(file_path, 'wb+')

        params = {
            "rest_token": self.sw.rest_token,
            "searchname": search_name,
            "type": "LogData",
            "nodename": node_name
        }

        response = self.sw.http_get(self.path, params=params)

        if "Exist" in response:
            file_handler.close()
            raise NotFound("Log not found")

        if isinstance(response, dict):
            file_handler.close()
            return response

        file_handler.write(response.content)
        file_handler.close()
