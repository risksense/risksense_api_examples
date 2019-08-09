""" ******************************************************************

Name        : move_hosts_to_new_group.py
Description : Moves a group of hosts (specified by filters) to a
              new group via the RiskSense REST API.
Copyright   : (c) RiskSense, Inc.
License     : Apache-2.0

****************************************************************** """

import json
import os
import requests
import toml


def move_hosts_to_new_group(platform, key, client, group):

    """
    Move hosts defined by a filter to a new group, specified by group ID.

    :param platform:    URL of the RiskSense platform to be queried.
    :type  platform:    str

    :param key:         API Key.
    :type  key:         str

    :param client:      ID of the client to be used.
    :type  client:      int

    :param group:       ID of the group you are moving the hosts into.
    :type  group:       int

    :return:    A list of all hosts returned by the API.
    :rtype:     list
    """

    success = False

    #  Assemble the URL for the API call
    url = platform + "/api/v1/client/" + str(client) + "/host/group/move"

    #  Define the header for the API call
    header = {
        "x-api-key": key,
        "content-type": "application/json"
    }

    #  Define the filters to be used in your query.  In this case we are filtering
    #  for hosts with a hostname of my.hostname.com.  Update to reflect your
    #  network conditions.
    filters = [
        {
            "field": "hostName",
            "exclusive": False,
            "operator": "EXACT",
            "value": "my.hostname.com"  # UPDATE THIS FILTER AS DESIRED
        }
        #  You can stack multiple filters here, to further narrow your results,
        #  just as you can in the UI.
    ]

    # Define the body for your API call.  Specifies the filter(s) to use to identify the hosts
    # that you would like moved, and the group to move them to.
    body = {
        "filterRequest": {
            "filters": filters  # This uses the filter(s) defined above.
        },
        "targetGroupId": group
    }

    #  Send your request to the API.
    response = requests.post(url, headers=header, data=json.dumps(body))

    #  If request is reported as successful...
    if response and response.status_code == 200:
        success = True

    else:
        print("There was an error updating the hosts from the API.")
        print(f"Status Code Returned: {response.status_code}")
        print(f"Response: {response.text}")

    return success


def read_config_file(filename):

    """
    Reads TOML-formatted configuration file.

    :param filename:    path to file to be read.
    :type  filename:    str

    :return:    Variables found in config file.
    :rtype:     dict
    """

    #  Read the config file
    toml_data = open(filename).read()

    #  Load the definitions in the config file
    data = toml.loads(toml_data)

    return data


def main():

    """ Main Body of script """

    #  Define the path to the config file, and read it.
    conf_file = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    # Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']

    #  Specify ID for group that you would like to move your hosts to.
    group_id = 0  # UPDATE THIS WITH YOUR DESIRED GROUP ID

    #  Move the hosts to the new group.
    print(f"Moving host(s) to new group({group_id}).")
    print()

    #  Call the function to move your hosts
    successful = move_hosts_to_new_group(rs_url, api_key, client_id, group_id)

    if successful:
        print("The move was successful.")

    else:
        print("The attempted move was not successful.")


#  Execute the Script
if __name__ == "__main__":
    main()
