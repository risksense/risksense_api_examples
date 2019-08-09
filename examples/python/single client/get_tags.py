""" ******************************************************************

Name        : get_tags.py
Description : Retrieves a list of all tags associated with a client
              via the RiskSense REST API.
Copyright   : (c) RiskSense, Inc.
License     : Apache-2.0

****************************************************************** """

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


def get_tags(platform, key, client_id):

    """
    Retrieve a list of all of the tags that are associated with
    the specified client ID.

    :param platform:    URL of the RiskSense platform to be queried.
    :type  platform:    str

    :param key:         API Key.
    :type  key:         str

    :param client_id:   ID of the client to be queried.
    :type  client_id:   int

    :return:    A list of all tags returned by the API.
    :rtype:     list
    """

    #  Assemble the URL for the API call
    url = platform + "/api/v1/client/" + str(client_id) + "/tag/search"

    #  Set the page size for returned results
    page_size = 100

    #  Set the initial page of results to retrieve
    page = 0

    #  Define the header for the API call
    header = {
        "x-api-key": key,
        "content-type": "application/json"
    }

    #  Define the filters to be used in your query.  You can get a list of fields
    #  that can be filtered on from the /client/{clientId}/tag/filter API endpoint.
    filters = [
        #  In this case we are filtering for all tags created in 2018.  You can
        #  stack multiple filters here, to further narrow your results, just as
        #  you can in the UI.
        {
            "field": "created",
            "exclusive": False,
            "operator": "LIKE",
            "value": "2018"
        }

    ]

    # Define the body for your API call.
    body = {
        "filters": filters,  # The filters you specified above
        "projection": "basic",
        "sort": [  # Sort results returned by tag ID  (ascending)
            {
                "field": "id",
                "direction": "ASC"
            }
        ],
        "page": page,
        "size": page_size
    }

    #  Send your request to the API, and get the number of pages of results
    #  that are available.
    response = requests.post(url, headers=header, data=json.dumps(body))

    #  If the status code returned equals success...
    if response and response.status_code == 200:
        jsonified_result = json.loads(response.text)

    else:
        print("There was an error retrieving the tags from the API.")
        print(f"Status Code Returned: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)

    number_of_pages = jsonified_result['page']['totalPages']

    all_tags = []

    #  Cycle thorough all of the pages of tag results and add them to a list to be returned.
    while page < number_of_pages:

        #  Send the API request
        print(f"Getting page {page + 1}/{number_of_pages} of tags for client id {client_id}...")
        response = requests.post(url, headers=header, data=json.dumps(body))

        #  If the status code returned equals success...
        if response and response.status_code == 200:
            jsonified_result = json.loads(response.text)

        else:
            print(f"There was an error retrieving page {page} of the found tags.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            exit(1)

        #  Append the tags found to our list to be returned.
        for item in jsonified_result['_embedded']['tags']:
            all_tags.append(item)

        # Increment the page number to retrieve in the next run.
        page += 1
        body['page'] = page

    return all_tags


def main():

    """ Main body of script """

    #  Define the path to the config file, and read it.
    conf_file = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    # Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']

    #  Get a list of the tags returned.
    tags = get_tags(rs_url, api_key, client_id)

    #  Get the length of the list that was returned.  This is the number of tags found.
    number_of_tags = len(tags)

    #  Print basic information about each tag found to the console.
    print("Tags found:")
    print()
    for tag in tags:
        print(f"Tag ID: {tag['id']}")
        print(f"Tag Name: {tag['name']}")
        print(f"Tag Desc: {tag['description']}")
        print()

    #  Print the total number of tags that were found to the console.
    print(f"{number_of_tags} tag(s) were retrieved from the RiskSense API.")
    print()


# Execute the script
if __name__ == '__main__':
    main()
