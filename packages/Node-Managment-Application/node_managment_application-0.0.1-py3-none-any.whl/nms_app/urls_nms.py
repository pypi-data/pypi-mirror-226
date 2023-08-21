from django.urls import path

from nms_app.nms_services import url_check_scheduler
from nms_app.views import *

urlpatterns = [
    path('setup_project/', SetupProject.as_view(), name='setup_project'),
    path('start_project_app/', StartProjectApp.as_view(), name='start_project_app'),
    path('stop_project_app/', StopProjectApp.as_view(), name='stop_project_app'),
    path('restart_project_app/', RestartProjectApp.as_view(), name='restart_project_app'),
    # path('get_node_ip_and_location/', GetNodeIPAndLocation.as_view(), name='get_node_ip_and_location'),
    path('upgrade_node/', UpgradeNode.as_view(), name='upgrade_node'),
    path('get_system_config/', GetSystemConfig.as_view(), name='get_node_status'),
    path('get_node_status/', GetNodeStatus.as_view(), name='get_node_id'),
    path('join_network/', JoinNetwork.as_view(), name='join_network'),
    path('leave_network/', LeaveNetwork.as_view(), name='leave_network'),
    path('set_firewall_request/', SetFireWallRequest.as_view(), name='set_firewall_request'),
    path('get_log/', GetLog.as_view(), name='get_log'),
    #path('get_node_ip/', GetNodeIP.as_view(), name='get_node_ip'),
    #path('get_node_location/', GetNodeLocation.as_view(), name='get_node_location'),
    # path('update_config/', UpdateConfig.as_view(), name='update_config'),
    path('get_node_id/', GetNodeId.as_view(), name='get_node_id'),
    path('app_health_status/', AppHealthStatus.as_view(), name='check_health_status'),
    path('get_cluster_nodes_info/', GetClusterNodesInfo.as_view(), name='check_health_status'),
    path('get_transaction_info/', GetTransactionInfo.as_view(), name='get_transaction_info'),
    path('get_transaction_details/', GetTransactionDetails.as_view(), name='get_transaction_details'),
    path('get_full_health_status/', GetFullHealthStatus.as_view(), name='get_full_health_status'),
    #path('list_of_open_ports/', ListOfOpenPorts.as_view(), name='get_node_id'),
    #path('file_download_status/', FileDownloadStatus.as_view(), name='get_node_id'),
    path('get_nms_version/', GetNmsVersion.as_view(), name='get_node_id'),
    path('get_application_version/', GetApplicationVersion.as_view(), name='get_node_id'),
    path('reset_project/', ResetProject.as_view(), name='reset_project'),
    path('', url_check_scheduler.hit_url),

]
