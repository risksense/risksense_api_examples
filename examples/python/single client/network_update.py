""" *******************************************************************************************************************
|
|  Name        : network_update.py
|  Description : Updates the name of a network by leveraging the RiskSense REST API.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
import os
import requests
import toml


def update_network(platform, key, client, net_id, new_name):

    """
    Updates the name of a network via the API.

    :param platform:    URL of the RiskSense Platform to be queried.
    :type  platform:    str

    :param key:         API Key.
    :type  key:         str

    :param client:      Client ID to be queried.
    :type  client:      int

    :param net_id:      Identifier for network to be updated.
    :type  net_id:      int

    :param new_name:    Desired new name for the network to be updated.
    :type  new_name:    str

    :return:    Returns a dictionary containing the response from the platform.
    :rtype:     dict
    """

    #  Assemble the URL for the API request.
    url = platform + "/api/v1/client/" + str(client) + "/network/" + str(net_id)

    #  Define the header for the API request.
    header = {
        "x-api-key": key,
        "content-type": "application/json",
        "Cache-Control": "no-cache"
    }

    #  Define the body for the API request
    body = {
        "name": new_name
    }

    #  Submit the update request to the API
    response = requests.put(url, headers=header, data=json.dumps(body))

    #  If the request is successful...
    if response and response.status_code == 200:
        network_response = json.loads(response.text)

    #  If the request is unsuccessful...
    else:
        print("An error occurred updating the network via API.")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)

    return network_response


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

    """ Main body of the script. """

    #  Define the path to the config file, and read it
    conf_file = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    #  Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']

    #  Update to define the network ID to be updated.
    network_id = 0  # UPDATE AS DESIRED

    #  Define the new name for your network
    new_network_name = "My_New_Network_Name"  # UPDATE AS DESIRED

    #  Send the network update request to the platform via the API
    network_info = update_network(rs_url, api_key, client_id, network_id, new_network_name)

    #  Print the network info returned from from the platform in response to your request.
    print(network_info)


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
