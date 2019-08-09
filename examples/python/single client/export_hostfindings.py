""" ******************************************************************

Name        : export_hostfindings.py
Description : Exports and downloads a csv file containing hostfindings
              from the RiskSense platform via the REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """

import json
import datetime
import time
import os
import requests
import toml


def initiate_export(platform, key, client, filename):

    """
    Initiates the generation of an export file containing all host findings in .csv format.

    :param platform:    URL of RiskSense Platform to be queried
    :type  platform:    str

    :param key:         API Key.
    :type  key:         str

    :param client:      Client ID associated with data to be exported.
    :type  client:      int

    :param filename:    Specifies the desired filename for the export.
    :type  filename:    str

    :return:    Returns the identifier for the export.
    :rtype:     int
    """

    print()
    print("Submitting request for host finding file export.")
    export_identifier = 0
    todays_date = datetime.date.today()

    #  Assemble the URL for the API call
    #  https://<platform>/api/vi/client/<client ID>/hostFinding/export
    api_url = platform + '/api/v1/client/' + str(client) + '/hostFinding/export'

    #  Define the header for the API call
    header = {
        "x-api-key": key,
        "content-type": "application/json",
        "Cache-Control": "no-cache"
    }

    #  This is where we define the filter(s) to be sed when generating the requested
    #  export file.  In this case, we are filtering for host findings that have
    #  threats.

    filters = [
        {
            "field": "has_threat",
            "exclusive": False,
            "operator": "EXACT",
            "value": True
        }
    ]

    #  Define the body for the API call.
    body = {
        "filterRequest": {
            "filters": filters
        },
        "fileType": "CSV",
        "comment": "Host Finding Export for " + str(todays_date),
        "fileName": filename
    }

    # Send API request to the platform
    response = requests.post(api_url, headers=header, data=json.dumps(body))

    # If successful...
    if response and response.status_code == 200:
        print("Export request submitted successfully.")
        jsonified_response = json.loads(response.text)
        export_identifier = jsonified_response['id']

    # If not successful...
    else:
        print("There was an error requesting your export.")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        exit(1)

    return export_identifier


def download_exported_file(platform, key, client, export, filename):

    """
    Downloads an export via the RiskSense REST API.

    :param platform:    URL of the RiskSense platform to be queried.
    :type  platform:    str

    :param key:         API Key
    :type  key:         str

    :param client:      Client ID associated with the export.
    :type  client:      int

    :param export:      Identifier of the export to be downloaded.
    :type  export:      int

    :param filename:    File path and name where download will be stored.
    :type  filename:    str

    :return:    Returns a boolean reflecting whether or not the download was successful.
    :rtype:     bool
    """

    success = False

    #  Assemble the URL for the API call
    url = platform + "/api/v1/client/" + str(client) + "/export/" + str(export)

    #  Define the header for the API call
    header = {
        'x-api-key': key,
        'content-type': 'application/json'
    }

    print("Attempting to download your export file.")

    #  Send API request to the platform
    response = requests.get(url, headers=header)

    #  If successful...
    if response.status_code == 200:
        print("Writing your file to disk.")
        open(filename, "wb").write(response.content)
        print(" - Done.")
        success = True

    #  If not successful...
    else:
        print("There was an error getting your file.")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text:{response.text}")
        exit(1)

    return success


def read_config_file(filename):

    """
    Reads TOML-formatted configuration file.

    :param filename:    path to file to be read.
    :type  filename:    str

    :return:    List of variables found in config file.
    :rtype:     list
    """

    toml_data = open(filename).read()
    data = toml.loads(toml_data)

    return data


def main():

    """ Main body of the script. """

    #  Read config file to get platform info and API token
    conf_file = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    # Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']

    #  Set filename for your export
    export_filename = 'hostfindings_export'  # UPDATE AS DESIRED

    ######################################
    #  Start file export
    ######################################

    #  Initiate the export.  Export ID is returned.
    export_id = initiate_export(rs_url, api_key, client_id, export_filename)

    #  Wait for file to be exported.  This could take quite a while depending now how big
    #  your export is, and how busy the platform is.  You may need to adjustaccordingly.
    #  Currently set to wait 5 minutes.
    wait_time = 600  # Seconds
    counter = 0

    # Display a countdown timer while we wait for the platform to generate the export file.
    while counter < wait_time:
        print(f" - Sleeping for {wait_time - counter} seconds to allow the platform some time to generate the file.")
        time.sleep(1)
        counter += 1

    ######################################
    #  Download exported file
    ######################################

    #  This is the location to save your exported file.  Adjust as desired.
    #  Hostfindings exports are zip files containing other files with the actual findings.
    exported_path_file = export_filename + '.zip'

    # Request download from the platform.
    downloaded = download_exported_file(rs_url, api_key, client_id, export_id, exported_path_file)

    if downloaded:
        print("Success.")

    else:
        print("There was an error downloading your export file from the platform.")
        exit(1)


#  Execute the Script
if __name__ == "__main__":
    main()
