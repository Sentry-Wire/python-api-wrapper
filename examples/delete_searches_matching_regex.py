import sys

from sentrywire.client import Sentrywire
import os
import re


def delete_searches_matching_regex(pattern):
    """
    Comb completed searches and delete those matching a regex

    Args:
        pattern: regex pattern to match e.g. ".*continuum.*"

    Returns:
        List of searches deleted
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

    # Authenticate
    sw = Sentrywire(os.getenv("TARGET"), ssl_verify=False)
    sw.authentication.login(os.getenv("SW_USERNAME"), os.getenv("SW_PASSWORD"))

    completed_searches = sw.searches.completed()
    search_names = []
    for item in completed_searches:
        if re.search(pattern, item["SearchName"]):
            if os.getenv("DEBUG"):
                print("Deleting " + item["Searchname"])
            search_names.append(item["SearchName"])
            sw.searches.delete(item["SearchName"])

    print(str(search_names))
    return search_names


if __name__ == "__main__":
    """
    Example: Delete all searches run by continuum. Username and search name are part of the search token
    
    python delete_searches_matching_regex continuum
    """
    delete_searches_matching_regex(sys.argv[1])
