""" *******************************************************************************************************************
|
|  Name        :  get_saved_hostfinding_filters.py
|  Description :  Get saved filters from the RiskSense platform via the API.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
import os
import toml
import requests


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

    #  Load the definitions contained in the config file
    data = toml.loads(toml_data)

    return data


def get_hostfinding_filters(platform, key, cli_id):

    """
    Get saved hostfinding filters.

    :param platform:    Platform URL
    :type  platform:    str

    :param key:         API Key
    :type  key:         str

    :param cli_id:      Client ID
    :type  cli_id:      int

    :return:    The JSON response from the platform is returned.
    :rtype:     dict
    """

    url = platform + '/api/v1/client/' + str(cli_id) + '/search/hostFinding/filter'

    header = {
        "x-api-key": key,
        "content-type": "application/json"
    }

    response = requests.get(url, headers=header)

    if response and response.status_code == 200:
        jsonified_response = json.loads(response.text)

    else:
        print("There was a problem retrieving your saved hostFinding filters from the API.")
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        exit(1)

    return jsonified_response


def main():

    """ Main body of the script """

    #  Define the path to the config file, and read it.
    conf_file = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    # Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']

    response = get_hostfinding_filters(rs_url, api_key, client_id)

    if 'filters' in response:
        found_filters = response['filters']

        for single_filter in found_filters:
            print(single_filter)

    else:
        print("There were no saved filters found.")


#  Execute the script
if __name__ == "__main__":
    main()


"""
   Copyright 2019 RiskSense, Inc.
   
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:
   
   http://www.apache.org/licenses/LICENSE-2.0
   
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""