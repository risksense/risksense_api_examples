import requests
import json
import time

""" *****************************************************
  Function to generate an export of hostfindings via
  the RiskSense REST API.
***************************************************** """
def create_export(platform, key, client, file_name):

    url = platform + "/api/v1/client/" + str(client) + "/hostFinding/export"

    header = {
                'x-api-key': key,
                'content-type': 'application/json'
             }

    #  Filter for host findings that are open and have known threats.
    filters = [
        {  # filter for open findings
            "field": "generic_state",
            "exclusive": False,
            "operator": "EXACT",
            "value": "open"
        },
        {  # filter for findings with threats
            "field": "has_threat",
            "exclusive": False,
            "operator": "EXACT",
            "value": True
        }
    ]

    body = {
                "filterRequest": {
                    "filters": filters
                },
                "fileType": "CSV",
                "comment": "Generated via Python Script",
                "fileName": file_name
    }

    raw_result = requests.post(url, headers=header, data=json.dumps(body))

    if raw_result.status_code == 200:
        jsonified_result = json.loads(raw_result.text)

    else:
        print("** There was an error creating your export. **")
        print(f"Status code returned: {raw_result.status_code}")
        print(raw_result.text)
        exit(1)

    export_identifier = jsonified_result['id']

    return export_identifier

""" *****************************************************
  Function to download an export via the
  RiskSense REST API.
***************************************************** """
def get_exported_file(platform, key, client, export):

    url = platform + "/api/v1/client/" + str(client) + "/export/" + str(export)

    header = {
        'x-api-key': key,
        'content-type': 'application/json'
    }

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        print("Writing your file to disk.")
        open("my_export_file.zip", "wb").write(response.content)
        print("Done.")

    else:
        print("There was an error getting your file.")


""" *****************************************************
  Main body of the script
***************************************************** """
def main():

    rs_platform = 'https://platform.risksense.com'  # update as needed
    api_key = ''  # Insert your API token here
    client_id =  # Insert your client ID here

    #  Generate the export
    export_filename = "my_test_file"
    export_id = create_export(rs_platform, api_key,client_id, export_filename)
    print(f"Export ID: {export_id}")

    #  Make the script sleep for 30 seconds to allow time for the platform to generate the export.
    #  Depending on how big your export is, and how busy the platform is, the time needed to
    #  generate the file will vary.
    #  Displays the countdown of the timer to the console.

    x = 0
    time_to_sleep = 30

    while x < time_to_sleep:
        time.sleep(1)
        print(f"Sleeping for {time_to_sleep - x} seconds")
        x += 1

    print("Time to download your export.")
    print()

    #  Download your file
    get_exported_file(rs_platform, api_key, client_id, export_id)


if __name__ == "__main__":
    main()
