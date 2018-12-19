""" ******************************************************************

Name        : get_specific_client.py
Description : Retrieves all information for a specific client
              from the RiskSense REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import requests
import json
import os
import toml


##################################################################
#
#  Function to leverage the API to retrieve all of the info
#  associated with a specific client ID.
#
##################################################################
def get_client_info(platform, key, client_id):

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
    id_to_query = configuration['platform']['client_id']

    #  Send the request for the client info to the API
    id_info = get_client_info(rs_url, api_key, id_to_query)

    print(id_info)


##################################################################
#  Execute the Script
##################################################################
if __name__ == "__main__":
    main()
