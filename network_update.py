import requests
import json


def update_network(platform, key, cli_id, net_id, new_name):

    url = platform + "/api/v1/client/" + str(cli_id) + "/network/" + str(net_id)

    header = {
        "x-api-key": key,
        "content-type": "application/json",
        "Cache-Control": "no-cache"
    }

    body = {
        "name": new_name
    }

    raw_response = requests.put(url, headers=header, data=json.dumps(body))
    json_response = json.loads(raw_response.text)

    if raw_response.status_code == 200:
        network_response = json_response
    else:
        print(f"Error Getting Client IDs: Status Code returned was {raw_response.status_code}")
        print(json_response)
        exit(1)

    return network_response


def main():

    rs_platform = 'https://platform.risksense.com'  # update as needed
    api_key = ''  #insert your API token here

    client_id =  # update with client ID to be used
    network_id =  # update with network ID to be used

    new_network_name = "My_New_Network_Name"  # update as desired

    network_info = update_network(rs_platform, api_key, client_id, network_id, new_network_name)

    print(network_info)


if __name__ == "__main__":
    main()