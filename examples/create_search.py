from datetime import datetime
import sys

from sentrywire.client import Sentrywire
import os


def download_search_objects(search_name, start_time, end_time, search_filter, max_packets=10000):
    """
    Create search on Sentrywire unit

    Args:
        search_name     String
        start_time      Datetime
        end_time        Datetime
        search_filter   String
        max_packets     Int

    Returns:
        Requests request: objects endpoint response
    """
    if os.getenv("TARGET") is None:
        print("Set TARGET environment variable to the sentrywire host address")
        sys.exit(1)
    if os.getenv("SW_USERNAME") is None:
        print("Set SW_USERNAME environment variable to the sentrywire username")
        sys.exit(1)
    if os.getenv("SW_PASSWORD") is None:
        print("Set SW_PASSWORD environment variable to the sentrywire password")
        sys.exit(1)

    sw = Sentrywire(os.getenv("TARGET"), ssl_verify=False)
    sw.authentication.login(os.getenv("SW_USERNAME"), os.getenv("SW_PASSWORD"))
    response = sw.searches.create(search_name,
                                  start_time,
                                  end_time,
                                  search_filter=search_filter,
                                  max_packets=max_packets
                                  )

    sw.authentication.logout()

    return response


if __name__ == "__main__":
    """
    Create a search.
    SW_USERNAME=<Sentrywire user> SW_PASSWORD=<Sentrywire password> TARGET=<Sentrywire IP> python <search_name> <start_time> <end_time> <search_filter> <max_packets=10000>

    Example with max packets: 
    SW_USERNAME=test_user SW_PASSWORD=abc123 TARGET=10.1.55.176 python create_search_test 2/23/22T00:00:00 2/23/22T01:00:00 "tcp or udp" 10
    Example without max packets (Defaults to 10,000):
    SW_USERNAME=test_user SW_PASSWORD=abc123 TARGET=10.1.55.176 python create_search_test 2/23/22T00:00:00 2/23/22T01:00:00 "tcp or udp"
    """
    if len(sys.argv) == 6:
        print(download_search_objects(sys.argv[1],
                                      datetime.strptime(sys.argv[2], '%m/%d/%yT%H:%M:%S'),
                                      datetime.strptime(sys.argv[3], '%m/%d/%yT%H:%M:%S'),
                                      sys.argv[4],
                                      max_packets=int(sys.argv[5])))
    else:
        print(download_search_objects(sys.argv[1],
                                      datetime.strptime(sys.argv[2], '%m/%d/%yT%H:%M:%S'),
                                      datetime.strptime(sys.argv[3], '%m/%d/%yT%H:%M:%S'),
                                      sys.argv[4]))
