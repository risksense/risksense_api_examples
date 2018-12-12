import requests
import json


def get_client_id(platform, key, client_id):

    url = platform + "/api/v1/client/" + str(client_id)

    header = {'x-api-key': key,
              'content-type': 'application/json'
              }

    raw_client_id_response = requests.get(url, headers=header)
    json_client_id_response = json.loads(raw_client_id_response.text)

    if raw_client_id_response.status_code == 200:
        found_id = json_client_id_response

    else:
        print(f"Error Getting Client IDs: Status Code returned was {raw_client_id_response.status_code}")
        print(raw_client_id_response.text)
        exit(1)

    return found_id


def main():

    rs_platform = 'https://platform.risksense.com'  # update as required
    api_key = ''  # insert your API token here.

    id_to_query = 12345  # update as required

    id_info = get_client_id(rs_platform, api_key, id_to_query)
    print(id_info)


if __name__ == "__main__":
    main()
