""" ******************************************************************

Name        : get_specific_client.py
Description : Retrieves all information for a specific client
              from the RiskSense REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import json
import os
import requests
import toml


def get_client_info(platform, key, client_id):

    """
    Retrieves all attributes of a specific client.

    :param platform:    URL for RiskSene platform to be queried.
    :param key:         API Key
    :param client_id:   Client ID to be queried.

    :return:    Returns a dictionary of the attributes found.
    """

    #  Assemble the URL for the API request
    url = platform + "/api/v1/client/" + str(client_id)

    #  Define the header for the API request
    header = {
                'x-api-key': key,
                'content-type': 'application/json'
    }

    #  Send the request to the API
    raw_client_id_response = requests.get(url, headers=header)

    #  If the request was successful...
    if raw_client_id_response.status_code == 200:
        found_info = json.loads(raw_client_id_response.text)

    #  If the request was unsuccessful...
    else:
        print("There was an error retrieving the client information.")
        print(f"Error Getting Client IDs: Status Code returned was {raw_client_id_response.status_code}")
        print(raw_client_id_response.text)
        exit(1)

    return found_info


def read_config_file(filename):

    """
    Reads TOML-formatted configuration file.

    :param filename:    Path to file to be read.

    :return:    List of variables found in config file.
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
