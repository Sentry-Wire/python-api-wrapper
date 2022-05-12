from sentrywire.base import EndpointHandler
from json import loads


class Capture(EndpointHandler):
    path = "/fmcapture"

    def __init__(self, sw):
        """Packet capture handler
        """
        super(Capture, self).__init__(sw, self.path)

    def stop(self):
        """Stop the server from capturing packets
        Returns:
            (dict): status in message, if it does not throw an exception it is fine
            {
              "message": "pause request submitted"
            }
        """
        params = {"rest_token": self.sw.rest_token,
                  "action": "pause"}
        json = self.sw.http_put(self.path, params=params)
        return json

    def start(self):
        """Start capturing packets on the server
        Returns:
            (dict): status in message, if it does not throw an exception it is fine
            {
              "message": "resume request submitted"
            }
        """
        params = {"rest_token": self.sw.rest_token,
                  "action": "resume"}
        json = self.sw.http_put(self.path, params=params)
        return json

    # Aliases to newest version of documentation.
    pause = stop
    resume = start


class Server(EndpointHandler):
    path = "/fmping"

    def __init__(self, sw):
        """Server status function handler
        """
        self.capture = Capture(sw)
        super(Server, self).__init__(sw, self.path)

    def status(self):
        """Get server status
        Returns:
            dict: Server status dump
            {
                'ServerInfo': {
                    'NodeName': 'sw138',
                    'NodeIP': '127.0.0.1',
                    'Upordown': '1',
                    'Port': '[0:10 Gbps  1:Down  ]',
                    'Status': 'Running',
                    'Duration': '00:22:52:00',
                    'BeginTime': '2022-02-15 18:39:00',
                    'EndTime': '2022-02-16 17:31:00',
                    'License': 'Evaluation',
                    'TimeZone': 'UTC',
                    'PreCaptureFilter': 'On',
                    'VirtualStorage': '212.27TB',
                    'RealStorage': '169.00TB',
                    'Capturedrops': '0',
                    'BeginTimeSeconds': '1644950340',
                    'CaptureServerTime': '140346318284896',
                    'Throughput': '0.51',
                    'CompressionRatio': '1.26',
                    'ClusterCount': '0',
                    'tcppps': '0',
                    'udppps': '0',
                    'otherpps': '0',
                    'totalpps': '0',
                    'LogDataCompressionRatio': '8.26',
                    'PercentIOWait': '0.00',
                    'LoadAverage': '6.35 5.52 5.52'
                },
                'FMNodes': [{
                        'authenticationmode': '',
                        'throughput': '0.99',
                        'nodename': 'sw138',
                        'node_ip': '10.1.55.138',
                        'UserName': 'continuum',
                        'Password': '',
                        'Token': '',
                        'groupname': 'g138',
                        'port': '[0:10 Gbps  1:Down  ]',
                        'status': 'Running',
                        'compressionratio': '1.26',
                        'virtualstorage': '212.27TB',
                        'realstorage': '169.00TB',
                        'begintime': '2022-02-15 18:39:00',
                        'endtime': '2022-02-16 17:31:00',
                        'license': 'Evaluation',
                        'capturemode': '',
                        'precapturefilter': 'On',
                        'duration': '00:22:52:00',
                        'timezone': 'UTC',
                        'serverinfo': '0:0:0:0:0:8.26:0.00:4.77 5.24 5.45',
                        'clusternodecount': '',
                        'other': '',
                        'serverip': '10.1.55.138',
                        'percentiowait': '',
                        'loadaverage': '',
                        'selected': False
                    },
                    ...
                ],
                'Groups': [{
                        'groupname': 'g138',
                        'groupcount': 1,
                        'aggregate_throughput': 0,
                        'userslist': ''
                    },
                    ...
                ],
                'SWVersion': '7.3.0.309-408.14r2.29-u021622\n',
                'ApiVersion': '1.4'
            }
        """
        params = {"rest_token": self.sw.rest_token}
        list_of_statuses = self.sw.http_get(self.path, params=params)
        try:
            # Bug in current version that returns strings of json within json rather than nested json
            for item in ["ServerInfo", "FMNodes", "Groups"]:
                list_of_statuses[item] = loads(list_of_statuses[item])
        except:
            pass
        return list_of_statuses
