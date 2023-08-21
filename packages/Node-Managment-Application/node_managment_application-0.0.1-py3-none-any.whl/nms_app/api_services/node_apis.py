from datetime import datetime, timedelta
import json
import requests
from rest_framework import status

from nms_app.nms_services.api_key_valdation import get_node_id
from nms_app.nms_services.get_json_result import get_json_result_func, put_json_result_func
from nms_app.nms_services.get_server_info import get_server_info, get_server_details
from nms_project_settings.settings import IP_ADD


def get_node_ip_func(request):
    node_id = request.query_params.get('node_id')
    if node_id == get_node_id():
        ip, location = get_server_info()
        return {'status': 'success', 'Node Ip': IP_ADD}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def get_node_location_func(request):
    node_id = request.query_params.get('node_id')
    if node_id == get_node_id():
        ip, location = get_server_info()
        return {'status': 'success', 'Node Address': 'London'}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def upgrade_node_func(request):
    node_id = request.query_params.get('node_id')
    if node_id == get_node_id():
        msg = "Node up-gradation successfully."
        return {'status': 'success', 'Message': msg}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def get_node_status_func(request):
    node_id = request.query_params.get('node_id')
    if node_id == get_node_id():
        dt = get_server_details()
        ls_ = ['system_uptime',
               'total_cpu_usage',
               'total_ram_memory_available',
               'total_ram_memory_used',
               'ram_percentage_used',
               'used_memery',
               'free_memery',
               'used_memery_in_percentage']

        return {"status": "success", "data": {k: v for k, v in dt.items() if k in ls_}}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def get_system_config_func(request):
    node_id = request.query_params.get('node_id')
    if node_id == get_node_id():
        dt = get_server_details()
        ls_ = ['system_name',
               'operating_system_version',
               'processor',
               'physical_cores',
               'total_cores',
               'total_ram_memory_present',
               'total_memery']

        return {"status": "success", "data": {k: v for k, v in dt.items() if k in ls_}}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def get_cluster_nodes_info(request):
    node_id = request.query_params.get('node_id')
    if node_id == get_node_id():
        url = f"http://{IP_ADD}:19001/ads/validators"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                msg = str(json.loads(json.dumps(response.json())))
            else:
                msg = "Error while accessing URL."
        except:
            msg = "Error while accessing URL."
        return {'status': 'success', 'Message': msg}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def get_transaction_info_func(request):
    node_id = request.query_params.get('node_id')
    if node_id == get_node_id():
        count, err = transaction_count()
        return {'status': 'success', 'transaction_count': count}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def get_transaction_details_func():
    data = get_json_result_func('TransactionDetails')
    db_count = data["td_count"]
    count, err = transaction_count()
    if db_count != "":
        db_time = datetime.fromisoformat(data['td_cr_timestamp'])
        timestamp = (db_time + timedelta(hours=1)).strftime('%I %p') + " to " + (db_time + timedelta(hours=2)).strftime(
            '%I %p')
    else:
        db_count = 0
        timestamp = "Scheduler not yet started."
    if db_count <= count:
        res = str(int(count) - int(db_count))
    else:
        res = str(count)
        data.update({"td_cr_timestamp": datetime.now().isoformat(),
                     "td_count": count,
                     "td_api_status": err,
                     })

        put_json_result_func("TransactionDetails", data)

    return {'status': 'success', 'transaction_date': datetime.now().strftime('%d/%m/%Y'),
            'transaction_time': timestamp,
            'transaction_count': res}, status.HTTP_200_OK


def get_detailed_info_func(request):
    node_id = request.query_params.get('node_id')
    if node_id == get_node_id():
        data = get_json_result_func('IPHealthStatus')
        ihs_response = [i.get('ihs_response') for i in data['IPHealthStatus']]
        msg = "Server is " + (
            'down.' if all([True if i == 'Not Found' else False for i in ihs_response]) else 'up.')
        transaction_dt = get_transaction_details_func()[0]
        dt = get_server_details()
        dt.update({'server_status': msg})
        dt.update(transaction_dt)
        ls_ = ['system_uptime',
               'total_cpu_usage',
               'total_ram_memory_available',
               'total_ram_memory_used',
               'ram_percentage_used',
               'used_memery',
               'free_memery',
               'used_memery_in_percentage',
               'server_status', 'transaction_date', 'transaction_time', 'transaction_count']

        return {"status": "success", "data": {k: v for k, v in dt.items() if k in ls_}}, status.HTTP_200_OK
    else:
        return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED


def transaction_count():
    value_ls = list()
    err = list()
    urls = [f"http://{IP_ADD}:19001/ads/counters",
            f"http://{IP_ADD}:19002/ads/counters",
            f"http://{IP_ADD}:19003/ads/counters",
            f"http://{IP_ADD}:19004/ads/counters"]
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                url_response_json = response.json()
                for i in url_response_json:
                    if i.get('name') == 'consensusRequestsCompleted':
                        value_ls.append(i.get('count', 0))
                        print(i.get('count', 0))
            else:
                value_ls.append(0)
            err.append(response.text)
        except Exception as e:
            value_ls.append(0)
            err.append(str(e))
    return sum(value_ls), err
