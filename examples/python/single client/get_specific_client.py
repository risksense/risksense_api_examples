""" *******************************************************************************************************************
|
|  Name        :  get_specific_client.py
|  Description :  Retrieves all information for a specific client
                  from the RiskSense REST API.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
import os
import requests
import toml


def get_client_info(platform, key, client_id):

    """
    Retrieves all attributes of a specific client.

    :param platform:    URL for RiskSense platform to be queried.
    :type  platform:    str

    :param key:         API Key
    :type  key:         str

    :param client_id:   Client ID to be queried.
    :type  client_id:   int

    :return:    Returns a dictionary of the attributes found.
    :rtype:     dict
    """

    #  Assemble the URL for the API request
    url = platform + "/api/v1/client/" + str(client_id)

    #  Define the header for the API request
    header = {
        'x-api-key': key,
        'content-type': 'application/json'
    }

    #  Send the request to the API
    response = requests.get(url, headers=header)

    #  If the request was successful...
    if response and response.status_code == 200:
        found_info = json.loads(response.text)

    #  If the request was unsuccessful...
    else:
        print("There was an error retrieving the client information.")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        exit(1)

    return found_info


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

    """ Main Body of script """

    #  Define the path to the config file, and read it
    conf_file = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    #  Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    id_to_query = configuration['platform']['client_id']

    #  Send the request for the client info to the API
    id_info = get_client_info(rs_url, api_key, id_to_query)

    #  print ID info to the console.
    print(id_info)


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
