import sys
import time

from sentrywire.client import Sentrywire
import os


def download_search_objects(node_name, search_token, destination_directory):
    """
    Download search objects

    Args:
        Destination path for desired zip file

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

    if destination_directory[-1] != "/":
        destination_directory = destination_directory + "/"
    file_name = destination_directory + search_token + "_objects.zip"

    sw = Sentrywire(os.getenv("TARGET"), ssl_verify=False)
    sw.authentication.login(os.getenv("SW_USERNAME"), os.getenv("SW_PASSWORD"))

    while True:
        response = sw.searches.status(node_name, search_token)
        if "SearchStatus" in response:
            time.sleep(5)
        elif "SearchResult" in response:
            break
        else:
            raise Exception("Unexpected search state: " + str(response))

    response = sw.searches.objects.get(node_name, search_token, file_name)

    sw.authentication.logout()

    return response


if __name__ == "__main__":
    """
    Return objects from search. Username and search name are part of the search token
    SW_USERNAME=<Sentrywire user> SW_PASSWORD=<Sentrywire password> TARGET=<Sentrywire IP> python <node_name> <search_token> <destination_directory>

    Example: 
    SW_USERNAME=test_user SW_PASSWORD=abc123 TARGET=10.1.55.176 python download_search_objects sw176 continuum_1645157014_124_test_get_pcap /tmp/
    """
    print(download_search_objects(sys.argv[1], sys.argv[2], sys.argv[3]))
