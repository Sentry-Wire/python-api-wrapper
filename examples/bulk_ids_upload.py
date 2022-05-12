import sys

from sentrywire.client import Sentrywire
import os


def bulk_upload_rules(directory):
    """
    Upload all rule files in a directory
    Args:
        directory: (String) path to directory containing rule files

    Returns:
        Prints files being uploaded, then prints errors at the end
    """
    if directory[-1] != '/':
        directory += '/'

    if os.getenv("TARGET") is None:
        print("Set TARGET environment variable to the sentrywire host address")
        sys.exit(1)
    if os.getenv("SW_USERNAME") is None:
        print("Set SW_USERNAME environment variable to the sentrywire username")
        sys.exit(1)
    if os.getenv("SW_PASSWORD") is None:
        print("Set SW_PASSWORD environment variable to the sentrywire password")
        sys.exit(1)

    # Get only files present in a path
    rule_list = os.listdir(path=directory)

    # Loop through each value in the rule_list
    for val in rule_list:

        # Remove the value from rule_list if the ".rules" is not present in value
        if ".rules" not in val:
            rule_list.remove(val)
    print(rule_list)

    # Authenticate
    sw = Sentrywire(os.getenv("TARGET"), ssl_verify=False)
    sw.authentication.login(os.getenv("SW_USERNAME"), os.getenv("SW_PASSWORD"))

    errors = []

    for rule_file in rule_list:
        try:
            response = sw.idsrules.create(directory + rule_file)
        except Exception as e:
            errors.append((rule_file, str(e)))

    sw.authentication.logout()
    if errors:
        print("Errors:")
        for error in errors:
            print("\t" + str(error))
    else:
        print("Upload successful")


if __name__ == "__main__":
    bulk_upload_rules(sys.argv[1])
