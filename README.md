# About
This wrapper is for the sentrywire API v2.0

# Installation
**Requries Python 2.7 or higher.** 

## Libraries
In order to use this wrapper you will need the python requests library. 

The version below is the version used to develop this, but it will likely work with most versions of the requests library
- requests>=2.24.0
### To install dependencies
run the following commands based on your operating system to install the requests library
- Linux/macOS
  - python3 -m pip install -U requests

- Windows
    - py -3 -m pip install -U requests

If these methods do not work for you, then you can follow the extended installation guide on their site
[https://requests.readthedocs.io/en/latest/user/install/#install](https://requests.readthedocs.io/en/latest/user/install/#install)

# SentryWire client
The Sentrywire client class is the primary method of interaction within the wrapper.

Aside from any SentrywireExceptions you handle, this is the only thing you will need to import.
```python
from sentrywire.client import Sentrywire
from os import getenv

# Create a new sentrywire handler instance for the unit at IP 192.168.0.1
sw = Sentrywire(getenv("SW_IP"))
# Login to the unit (generates a new rest token for the client)
sw.authentication.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))
# List completed searches on the system
sw.searches.completed()
# Invalidate the currently stored rest token
sw.authentication.logout()
```

# Exceptions
Each request may raise exceptions based on issues that occur. There are several types of exceptions:

## Sentrywire exceptions
Aside from the parent class, SentrywireException,
all exceptions are directly associated with http status codes

- SentrywireException
  - Parent class that other Exceptions extend
- 400: InvalidParameters
  - You may be missing parameters
  - Parameters may not be valid for the request you are making
  - More information provided in exception description
- 401: InvalidAuthentication
  - Provided credentials are invalid
- 403: InvalidAuthentication
  - Provided credentials are invalid
- 404: NotFound
  - item was not found
- 429: TooManyRequests
  - Server is full or overloaded
- 500: ServerError
  - Something has gone horribly wrong

# Login and logout
All functions require a login. The sentrywire client will manage your authentication tokens, but requires credentials to login with.
```python
from sentrywire.client import Sentrywire
from os import getenv

# Create a new sentrywire handler instance
sw = Sentrywire("192.168.0.1")

# Login using the given credentials
sw.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

# Log out of a unit
sw.logout()
```

From here on, it will be assumed that 'sw' refers to an established sw instance.

# Searches
## Creating a new search
The wrapper uses an instance of a sentrywire handler to manage requests sent to a unit. 
Here is an example using a request to create a new search with the following parameters
- Named "test_search" 
- Filtering for pcap data coming from port 80 
- Originating yesterday or afterward

For more information on how to create a search, look into the sw.searches.create function. You can do this via help(sw.searches.create)
```python
from sentrywire.client import Sentrywire
from datetime import datetime, timedelta
from os import getenv

# Create a new sentrywire handler instance
sw = Sentrywire("192.168.0.1")

# This function requires admin login
sw.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

response = sw.searches.create("test_new_search",
                              datetime.now() - timedelta(minutes=45),
                              datetime.now() - timedelta(minutes=30),
                              search_filter="tcp or udp",
                              max_packets=100
                              )

# Print the response
print(response)
# It will show a python dictionary object that looks like this 
# {
#   "searchname": "continuum_1631377579_1_test_new_search"
# }

# From this result, we likely want to save the search_token so we can check on this search later
search_token = response["searchname"]
# search_token appears as "test_new_search" with extra data around it
```

## Checking status of our search
```python
from sentrywire.client import Sentrywire
from os import getenv

# Create a new sentrywire handler instance (or just use the old one)
sw = Sentrywire("192.168.0.1")
test_search_token = "REST_test_create_90n6wt0p_api.demos"

response = sw.searches.status(getenv("NODE_NAME"), test_search_token)

print(response)
# It will return a python dictionary that looks like this
#  {'SearchKey': 'continuum_1635133528_100_test_search_status_pendingsw152', 'SearchName': 'continuum_1635133528_100_test_search_status_pending', 'SubmittedTime': '1635133528', 'Begintime': '2021-10-24 23:00:20', 'Endtime': '2021-10-24 23:15:20', 'SearchFilter': 'PcapData,tcp or udp', 'NodeName': 'sw152', 'SearchStatus': 'Pending'}
```

## Deleting a search 
If a search you created is no longer necessary, you may want to delete it. Here is how to do that. You can find more information in the class definiton of `sw.searches.delete()`

You must stop a search before you delete it.
```python
from sentrywire.client import Sentrywire
from os import getenv

# Create a new sentrywire handler instance (or just use an already authenticated one at this point)
sw = Sentrywire("192.168.0.1")
test_search_token = "REST_test_create_90n6wt0p_api.demos"

# Login
sw.login(getenv("SW_USERNAME"), getenv("SW_PASSWORD"))

# The output of this command is the json response, but it is likely irrelevant if the command did not raise an error
response = sw.searches.delete(test_search_token)
print(response)
# {
#   'message': 'REST_test_create_90n6wt0p_api.demos Deleted',
# }
```

# Help
Going forward, refer to the docstrings for what the responses for each method will look like. 

## help(sw.server.status)
```
>>> help(sw.server.status)
Help on method status in module sentrywire.v2.server:
status() method of sentrywire.v2.server.Server instance
    Get server status
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

```

It will also tell you what commands are available via the methods for each item.
## help(sw.server)
```
>>> help(sw.server)
Help on Server in module sentrywire.v2.server object:
class Server(sentrywire.base.EndpointHandler)
 |  Server(sw)
 |  
 |  Method resolution order:
 |      Server
 |      sentrywire.base.EndpointHandler
 |      sentrywire.base.SentrywireHandler
 |      builtins.object
 |  
 |  Methods defined here:
 |  
 |  __init__(self, sw)
 |      Server status function handler
 |  
 |  status(self)
 |      Get server status
 |      Returns:
 |          (list of dict): Server status dump
 |          [
 |              {
 |                  'authenticationmode': '',
 |                  'throughput': '0.00',
 |                  'nodename': 's12',
 |                  'node_ip': '10.100.5.12',
 |                  'UserName': 'continuum',
 |                  'Password': '',
 |                  'Token': '',
 |                  'groupname': 'sentrywire',
 |                  'port': '[0:Down  1:Down  ]',
 |                  'status': 'Running',
 |                  'compressionratio': '1.36',
 |                  'virtualstorage': '12.27TB',
 |                  'realstorage': '9.00TB',
 |                  'begintime': '2021-10-15 00:20:00',
 |                  'endtime': '2021-10-20 16:13:00',
 |                  'license': 'Evaluation',
 |                  'capturemode': '',
 |                  'precapturefilter': 'Off',
 |                  'duration': '05:15:53:00',
 |                  'timezone': 'UTC',
 |                  'serverinfo': '0:0:0:0:0:9.16',
 |                  'clusternodecount': '',
 |                  'other': '',
 |                  'serverip': '10.100.5.12'
 |              },
 |              {
 |                  other server's info
 |              },
 |              ...
 |           ]
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  path = '/fmping'
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from sentrywire.base.SentrywireHandler:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
```

# List of supported requests

Read this list as if further indentation implies a period

For example: `sw.searches.pending()` appears as 
- sw
  - searches 
    - pending()

Parameters that appear as `method(<parameter>=None)` means that the parameter is optional, and can be defined by explicitly stating the name, followed by an equals sign, then the desired value.

Alternatively, parameters that appear as `method(<parameter>=<value>)` means that the parameter has a default value that you can override

- sw
  - login(username, password)
  - logout(username, password)
  - activetriggers
    - create(trigger_name, search_filter, seconds_before, seconds_after)
    - delete(trigger_name)
    - list(trigger_name=None)
  - authentication
    - login(username, password)
    - logout(username, password)
  - authorization
    - roles
      - create(role_name, permissions)
      - delete(role_name)
      - list()
  - federation
    - groups
      - create(group_name)
      - delete(group_name)
      - list()
    - nodes
      - create(node_address, group_name)
      - delete(node_address)
  - idsrules
    - create(file_path)
    - delete(rule_set_name)
    - list(list_type)
      - list_type is either "activated" or "deactivated"
    - get(rule_set_name, file_path)
      - Downloads a rule set to the file_path
    - activate(rule_set_name)
    - deactivate(rule_set_name)
  - precapturefilter
    - create(search_filter)
      - You can also use add()
    - delete()
      - You can also use reset()
    - list()
  - searches
    - create(search_name, begin_time, end_time, search_filter=None, max_packets=1000)
    - delete(search_name)
    - status(node_name, search_name)
    - pending(count=0)
    - completed(count=0)
    - pcaps
      - list(node_name, search_token)
      - get(node_name, search_name, index, file_path)
    - logs
      - get(node_name, search_token, file_path)
    - objects
      - list(node_name, search_token, file_path)
      - get(node_name, search_token, file_path)
  - server
    - status()
