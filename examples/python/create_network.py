""" ******************************************************************

Name        : create_network.py
Description : Creates a new RiskSense network via the REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import requests
import json
import os
import toml


##################################################################
#
#  Function to leverage the API to create your new network.
#  This function sends a post request containing the
#  information required to create that new network.
#
##################################################################
def create_network(platform, key, cli_id, desired_name, desired_type):

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


##################################################################
#
#  Function to read configuration file.  Requires the
#  installation of the toml module.
#
##################################################################
def read_config_file(filename):

    #  Read the config file
    toml_data = open(filename).read()

    #  Load the definitions in the config file
    data = toml.loads(toml_data)

    return data


##################################################################
#
#  Main Body of script
#
##################################################################
def main():

    #  Define the path to the config file, and read it
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    # Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']

    #  Define the name for your new network.  Update as desired.
    network_name = "My_Test_Network"

    #  Define the type for your new network.  The options are "IP" or "HOSTNAME"
    network_type = "IP"

    #  Create your network.  The information associated with the network created
    #  is returned.
    network_info = create_network(rs_url, api_key, client_id, network_name, network_type)

    print(network_info)


##################################################################
#  Execute the Script
##################################################################
if __name__ == "__main__":
    main()
