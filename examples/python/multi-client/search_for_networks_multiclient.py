"""********************************************************************************************************************
|
|  Name        : search_for_networks_multiclient.py
|  Description : Searches for a network by leveraging the RiskSense REST API.
|  Copyright   : 2019 (c) RiskSense, Inc.
|  License     : Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
********************************************************************************************************************"""

import json
import os
import toml
import requests


def get_clients(platform, key):

    """
    Gets and returns a list of all client IDs associated with your API key.

    :param platform:    URL of RiskSense platform to be queried.
    :type  platform:    str

    :param key:         API Key
    :type  key:         str

    :return:    Returns a list of all client IDs associated with your API key.
    :rtype:     list
    """

    #  Define the size of the page to be returned by request.  This is the number
    #  of results on a single page.
    page_size = 100

    #  Assemble the URL for your API request
    url = platform + "/api/v1/client?size=" + str(page_size)

    #  Define the header for your API request
    header = {
        'x-api-key': key,
        'content-type': 'application/json'
    }

    #  Submit your request to the API
    response = requests.get(url, headers=header)

    #  If the request is successful...
    if response and response.status_code == 200:
        #  Convert the response text to JSON format.
        jsonified_response = json.loads(response.text)

        #  Get the found_ids from the JSON-formatted response.
        #  found_ids is a list of dictionaries.
        found_clients = jsonified_response['_embedded']['clients']

    #  If the request is unsuccessful...
    else:
        print("There was an error retrieving the clients from the API.")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)

    return found_clients


def get_networks(platform, key, client_id):

    """
    Gets all networks with a type of 'hostname' for the specified client ID.

    :param platform:    URL of RiskSense platform to be queried.
    :type  platform:    str

    :param key:         API Key
    :type  key:         str

    :param client_id:   Client ID to be queried.
    :type  client_id:   int

    :return:    Returns a list of dictionaries containing all of the found networks.
    :rtype:     list
    """

    #  Assemble the URL for the API request.
    url = platform + "/api/v1/client/" + str(client_id) + "/network/search"

    #  Define the page size for your request.  This is the number of results that can
    #  be returned in a single page.
    page_size = 100

    #  Define the starting page for your requests.
    page = 0

    #  Define the header for your request.
    header = {
        "x-api-key": key,
        "content-type": "application/json"
    }

    #  Define the filter(s) for your request.  In this case, we are filtering for
    #  any network that is of the type "hostname".
    filters = [
        {
            "field": "type",
            "exclusive": False,
            "operator": "EXACT",
            "value": "hostname"
        }
        #  You can stack multiple filters here to further narrow the results, just as in the UI
    ]

    #  Define the body for your request.
    body = {
        "filters": filters,
        "projection": "basic",  # There is no "detail" projection for networks
        "sort": [
            {
                "field": "id",
                "direction": "ASC"
            }
        ],
        "page": page,
        "size": page_size
    }

    #  Submit your request to the API.
    response = requests.post(url, headers=header, data=json.dumps(body))

    #  If the request is successful...
    if response and response.status_code == 200:
        jsonified_response = json.loads(response.text)
        number_of_pages = jsonified_response['page']['totalPages']

    #  If the request is unsuccessful...
    else:
        print("There was an error retrieving the networks from the API.")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)

    found_networks = []

    # Cycle through all of the pages of results, and add them to a list (found_networks)
    while page < number_of_pages:

        print(f"Getting page {page + 1}/{number_of_pages} of networks for client id {client_id}...")

        #  Submit your request to the API.
        response = requests.post(url, headers=header, data=json.dumps(body))

        #  If the request is successful...
        if response and response.status_code == 200:
            jsonified_response = json.loads(response.text)

        #  If the request is unsuccessful...
        else:
            print(f"There was an error retrieving page {page} of the networks from the API.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            exit(1)

        #  Cycle through all of the findings returned, and append them to the found_networks list
        for finding in jsonified_response['_embedded']['networks']:
            found_networks.append(finding)

        #  Increment the page number for the next run.
        page += 1
        body['page'] = page

    return found_networks


def read_config_file(filename):

    """
    Reads TOML-formatted configuration file.

    :param filename:    Path to file to be read.
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

    """ Main body of script. """

    #  Define the path to the config file, and read it
    conf_file = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    #  Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']

    #  Get all clients associated with your api_key
    clients = get_clients(rs_url, api_key)

    #  Print the number of clients found to the console.
    print()
    print(f"{len(clients)} clients found.")

    #  Get all users associated with each Client
    print("Getting networks for each client identified.")
    print()

    #  Cycle through all of the clients found, and retrieve all networks returned by the filter.
    for client in clients:

        # networks variable is a list of all networks found for that client
        networks = get_networks(rs_url, api_key, client['id'])

        #  Print the number of networks found to the console.
        print(f"{len(networks)} networks for client \"{client['name']}\" found. ")
        print()


#  Execute the Script
if __name__ == "__main__":
    main()

"""
Copyright 2019 RiskSense, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""