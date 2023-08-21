import os
import subprocess
from rest_framework import status

from nms_app.models import SetupProjectDetails
from nms_app.nms_services.api_key_valdation import get_node_id
from nms_app.nms_services.common_services import run_command, kill_processes_by_cmdline
from nms_app.nms_services.get_json_result import get_json_result_func


def start_project_app_func(request):
    try:
        # Get the 'node_id' from the query parameters of the request
        node_id = request.query_params.get('node_id')

        # Assuming 'get_node_id()' retrieves the expected node_id
        expected_node_id = get_node_id()

        if not node_id:
            return {'status': 'fail', 'message': "Node ID is missing."}, status.HTTP_400_BAD_REQUEST

        if node_id != expected_node_id:
            return {'status': 'fail', 'message': "Invalid Node ID."}, status.HTTP_401_UNAUTHORIZED

        spd_node_category = SetupProjectDetails.objects.values_list('spd_node_category', flat=True)

        if "MASTER" in spd_node_category:
            try:
                path = "/home/ubuntu/nms_project/node_mgmt_system/nms_app/nms_services/start_l2_project.sh"
                #run_command(f"sudo dos2unix {path}")
                os.system(f'echo "dos2unix {path}" > /app/docker_pipes/project_app_pipe')
                subprocess.check_call(['/usr/bin/bash', path])
                msg = "Project application started successfully."
                return {'status': 'success', 'message': msg}, status.HTTP_200_OK
            except subprocess.CalledProcessError as e:
                msg = str(e)
                return {'status': 'fail', 'message': msg}, status.HTTP_500_INTERNAL_SERVER_ERROR

        if "GUARDIAN" in spd_node_category:
            try:
                path = "/home/ubuntu/nms_project/node_mgmt_system/nms_app/nms_services/start_l1_project.sh"
                #run_command(f"sudo dos2unix {path}")
                os.system(f'echo "dos2unix {path}" > /app/docker_pipes/project_app_pipe')
                subprocess.check_call(['/usr/bin/bash', path])
                msg = "Project application started successfully."
                return {'status': 'success', 'message': msg}, status.HTTP_200_OK
            except subprocess.CalledProcessError as e:
                msg = str(e)
                return {'status': 'fail', 'message': msg}, status.HTTP_500_INTERNAL_SERVER_ERROR

        # Return a JSON response with status 404 if the 'spd_node_category' is not recognized
        return {'status': 'fail', 'message': "Unknown Node Category."}, status.HTTP_404_NOT_FOUND

    except Exception as e:
        # Return a JSON response with status 500 if an unexpected error occurs
        return {'status': 'error', 'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


def stop_project_app_func(request):
    try:
        # Get the 'node_id' from the query parameters of the request
        node_id = request.query_params.get('node_id')

        # Assuming 'get_node_id()' retrieves the expected node_id
        expected_node_id = get_node_id()

        if not node_id:
            return {'status': 'fail', 'message': "Node ID is missing."}, status.HTTP_400_BAD_REQUEST

        if node_id != expected_node_id:
            return {'status': 'fail', 'message': "Invalid Node ID."}, status.HTTP_401_UNAUTHORIZED

        spd_node_category = SetupProjectDetails.objects.values_list('spd_node_category', flat=True)

        if "MASTER" in spd_node_category:
            # os.chdir(r'/home/ubuntu/L2_App/')
            # run_command('sudo docker-compose down')
            os.system('echo "cd /home/ubuntu/L2_App" > /app/docker_pipes/project_app_pipe')
            os.system('echo "docker-compose down" > /app/docker_pipes/project_app_pipe')
        elif "GUARDIAN" in spd_node_category:
            kill_processes_by_cmdline('tessellation-core-assembly-1.9.1.jar')

        msg = f"{spd_node_category[0]} project stopped successfully."
        return {'status': 'success', 'message': msg}, status.HTTP_200_OK

    except Exception as e:
        # Return a JSON response with status 500 if an unexpected error occurs
        return {'status': 'error', 'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


def restart_project_app_func(request):
    try:
        # Get the 'node_id' from the query parameters of the request
        node_id = request.query_params.get('node_id')

        # Assuming 'get_node_id()' retrieves the expected node_id
        expected_node_id = get_node_id()

        if not node_id:
            return {'status': 'fail', 'message': "Node ID is missing."}, status.HTTP_400_BAD_REQUEST

        if node_id != expected_node_id:
            return {'status': 'fail', 'message': "Invalid Node ID."}, status.HTTP_401_UNAUTHORIZED

        # Your code to restart the project application goes here
        # Example: call_restart_project_app_function()

        msg = "Project application restarted successfully."
        return {'status': 'success', 'message': msg}, status.HTTP_200_OK

    except Exception as e:
        # Return a JSON response with status 500 if an unexpected error occurs
        return {'status': 'error', 'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


def app_health_status_func(request):
    # Get the 'node_id' from the query parameters of the request
    node_id = request.query_params.get('node_id')

    # Assuming 'get_node_id()' retrieves the expected node_id
    expected_node_id = get_node_id()

    if node_id == expected_node_id:
        # Get the health status data from the 'get_json_result_func'
        data = get_json_result_func('IPHealthStatus')
        ihs_response = [i.get('ihs_response') for i in data['IPHealthStatus']]

        # Check if all health statuses are 'Not Found'
        is_server_down = all([True if i == 'Not Found' else False for i in ihs_response])

        # Compose the response message based on server status
        if is_server_down:
            msg = "Server is down."
        else:
            msg = "Server is up."

        # Return a JSON response with status 200
        return {'status': 'success', 'message': msg}, status.HTTP_200_OK
    else:
        # Return a JSON response with status 401 if the node_id is invalid
        return {'status': 'fail', 'message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED
