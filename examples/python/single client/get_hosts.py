""" ******************************************************************

Name        : get_hosts.py
Description : Retrieves a list of hosts with a criticality of "5"
              from all clients associated with a user via the
              RiskSense REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import json
import os
import requests
import toml


def get_hosts(platform, key, client_id):

    """
    Retrieve a list of all of the hosts with a criticality of "5" that are associated
    with the specified client ID.

    :param platform: URL of the RiskSense platform to be queried.
    :param key: API Key.
    :param client_id: ID of the client to be queried.

    :return: a list of all hosts returned by the API.
    """

    #  Assemble the URL for the API call
    url = platform + "/api/v1/client/" + str(client_id) + "/host/search"

    #  Set the page size for returned results
    page_size = 100

    #  Set the initial page of results to retrieve
    page = 0

    #  Define the header for the API call
    header = {
        "x-api-key": key,
        "content-type": "application/json"
    }

    #  Define the filters to be used in your query.  In this case we are filtering
    #  for hosts with a criticality of "5"
    filters = [
        {
            "field": "criticality",
            "exclusive": False,
            "operator": "EXACT",
            "value": "5"
        }
        #  You can stack multiple filters here, to further narrow your results,
        #  just as you can in the UI.
    ]

    # Define the body for your API call.
    body = {
        "filters": filters,
        "projection": "basic",  # Can also be set to "detail"
        "sort": [
            {
                "field": "id",
                "direction": "ASC"
            }
        ],
        "page": page,
        "size": page_size
    }

    #  Send your request to the API, and get the number of pages of results
    #  that are available.
    raw_result = requests.post(url, headers=header, data=json.dumps(body))

    #  If request is successful...
    if raw_result.status_code == 200:
        jsonified_result = json.loads(raw_result.text)

    else:
        print("There was an error retrieving the hosts from the API.")
        print(f"Status Code Returned: {raw_result.status_code}")
        print(f"Response: {raw_result.text}")
        exit(1)

    number_of_pages = jsonified_result['page']['totalPages']

    all_hosts = []

    #  Cycle thorough all of the pages of host results and add them to a list to be returned.
    while page < number_of_pages:

        print(f"Getting page {page + 1}/{number_of_pages} of hosts for client id {client_id}...")
        raw_result = requests.post(url, headers=header, data=json.dumps(body))

        #  If request is successful...
        if raw_result.status_code == 200:
            jsonified_result = json.loads(raw_result.text)

        else:
            print(f"There was an error retrieving page {page} of the found hosts.")
            print(f"Status Code: {raw_result.status_code}")
            print(f"Response: {raw_result.text}")
            exit(1)

        #  Append the hosts found to our list to be returned.
        for finding in jsonified_result['_embedded']['hosts']:
            all_hosts.append(finding)

        # Increment the page number to retrieve in the next run.
        page += 1
        body['page'] = page

    return all_hosts


def read_config_file(filename):

    """
    Reads TOML-formatted configuration file.

    :param filename: path to file to be read.

    :return: List of variables found in config file.
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

    # Get hosts associated with the specified client ID
    hosts = get_hosts(rs_url, api_key, client_id)

    #  Print your results to the console.
    print(f"{len(hosts)} hosts found with a criticality of 5. ")
    print()


#  Execute the Script
if __name__ == "__main__":
    main()
