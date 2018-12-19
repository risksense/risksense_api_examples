""" ******************************************************************

Name        : network_update.py
Description : Updates the name of a network by leveraging the
              RiskSense REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import requests
import json
import os
import toml


##################################################################
#
#  Function to update your network via the API.
#
##################################################################
def update_network(platform, key, client, net_id, new_name):

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
    raw_response = requests.put(url, headers=header, data=json.dumps(body))

    #  If the request is successful...
    if raw_response.status_code == 200:
        network_response = json.loads(raw_response.text)

    #  If the request is unsuccessful...
    else:
        print("An error occurred updating the network via API.")
        print(f"Status Code: {raw_response.status_code}")
        print(f"Response: {raw_response.text}")
        exit(1)

    return network_response


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

    #  Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']

    #  Define the network ID to be updated.
    network_id =

    #  Define the new name for your network
    #  Update as desired.
    new_network_name = "My_New_Network_Name"

    #  Send the network update request to the platform via the API
    network_info = update_network(rs_url, api_key, client_id, network_id, new_network_name)

    #  Print the network info returned from your request.
    print(network_info)


##################################################################
#  Execute the Script
##################################################################
if __name__ == "__main__":
    main()