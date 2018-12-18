import requests
import json
import datetime
import time


##################################################################
#
#  Initiates the generation of the export file containing
#  all users.  The file requested is in .csv format.
#
##################################################################
def initiate_export(url, key, client, filename):

    print()
    print("Submitting request for host finding file export.")
    export_identifier = 0
    todays_date = datetime.date.today()

    api_url = url + '/api/v1/client/' + str(client) + '/hostFinding/export'

    header = {
        "x-api-key": key,
        "content-type": "application/json",
        "Cache-Control": "no-cache"
    }

    body = {
        "filterRequest": {
            "filters": [
                # No filter parameter used.  This results in all users being returned.
            ]
        },
        "fileType": "CSV",
        "comment": "Host Finding Export for " + str(todays_date),
        "fileName": filename
    }

    response = requests.post(api_url, headers=header, data=json.dumps(body))

    if response.status_code == 200:
        print("Export request submitted successfully.")
        jsonified_response = json.loads(response.text)
        export_identifier = jsonified_response['id']

    else:
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

    url = platform + "/api/v1/client/" + str(client) + "/export/" + str(export)

    header = {
        'x-api-key': key,
        'content-type': 'application/json'
    }

    print("Attempting to download your export file.")

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        print("Writing your file to disk.")
        open(filename, "wb").write(response.content)
        print(" - Done.")
        success = True

    else:
        print("There was an error getting your file.")
        print(f"Status Code: {response.status_code}")
        print(response.text)
        exit(1)

    return success


##################################################################
#
#  Main Body of script
#
##################################################################
def main():
    rs_url = 'https://platform.risksense.com'  # Update as needed.
    api_key = ''  # Add your API token here.
    client_id =  # Add your client ID here.

    export_filename = 'hostfindings_export'  # update as desired.

    ######################################
    #  Start file export
    ######################################

    # initiate export.  Export ID is returned.
    export_id = initiate_export(rs_url, api_key, client_id, export_filename)

    # Wait for file to be exported...
    wait_time = 90  # in seconds
    x = 0

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
