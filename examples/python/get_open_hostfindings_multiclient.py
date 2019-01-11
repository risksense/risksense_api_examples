""" ******************************************************************

Name        : get_open_hostfindings_multiclient.py
Description : Retrieves a list of all open hostfindings for all
              clients associated with a user from the RiskSense
              REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import json
import os
import requests
import toml


def get_clients(platform, key):

    """
    Retrieve all clients that associated with a user.

    :param platform:    URL for RiskSense Platform to be queried
    :param key:         API Key

    :return: Returns a list of clients found.
    """

    #  Set page size for results to be returned.
    page_size = 100

    #  Assemble the URL for the API call.
    url = platform + "/api/v1/client?size=" + str(page_size)

    #  Define the header for the API call.
    header = {
                'x-api-key': key,
                'content-type': 'application/json'
    }

    #  Make the API call
    raw_client_id_response = requests.get(url, headers=header)

    #  If request is successful...
    if raw_client_id_response.status_code == 200:

        #  Convert the response to JSON
        json_client_id_response = json.loads(raw_client_id_response.text)

        #  Grab the list of found IDs from the JSON-converted response.
        #  found_clients is a list of dictionaries.
        found_clients = json_client_id_response['_embedded']['clients']

    #  If request is unsuccessful...
    else:
        print("There was an error retrieving the client IDs.")
        print(f"Status Code: {raw_client_id_response.status_code}")
        print(f"Response: {raw_client_id_response.text}")
        exit(1)

    return found_clients


def get_all_open_hostfindings(platform, key, client_id):

    """
    Retrieve all open hostfindings that are associated with the specified client ID.

    :param platform:    URL for RiskSense Platform to be queried
    :param key:         API Key
    :param client_id:   Client ID to be queried

    :return:    Returns a list of the hostfindings found.
    """

    #  Assemble the URL for the API call
    url = platform + "/api/v1/client/" + str(client_id) + "/hostFinding/search"

    #  Set the page size for the returned results.  This is the number of results in a single page.
    page_size = 100

    #  Set the initial page to retrieve.
    page = 0

    #  Define the header for the API call.
    header = {
        "x-api-key": key,
        "content-type": "application/json"
    }

    #  Define the filters for the API call.  In this case, we are filtering for all
    #  hostfindings that are open.
    filters = [
                {
                    "field": "generic_state",
                    "exclusive": False,
                    "operator": "EXACT",
                    "value": "open"
                }
                #  You can stack multiple filters here to further narrow your results , just as in the UI.
    ]

    #  Define the body for the API call.
    body = {
                "filters": filters,
                "projection": "basic",  # Can also be set to "detail"
                "sort": [
                    {
                        "field": "id",
                        "direction": "ASC"
                    }
                ],
                "page": page,
                "size": page_size
    }

    #  Send API request to the platform
    raw_result = requests.post(url, headers=header, data=json.dumps(body))

    #  If request is successful...
    if raw_result.status_code == 200:

        # Convert response to JSON format
        jsonified_result = json.loads(raw_result.text)

        # Get the number of available pages of results from the response.
        number_of_pages = jsonified_result['page']['totalPages']

    #  If request is unsuccessful...
    else:
        print("There was an error retrieving the hostfindings from the API")
        print(f"Status Code: {raw_result.status_code}")
        print(f"Response: {raw_result.text}")
        exit(1)

    all_hostfindings = []

    ###########################################
    #  Cycle thorough all of the pages of
    #  hostfindings and add them to a list
    #  to be returned.
    ###########################################
    while page < number_of_pages:

        print(f"Getting page {page + 1}/{number_of_pages} pages of hostFindings for client id {client_id}...")

        #  Send API request to the platform for this page of hostfindings
        raw_result = requests.post(url, headers=header, data=json.dumps(body))

        #  If request is successful...
        if raw_result.status_code == 200:
            jsonified_result = json.loads(raw_result.text)

        #  If request is unsuccessful...
        else:
            print(f"There was an issue retrieving page {page} of hostfindings.")
            print(f"Status Code: {raw_result.status_code}")
            print(f"Response: {raw_result.text}")
            exit(1)

        #  Cycle through findings in this set of results and append to the list to be returned.
        for finding in jsonified_result['_embedded']['hostFindings']:
            all_hostfindings.append(finding)

        #  Increment the page number for the next run.
        page += 1
        body['page'] = page

    return all_hostfindings


def read_config_file(filename):

    """
    Reads TOML-formatted configuration file.

    :param filename: path to file to be read.

    :return: List of variables found in config file.
   """

    #  Read the config file
    toml_data = open(filename).read()

    #  Load the definitions in the config file
    data = toml.loads(toml_data)

    return data


def main():

    """ Main Body of script. """

    #  Define the path to the config file, and read it
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    # Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']

    #  Get all client IDs associated with your user.
    clients = get_clients(rs_url, api_key)

    #  Print the number of clients found to the console.
    print()
    print(f"{len(clients)} clients found: ")
    print(clients)
    print()

    #  Get all hostFindings associated with each Client ID
    for client in clients:

        #  Get all hostfindings associated with a client ID
        hostfindings = get_all_open_hostfindings(rs_url, api_key, client['id'])

        #  Print the number of hostfindings found to the console.
        print(f"{len(hostfindings)} open hostFindings found for Client {client['name']} found: ")
        print()


#  Execute the Script
if __name__ == "__main__":
    main()
