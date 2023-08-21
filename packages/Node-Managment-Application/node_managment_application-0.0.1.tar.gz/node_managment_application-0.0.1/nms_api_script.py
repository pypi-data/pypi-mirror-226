#!/usr/bin/env python

import urllib.parse
import requests

from nms_project_settings.settings import IP_ADD


def post_request(path, app_key, body_json):
    headers = {
        "Authorization": app_key}
    response = requests.post(urllib.parse.urljoin(API_URL, path), params=body_json, headers=headers)
    return response


def get_request(path, app_key, json_payload):
    # Set the Content-Type header to indicate JSON data
    headers = {"Content-Type": "application/json", "Authorization": app_key}
    return requests.get(urllib.parse.urljoin(API_URL, path), params=json_payload, headers=headers)


def put_request(path, app_key, body_json):
    headers = {
        "Authorization": app_key}
    response = requests.put(urllib.parse.urljoin(API_URL, path), params=body_json, headers=headers)
    return response


def node_id_func(api_key):
    response = post_request('get_node_id/', api_key, {})
    return response.json().get("Node Id", "")


def api_calls():
    app_key = 'AR12532DE@#GH&67GF24GH45532$##FGG'
    node_id = node_id_func(app_key)
    while True:
        print("1. Setup project")
        print("2. Start project app")
        print("3. Stop project app")
        print("4. Restart project app")
        print("5. Get node ip")
        print("6. Get node location")
        print("7. Upgrade node")
        print("8. Get system config")
        print("9. App health status")
        print("10. Join network")
        print("11. Leave network")
        print("12. Get log")
        print("13. Get node id")
        print("14. Get health check status")
        print("15. Exit")
        print('\n')
        try:
            choice = int(input("Enter your choice : "))
        except:
            print("Enter only number.")
            break
        if choice == 1:
            response = post_request('setup_project/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("Message", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 2:
            response = get_request('start_project_app/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("Message", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 3:
            response = get_request('stop_project_app/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("Message", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 4:
            response = get_request('restart_project_app/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("Message", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 5:
            response = get_request('get_node_ip/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print("node ip address : " + response.json().get("Node Ip",""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 6:
            response = get_request('get_node_location/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print("node geo location : " + response.json().get(
                    "Node Address", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 7:
            response = put_request('upgrade_node/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("Message", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 8:
            response = get_request('get_system_config/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("data", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 9:
            response = get_request('app_health_status/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("data", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 10:
            response = get_request('join_network/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("Message", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 11:
            response = get_request('leave_network/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("Message", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 110:
            network_status = int(input("Enter network_status : "))
            open_ports_protocol = input("Enter open_ports_protocol : ")
            open_ports_port_number = int(input("Enter open_ports_port_number : "))
            close_ports_protocol = input("Enter close_ports_protocol : ")
            close_ports_port_number = int(input("Enter close_ports_port_number : "))
            response = post_request('set_firewall_request/', app_key,
                                    {"network_status": network_status, "node_id": node_id,
                                     "open_ports_protocol": open_ports_protocol,
                                     "open_ports_port_number": open_ports_port_number,
                                     "close_ports_protocol": close_ports_protocol,
                                     "close_ports_port_number": close_ports_port_number})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                dt = response.json().get("data", "")
                if dt:
                    print('Firewall setup details : \n', dt['data'])
                else:
                    print('Something went wrong.')
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 12:
            response = get_request('get_log/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("Message", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 13:
            response = post_request('get_node_id/', app_key, {})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print("Node Id : ", response.json().get("Node Id", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 14:
            response = post_request('check_health_status/', app_key, {"node_id": node_id})
            print('-------------------------------------------------------')
            if response.status_code in [200, 401]:
                print(response.json().get("Message", ""))
            else:
                print("Something went wrong.")
            print('\n')

        elif choice == 15:
            break
        else:
            print('-------------------------------------------------------')
            print("Invalid Choice")
            break


API_URL = f"http://{IP_ADD}:9000/nms_app/"

api_calls()
