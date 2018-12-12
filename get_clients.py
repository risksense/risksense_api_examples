import requests
import json


def get_client_ids(platform, key):

    url = platform + "/api/v1/client"

    header = {'x-api-key': key,
              'content-type': 'application/json'
              }

    raw_client_id_response = requests.get(url, headers=header)

    json_client_id_response = json.loads(raw_client_id_response.text)

    if raw_client_id_response.status_code == 200:
        found_ids = json_client_id_response['_embedded']['clients']

    else:
        print(f"Error Getting Client IDs: Status Code returned was {raw_client_id_response.status_code}")
        print(raw_client_id_response.text)
        exit(1)

    return found_ids


def main():

    rs_platform = 'https://platform.risksense.com'  # update as required
    api_key = ''  # insert your API token here.

    ids = get_client_ids(rs_platform, api_key)
    print(ids)


if __name__ == "__main__":
    main()
