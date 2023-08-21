import os
import urllib
import json
import requests

from rest_framework import status

from nms_app.nms_services.api_key_valdation import get_node_id
from nms_app.nms_services.common_services import run_command
from nms_project_settings.settings import IP_ADD


def gaurdian_join_network_func(request):
    node_id = request.query_params.get('node_id')
    ip = request.query_params.get('server_ip')
    public_port = request.query_params.get('public_port')
    p2p_port = request.query_params.get('p2p_port')
    if node_id == get_node_id():
        url = f"http://{ip}:{public_port}/cluster/info"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                id_ = response.json()
                if id_:
                    l1_id = id_[0].get('id')
                    run_command(
                        f"""curl -X POST http://127.0.0.1:9067/cluster/join -H "Content-type: application/json" -d '{"id": "{l1_id}", "ip": "{ip}", "p2pPort": {p2p_port} }'""")
                    res = "GUARDIAN network joined successfully."
                else:
                    res = 'Id not present in response.'
            else:
                # Request failed
                res = f"Error while accessing {url}."
        except:
            res = f"Error while accessing {url}."

        return {'status': 'success', 'Message': res}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def join_network_func(request):
    node_id = request.query_params.get('node_id')
    ip = request.query_params.get('server_ip')
    port = request.query_params.get('port_number')
    if node_id == get_node_id():
        url = f"http://{ip}:{port}/ads/validator-id"
        try:
            dt = dict()
            response = requests.get(url)
            if response.status_code == 200:
                id_ = response.text
                body_json = {"id": id_.replace('"', ''),
                             "host": ip,
                             "port": port}
                urls = ["http://localhost:19001/ads/validators/join",
                        "http://localhost:19002/ads/validators/join",
                        "http://localhost:19003/ads/validators/join",
                        "http://localhost:19004/ads/validators/join"]

                for i in urls:
                    try:
                        response = requests.post(i, data=json.dumps(body_json))
                        code = response.status_code
                    except:
                        code = f"Error while accessing {i}."
                    dt[str(urllib.parse.urlparse(i).port)] = 'Joined' if code == 202 else 'Fail'
            else:
                # Request failed
                dt = f"Error while accessing {url}."
        except:
            dt = f"Error while accessing {url}."

        return {'status': 'success', 'Message': str(dt)}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def leave_network_func(request):
    node_id = request.query_params.get('node_id')
    if node_id == get_node_id():
        dt = dict()
        urls = [f"http://{IP_ADD}:19001/ads/validators/leave",
                f"http://{IP_ADD}:19002/ads/validators/leave",
                f"http://{IP_ADD}:19003/ads/validators/leave",
                f"http://{IP_ADD}:19004/ads/validators/leave"]
        for i in urls:
            try:
                response = requests.post(i)
                code = response.status_code
            except:
                code = f"Error while accessing {i}."
            dt[str(urllib.parse.urlparse(i).port)] = 'Left' if code == 202 else 'Fail'
        return {'status': 'success', 'Message': str(dt)}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


