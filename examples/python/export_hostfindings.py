""" ******************************************************************

Name        : export_hostfindings.py
Description : Exports and downloads a csv file containing hostfindings
              from the RiskSense platform via the REST API.
Copyright   : (c) RiskSense, Inc.
License     : ????

****************************************************************** """
import requests
import json
import datetime
import time
import os
import toml


##################################################################
#
#  Function to initiate the generation of an export file
#  containing all host findings.  The file requested is in
#  .csv format.
#
##################################################################
def initiate_export(url, key, client, filename):

    print()
    print("Submitting request for host finding file export.")
    export_identifier = 0
    todays_date = datetime.date.today()

    #  Assemble the URL for the API call
    #  https://<platform>/api/vi/client/<client ID>/hostFinding/export
    api_url = url + '/api/v1/client/' + str(client) + '/hostFinding/export'

    #  Define the header for the API call
    header = {
        "x-api-key": key,
        "content-type": "application/json",
        "Cache-Control": "no-cache"
    }

    #  Define the body for the API call.  This is where we define the filter(s) to be
    #  used when generating the requested export.  In this case, we are not including
    #  a filter so that we will get *all* host findings returned.
    body = {
        "filterRequest": {
            "filters": [
                # No filter parameter used.  This results in all host findings being returned.
            ]
        },
        "fileType": "CSV",
        "comment": "Host Finding Export for " + str(todays_date),
        "fileName": filename
    }

    # Send API request to the platform
    response = requests.post(api_url, headers=header, data=json.dumps(body))

    # If successful...
    if response.status_code == 200:
        print("Export request submitted successfully.")
        jsonified_response = json.loads(response.text)
        export_identifier = jsonified_response['id']

    else:  # If not successful...
        print("There was an error requesting your export.")
        print(f"Status Code: {response.status_code}")
        print(response.text)
        exit(1)

    return export_identifier


##################################################################
#
#  Function to download an export via the RiskSense REST API.
#  The 'filename' parameter should be the desired full path
#  and name of file.  Example: /home/user-x/file.csv
#
##################################################################
def download_exported_file(platform, key, client, export, filename):

    success = False

    #  Assemble the URL for the API call
    url = platform + "/api/v1/client/" + str(client) + "/export/" + str(export)

    #  Define the header for the API call
    header = {
        'x-api-key': key,
        'content-type': 'application/json'
    }

    print("Attempting to download your export file.")

    # Send API request to the platform
    response = requests.get(url, headers=header)

    # If successful...
    if response.status_code == 200:
        print("Writing your file to disk.")
        open(filename, "wb").write(response.content)
        print(" - Done.")
        success = True

    else:  # If not successful...
        print("There was an error getting your file.")
        print(f"Status Code: {response.status_code}")
        print(response.text)
        exit(1)

    return success


##################################################################
#
#  Function to read configuration file.  Requires the
#  installation of the toml module.
#
##################################################################
def read_config_file(filename):

    toml_data = open(filename).read()
    data = toml.loads(toml_data)

    return data


##################################################################
#
#  Main Body of script
#
##################################################################
def main():

    ######################################
    #  Read config file to get platform
    #  info and API token
    ######################################
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)

    # Set our variables based on what is read from the config file.
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']

    #  Set filename for your export
    export_filename = 'hostfindings_export'  # update as desired.

    ######################################
    #  Start file export
    ######################################

    # initiate export.  Export ID is returned.
    export_id = initiate_export(rs_url, api_key, client_id, export_filename)

    # Wait for file to be exported...
    wait_time = 90  # in seconds
    x = 0

    # Display a countdown timer while we wait for the platform to generate the export file.
    while x < wait_time:
        print(f" - Sleeping for {wait_time - x} seconds to allow the platform some time to generate the file.")
        time.sleep(1)
        x += 1

    ######################################
    #  Download exported file
    ######################################

    # This is the location to save your exported file.  Adjust as desired.
    # Hostfindings exports are zip files containing other files with the actual findings.
    exported_path_file = export_filename + '.zip'

    # Request download from the platform.
    downloaded = download_exported_file(rs_url, api_key, client_id, export_id, exported_path_file)

    if downloaded:
        print("Success.")

    else:
        print("There was an error downloading your export from the platform.")
        exit(1)


##################################################################
#  Execute the Script
##################################################################
if __name__ == "__main__":
    main()
