import requests
import json


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


def get_hosts(platform, key, client_id):

    url = platform + "/api/v1/client/" + str(client_id) + "/host/search"
    page_size = 100
    page = 0

    header = {
        "x-api-key": key,
        "content-type": "application/json"
    }

    filters = [
        {
            "field": "criticality",
            "exclusive": False,
            "operator": "EXACT",
            "value": "5"
        }
        #  Filtering for all hosts with a criticality of 5
        #  You can stack multiple filters here, just as in the UI
    ]

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

    raw_result = requests.post(url, headers=header, data=json.dumps(body))
    jsonified_result = json.loads(raw_result.text)

    number_of_pages = jsonified_result['page']['totalPages']

    all_hosts = []

    while page < number_of_pages:

        print(f"Getting page {page + 1} of {number_of_pages} pages of hosts for client id {client_id}...")
        raw_result = requests.post(url, headers=header, data=json.dumps(body))
        jsonified_result = json.loads(raw_result.text)

        for finding in jsonified_result['_embedded']['hosts']:
            all_hosts.append(finding)

        page += 1
        body['page'] = page

    return all_hosts


def main():

    rs_platform = 'https://platform.risksense.com'  # update as required
    api_key = ''  # insert your API token here.

    #  Get all client IDs associated with your api_key
    clients = get_client_ids(rs_platform, api_key)

    #  Print your results to the console.
    print()
    print(f"{len(clients)} clients found.")

    #  Get all hosts associated with each Client ID
    print("Getting hosts for each client identified.")
    print()

    for client in clients:
        hosts = get_hosts(rs_platform, api_key, client['id'])  # hosts variable is a list of all hosts found for that client

        #  Print your results to the console.
        print(f"{len(hosts)} open hosts found for client \"{client['name']}\" found. ")
        print()


if __name__ == "__main__":
    main()
