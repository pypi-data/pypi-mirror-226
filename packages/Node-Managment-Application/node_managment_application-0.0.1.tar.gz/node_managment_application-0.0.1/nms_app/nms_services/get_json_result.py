import json

from nms_project_settings.settings import BASE_DIR


def get_json_result_func(file):
    f = open(f'{BASE_DIR}/nms_app/data_files/{file}.json')
    # f = open(f'/home/ubuntu/nms_project/node_mgmt_system/nms_app/data_files/{file}.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    return data


def put_json_result_func(file, data):
    with open(f'{BASE_DIR}/nms_app/data_files/{file}.json', 'w') as f:
        # with open(f'/home/ubuntu/nms_project/node_mgmt_system/nms_app/data_files/{file}.json', 'w') as f:
        json.dump(data, f)
