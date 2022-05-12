# 2.0
Python 2.7.18 compatibility

# 0.9
Updated to new API where federation services are handled by the server and defined by requests
New framework implemented for modular endpoints
Changed from running a request in a sentrywire handler to mapping requests to a sentrywire client

e.g

`sentrywire.request(GetSearchList())` changed to `sentrywire.search.list()`

# 0.5
Support for core functions added
- Search functions
- Partial policy function support
- Partial augmentation support
