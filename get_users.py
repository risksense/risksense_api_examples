import requests
import json

""" ************************************

Gets and returns a list of all client 
IDs associated with your API key.

************************************ """
def get_client_ids(platform, key):

    page_size = 100
    url = platform + "/api/v1/client?size=" + str(page_size)

    header = {'x-api-key': key,
              'content-type': 'application/json'
              }

    raw_client_id_response = requests.get(url, headers=header)
    json_client_id_response = json.loads(raw_client_id_response.text)
    found_ids = json_client_id_response['_embedded']['clients']

    return found_ids


""" ************************************

Gets and returns a list of all users 
with a Manager role for a particular
client ID.

************************************ """
def get_users(platform, key, client_id):

    url = platform + "/api/v1/client/" + str(client_id) + "/user/search"
    page_size = 100
    page = 0

    header = {
        "x-api-key": key,
        "content-type": "application/json"
    }

    filters = [
        {
            "field": "role",
            "exclusive": False,
            "operator": "EXACT",
            "value": "Manager"
        }
        #  Filtering for all users with Manager authority
        #  You can stack multiple filters here, just as in the UI
    ]

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

    raw_result = requests.post(url, headers=header, data=json.dumps(body))
    jsonified_result = json.loads(raw_result.text)

    number_of_pages = jsonified_result['page']['totalPages']

    found_users = []

    while page < number_of_pages:

        print(f"Getting page {page + 1} of {number_of_pages} pages of users for client id {client_id}...")
        raw_result = requests.post(url, headers=header, data=json.dumps(body))
        jsonified_result = json.loads(raw_result.text)

        for finding in jsonified_result['_embedded']['users']:
            found_users.append(finding)

        page += 1
        body['page'] = page

    return found_users


def main():

    rs_platform = 'https://platform.risksense.com'  # update as required
    api_key = ''  # insert your API token here.

    #  Get all client IDs associated with your api_key
    clients = get_client_ids(rs_platform, api_key)

    #  Print your results to the console.
    print()
    print(f"{len(clients)} clients found.")

    #  Get all users associated with each Client ID
    print("Getting users for each client identified.")
    print()

    for client in clients:
        users = get_users(rs_platform, api_key, client['id'])  # users variable is a list of all users found for that client

        #  Print your results to the console.
        print(f"{len(users)} users (Managers) for client \"{client['name']}\" found. ")
        print()


if __name__ == "__main__":
    main()
