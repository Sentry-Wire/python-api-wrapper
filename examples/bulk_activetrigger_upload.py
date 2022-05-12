import sys

from sentrywire.client import Sentrywire
import os
import json

import logging
from http.client import HTTPConnection


def bulk_upload_triggers(file_path):
    """
    Upload many triggers from a single file

    File must contain a list of json objects containing triggers.
    [
        {
            "trigger_name": "ssl_visibility",
            "search_filter":
            "vlan 5 or vlan 6",
            "seconds_before": "30",
            "seconds_after": "30",
            "createdtime": "2021-12-27T15:35:29.209Z"
        },
        ...
    ]
    Created time is not used, but is included in the list active triggers API output

    Args:
        file_path: (String) path to file

    Returns:
        Prints files being uploaded, then prints errors at the end
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

    # Load input data
    with open(file_path, 'r') as f:
        trigger_list = json.loads(f.read())

    # Authenticate
    sw = Sentrywire(os.getenv("TARGET"), ssl_verify=False)
    sw.enable_debug()
    sw.authentication.login(os.getenv("SW_USERNAME"), os.getenv("SW_PASSWORD"))

    errors = []

    for trigger in trigger_list:
        try:
            response = sw.activetriggers.create(trigger["trigger_name"],
                                                trigger["search_filter"],
                                                trigger["seconds_before"],
                                                trigger["seconds_after"])
        except Exception as e:
            errors.append((trigger, str(e)))

    sw.authentication.logout()
    if errors:
        print("Errors:")
        for error in errors:
            print("\t" + str(error))
    else:
        print("Upload successful")


if __name__ == "__main__":
    bulk_upload_triggers(sys.argv[1])
