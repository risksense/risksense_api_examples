""" ******************************************************************

Name        : create_network.py
Description : Creates a new RiskSense network via the REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import json
import os
import requests
import toml


def create_network(platform, key, cli_id, desired_name, desired_type):

    """
    Sends a post request containing the information required to create that new network.

    :param platform:        URL for RiskSense Platform to be posted to
    :param key:             API Key
    :param cli_id:          Client ID associated with the network to be created.
    :param desired_name:    Desired name for the new network.
    :param desired_type:    Type for the new network. "IP" or "HOSTNAME"

    :return:    Dict containing the new network's attributes.
    """

    #  Assemble the URL for the API call
    url = platform + "/api/v1/client/" + str(cli_id) + "/network/"

    #  Define the header for the API call
    header = {
                "x-api-key": key,
                "content-type": "application/json",
                "Cache-Control": "no-cache"
    }

    #  Define the body for the API call.  This is where we define the name and
    #  type of the network to be created.
    body = {
                "name": desired_name,
                "type": desired_type
    }

    # Send API request to the platform
    raw_response = requests.post(url, headers=header, data=json.dumps(body))

    # If request is successful...
    if raw_response.status_code == 201:
        json_response = json.loads(raw_response.text)

    # If request is unsuccessful...
    else:
        print(f"Error Getting Client IDs: Status Code returned was {raw_response.status_code}")
        print(raw_response.text)
        exit(1)

    return json_response


def read_config_file(filename):

    """
    Reads TOML-formatted configuration file.

    :param filename:    Path to file to be read.

    :return:    List of variables found in config file.
    """

    #  Read the config file
    toml_data = open(filename).read()

    #  Load the definitions retrieved from the config file
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

    #  Define the name for your new network.  UPDATE AS DESIRED
    network_name = "My_Test_Network"

    #  Define the type for your new network.  The options are "IP" or "HOSTNAME".  UPDATE AS DESIRED
    network_type = "IP"

    #  Create your network.  The information associated with the network created
    #  is returned and assigned to the network_info variable.
    network_info = create_network(rs_url, api_key, client_id, network_name, network_type)

    #  Print the new network details to the console.
    print(network_info)


#  Execute the Script
if __name__ == "__main__":
    main()
