""" *******************************************************************************************************************
|
|  Name        :  search_for_networks.py
|  Description :  searches for a network by leveraging the RiskSense REST API.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
import os
import toml
import requests


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
    :rtype:     dict
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
        jsonified_result = json.loads(response.text)

    #  If the request is unsuccessful...
    else:
        print("There was an error retrieving the networks from the API.")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)

    number_of_pages = jsonified_result['page']['totalPages']
    found_networks = []

    # Cycle through all of the pages of results, and add them to a single list (found_networks)
    while page < number_of_pages:

        print(f"Getting page {page + 1}/{number_of_pages} of networks for client id {client_id}...")

        #  Submit your request to the API.
        response = requests.post(url, headers=header, data=json.dumps(body))

        #  If the request is successful...
        if response.status_code == 200:
            jsonified_result = json.loads(response.text)

        #  If the request is unsuccessful...
        else:
            print(f"There was an error retrieving page {page} of the networks from the API.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            exit(1)

        #  Cycle through all of the findings returned, and append them to the found_networks list
        for finding in jsonified_result['_embedded']['networks']:
            found_networks.append(finding)

        #  Increment the page number for the next run.
        page += 1
        body['page'] = page

    return found_networks


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

    """ Main body of script. """

    #  Define the path to the config file, and read it
    conf_file = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    #  Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']

    # Get a list of networks for the specified client.
    networks = get_networks(rs_url, api_key, client_id)

    #  Print the number of networks found to the console.
    print(f"{len(networks)} hostname networks found.")
    print()

    #  Print the found networks to the console.
    for network in networks:
        print(network)


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
