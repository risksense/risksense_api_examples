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


def get_all_open_hostfindings(platform, key, client_id):

    url = platform + "/api/v1/client/" + str(client_id) + "/hostFinding/search"
    page_size = 100
    page = 0

    header = {
        "x-api-key": key,
        "content-type": "application/json"
    }

    filters = [
                {
                    "field": "generic_state",
                    "exclusive": False,
                    "operator": "EXACT",
                    "value": "open"
                }
                #  You can stack multiple filters here to further narrow your results , just as in the UI.
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

    all_hostfindings = []

    while page < number_of_pages:

        print(f"Getting page {page + 1}/{number_of_pages} pages of hostFindings for client id {client_id}...")
        raw_result = requests.post(url, headers=header, data=json.dumps(body))
        jsonified_result = json.loads(raw_result.text)

        for finding in jsonified_result['_embedded']['hostFindings']:
            all_hostfindings.append(finding)

        page += 1
        body['page'] = page

    return all_hostfindings


def main():

    rs_platform = 'https://platform.risksense.com'  # update as needed
    api_key = ''  # insert your API token here

    #  Get all client IDs associated with your api_key
    clients = get_client_ids(rs_platform, api_key)

    #  Print your results to the console.
    print()
    print(f"{len(clients)} clients found: ")
    print(clients)
    print()

    #  Get all hostFindings associated with each Client ID
    for client in clients:
        hostfindings = get_all_open_hostfindings(rs_platform, api_key, client['id'])

        #  Print your results to the console.
        print(f"{len(hostfindings)} open hostFindings found for Client {client['name']} found: ")
        print(hostfindings)
        print()


if __name__ == "__main__":
    main()
