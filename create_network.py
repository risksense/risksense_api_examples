import requests
import json


def create_network(platform, key, cli_id, desired_name, desired_type):

    url = platform + "/api/v1/client/" + str(cli_id) + "/network/"

    header = {
                "x-api-key": key,
                "content-type": "application/json",
                "Cache-Control": "no-cache"
            }

    body = {
                "name": desired_name,
                "type": desired_type
            }

    raw_response = requests.post(url, headers=header, data=json.dumps(body))
    json_response = json.loads(raw_response.text)

    if raw_response.status_code == 201:
        network_response = json_response
    else:
        print(f"Error Getting Client IDs: Status Code returned was {raw_response.status_code}")
        print(json_response)
        exit(1)

    return network_response

def main():
    rs_platform = 'https://platform.risksense.com'  # update as needed
    api_key = ''  # Insert your API token here

    network_name = "My_Test_Network"

    # Options are "IP" or "HOSTNAME"
    network_type = "IP"

    client_id =  # insert your client ID here

    network_info = create_network(rs_platform, api_key, client_id, network_name, network_type)

    print(network_info)


if __name__ == "__main__":
    main()
