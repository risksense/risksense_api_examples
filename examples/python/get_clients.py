""" ******************************************************************

Name        : get_clients.py
Description : Gets and returns all of the client IDs that a user is
              associated with in the RiskSense platform via the
              REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import requests
import json
import os
import toml


##################################################################
#
#  Function to leverage the API to retrieve all client IDs
#  that are associated with a user.
#
##################################################################
def get_client_ids(platform, key):

    #  Assemble the URL for the API call
    url = platform + "/api/v1/client"

    #  Define the header for the API call
    header = {
                'x-api-key': key,
                'content-type': 'application/json'
             }

    #  Send API request to the platform
    raw_client_id_response = requests.get(url, headers=header)

    #  Convert the response to JSON format
    json_client_id_response = json.loads(raw_client_id_response.text)

    #  If request is successful...
    if raw_client_id_response.status_code == 200:
        #  Pick out all clients from the JSON formatted response
        found_ids = json_client_id_response['_embedded']['clients']

    #  If request is unsuccessful...
    else:
        print(f"Error Getting Client IDs: Status Code returned was {raw_client_id_response.status_code}")
        print(raw_client_id_response.text)
        exit(1)

    return found_ids


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

    #  Send request for client IDs.  A list is returned.
    ids = get_client_ids(rs_url, api_key)
    print(ids)


##################################################################
#  Execute the Script
##################################################################
if __name__ == "__main__":
    main()
