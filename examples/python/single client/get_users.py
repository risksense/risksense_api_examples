""" ******************************************************************

Name        : get_users.py
Description : Retrieves all users with a "Manager" role for all
              clients associated with an API token from the
              RiskSense REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import json
import os
import requests
import toml


def get_users(platform, key, client_id):

    """
    Gets and returns a list of all users with a 'Manager' role for the specified client ID.

    :param platform:    URL for the RiskSense platform to be queried.
    :param key:         API Key
    :param client_id:   Client ID to be queried.

    :return:    Returns a list of all users with a 'Manager' role for the specified client ID.
    """

    #  Assemble the URL for the API request
    url = platform + "/api/v1/client/" + str(client_id) + "/user/search"

    #  Define the page size for returned results.  This is the number of results in a single page.
    page_size = 100

    #  Define the page number to begin with when sending the API request.
    page = 0

    #  Define the header for your API request
    header = {
                "x-api-key": key,
                "content-type": "application/json"
    }

    #  Define the filters to be used in the API request.  In this case we are filtering for
    #  all users with a "Manager" role.
    filters = [
        {
            "field": "role",
            "exclusive": False,
            "operator": "EXACT",
            "value": "Manager"
        }
        #  You can stack multiple filters here to further narrow your results, just as in the UI
    ]

    #  Define the body for the API request.
    body = {
        "filters": filters,
        "projection": "basic",
        "sort": [
            {
                "field": "id",
                "direction": "ASC"
            }
        ],
        "page": page,
        "size": page_size
    }

    #  Send the request to the API
    raw_result = requests.post(url, headers=header, data=json.dumps(body))

    #  If the request is successful...
    if raw_result.status_code == 200:
        jsonified_result = json.loads(raw_result.text)
        number_of_pages = jsonified_result['page']['totalPages']

    #  If the request is unsuccessful...
    else:
        print("There was an error retrieving the users from the API.")
        print(f"Status Code: {raw_result.status_code}")
        print(f"Response: {raw_result.text}")
        exit(1)

    found_users = []

    #  Cycle thorough all of the pages of users and add them to a list to be returned.
    while page < number_of_pages:

        print(f"Getting page {page + 1}/{number_of_pages} of users for client id {client_id}...")

        # Send the request to the API
        raw_result = requests.post(url, headers=header, data=json.dumps(body))

        #  If the request is successful...
        if raw_result.status_code == 200:

            # Convert the response text to JSON format.
            jsonified_result = json.loads(raw_result.text)

        #  If the request is unsuccessful...
        else:
            print(f"There was an error retrieving page {page} of users from the API.")
            print(f"Status Code: {raw_result.status_code}")
            print(f"Response: {raw_result.text}")
            exit(1)

        for finding in jsonified_result['_embedded']['users']:
            found_users.append(finding)

        #  Increment the page number for the next run
        page += 1
        body['page'] = page

    return found_users


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
    client_id = configuration['platform']['client_id']

    # Get users.  The 'users' variable is a list of all users found for that client
    users = get_users(rs_url, api_key, client_id)

    #  Print the number of users with a "Manager" role to the console.
    print(f"{len(users)} users (Managers) found. ")
    print()


#  Execute the Script
if __name__ == "__main__":
    main()