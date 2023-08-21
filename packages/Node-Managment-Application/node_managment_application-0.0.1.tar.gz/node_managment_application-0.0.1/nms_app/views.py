import shutil

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from nms_app.api_services.network_api import join_network_func, leave_network_func, gaurdian_join_network_func
from nms_app.api_services.node_apis import get_node_ip_func, get_node_location_func, upgrade_node_func, \
    get_cluster_nodes_info, get_transaction_info_func, get_system_config_func, get_node_status_func, \
    get_detailed_info_func, get_transaction_details_func
from nms_app.api_services.setup_project_api import project_setup_func
from nms_app.api_services.project_app_apis import start_project_app_func, stop_project_app_func, \
    restart_project_app_func, app_health_status_func
from nms_app.nms_services.common_services import run_command
from nms_app.nms_services.get_server_info import get_open_ports
from nms_app.models import SetupProjectDetails
from nms_app.nms_services.api_key_valdation import custom_api_key_validation, get_node_id
from nms_app.swagger_supporting_file import ls_of_node, ls_of_node_set_firewall_request, \
    authorization, node_category_parameter, ref_id_parameter, ls_of_server_ip, port_number, port_number1
from django.db import connection


class SetupProject(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Setup NMS project on node.',
        manual_parameters=ls_of_node + node_category_parameter,
    )
    def post(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = project_setup_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class StartProjectApp(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Start NMS project on node.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = start_project_app_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class StopProjectApp(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Stop the NMS project.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = stop_project_app_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class RestartProjectApp(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Restart the NMS project.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = restart_project_app_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetNodeIP(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Get the NMS project node IP.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = get_node_ip_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetNodeLocation(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Get NMS project node location.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = get_node_location_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class UpgradeNode(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Upgrade the NMS project.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def put(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = upgrade_node_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetNodeStatus(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Get the node property details.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = get_node_status_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetSystemConfig(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Get the node property details.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = get_system_config_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class JoinNetwork(APIView):
    all_tables = connection.introspection.table_names()
    if 'nms_app_setupprojectdetails' in all_tables:
        spd_node_category = SetupProjectDetails.objects.values_list('spd_node_category', flat=True)
    else:
        spd_node_category = ["MASTER"]

    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Join the NMS node.',
        manual_parameters=ls_of_node + ls_of_server_ip + (port_number1 if
        spd_node_category[0] == "GUARDIAN" else port_number) if spd_node_category else
        ls_of_node + ls_of_server_ip + port_number1,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            spd_node_category = SetupProjectDetails.objects.values_list('spd_node_category', flat=True)
            if spd_node_category:
                if spd_node_category[0] == "GUARDIAN":
                    response = gaurdian_join_network_func(request)
                else:
                    response = join_network_func(request)
                return Response(response[0], response[1])
            else:
                return Response({'status': 'fail', 'Message': 'Project not present to join.'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class LeaveNetwork(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Leave the NMS node.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            # spd_node_category = SetupProjectDetails.objects.values_list('spd_node_category', flat=True)

            response = leave_network_func(request)
            # else:
            #     response = leave_network_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetFireWallRequest(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Set the firewall configuration for NMS project.',
        manual_parameters=ls_of_node_set_firewall_request,
        # responses=dt_of_response
    )
    def post(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            node_id = request.query_params.get('node_id')
            if node_id == get_node_id():
                open_ports = request.query_params.get('open_ports')
                req_ports = open_ports.split(',') + [22, 9000]
                if req_ports:

                    for port in req_ports:
                        run_command(f"sudo iptables -A INPUT -p tcp --dport {port} -j ACCEPT")
                        # run_command(f'sudo iptables -F sudo iptables -A INPUT -p tcp -- dport {port} -j ACCEPT')
                    run_command('sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT')
                    run_command('sudo iptables -A INPUT -p tcp -j DROP')
                    return Response({"status": "success", "Message": 'All other ports are closed successfully.'},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'fail', 'Message': "Ports are not provided."},
                                        status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'status': 'fail', 'Message': "Invalid Node Id."},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetLog(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Get the log status project.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            node_id = request.query_params.get('node_id')
            if node_id == get_node_id():
                msg = "log file currently not available."
                return Response({'status': 'success', 'Message': msg}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'fail', 'Message': "Invalid Node Id."},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class UpdateConfig(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Update the node configurations.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def post(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            node_id = request.query_params.get('node_id')
            if node_id == get_node_id():
                msg = "Configurations Successful"
                return Response({'status': 'success', 'Message': msg}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'fail', 'Message': "Invalid Node Id."},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetNodeId(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Get the node id of NMS project.',
        manual_parameters=authorization,
        # responses=dt_of_response
    )
    def post(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            node_id = get_node_id()
            return Response({'status': 'success', 'Node Id': node_id}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class AppHealthStatus(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Check the node utilization details.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def post(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = app_health_status_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class ListOfOpenPorts(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            node_id = request.query_params.get('node_id')
            list_of_ports = get_open_ports()
            if node_id == get_node_id():
                msg = 'List of open ports are ' + ', '.join(list_of_ports)
                return Response({'status': 'success', 'Message': msg}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'fail', 'Message': "Invalid Node Id."},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class FileDownloadStatus(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Setup NMS project on node.',
        manual_parameters=ls_of_node + ref_id_parameter,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            node_id = request.query_params.get('node_id')
            file_ref_id = request.query_params.get('ref_id')
            if node_id == get_node_id():
                file_status = SetupProjectDetails.objects.filter(spd_ref_id=file_ref_id)
                return Response(
                    {'status': 'success', 'Message': str(file_status.values().get()['spd_download_status'])},
                    status=status.HTTP_200_OK)
            else:
                return Response({'status': 'fail', 'Message': "Invalid Node Id."},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetClusterNodesInfo(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Setup NMS project on node.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = get_cluster_nodes_info(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetTransactionInfo(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Setup NMS project on node.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = get_transaction_info_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetFullHealthStatus(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Setup NMS project on node.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            response = get_detailed_info_func(request)
            return Response(response[0], response[1])
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetTransactionDetails(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Setup NMS project on node.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            node_id = request.query_params.get('node_id')
            if node_id == get_node_id():
                response = get_transaction_details_func()
                return Response(response[0], response[1])
            else:
                return Response({'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetNmsVersion(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Setup NMS project on node.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            return Response({'status': 'success', 'Version': '1.0'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetApplicationVersion(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Setup NMS project on node.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            # response = get_transaction_details_func(request)
            return Response({'status': 'success', 'Message': 'Currently version not available.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)


class ResetProject(APIView):
    @swagger_auto_schema(
        tags=['NMS API'],
        operation_description='Remove project from server.',
        manual_parameters=ls_of_node,
        # responses=dt_of_response
    )
    def get(self, request):
        input_key = request.META.get('HTTP_AUTHORIZATION')
        key_validation = custom_api_key_validation(input_key)
        if key_validation['status']:
            spd_node_category = SetupProjectDetails.objects.values_list('spd_node_category', flat=True)
            if spd_node_category:
                path = '/home/ubuntu/L1_App' if spd_node_category[0] == "GUARDIAN" else '/home/ubuntu/L2_App'
                SetupProjectDetails.objects.all().delete()
                try:
                    shutil.rmtree(path, ignore_errors=True)
                    msg = f"{spd_node_category[0]} Project deleted successfully."
                except OSError as error:
                    print(error)
                    msg = f"Directory {path} can not be removed."
            else:
                msg = 'Project not setup yet.'
            return Response({'status': 'success', 'Message': msg}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'fail', 'Message': key_validation['Message']},
                            status=status.HTTP_401_UNAUTHORIZED)
