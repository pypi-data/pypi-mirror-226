from drf_yasg import openapi

from nms_app.nms_services.api_key_valdation import get_node_id
from nms_project_settings.settings import IP_ADD

authorization = [
    openapi.Parameter(
        'authorization',
        openapi.IN_HEADER,
        description='api_key',
        type=openapi.TYPE_STRING,
        default='AR12532DE@#GH&67GF24GH45532$##FGG',
        required=True)
    # Add more parameters as needed
]

ls_of_node = authorization + [
    openapi.Parameter(
        name='node_id',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='node_id',
        default=get_node_id(),
        required=True,
    ),
    # Add more parameters as needed
]

ref_id_parameter = [
    openapi.Parameter(
        name='ref_id',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='ref_id',
        default='',
        required=True,
    ),
    # Add more parameters as needed
]

node_category_parameter = [
    openapi.Parameter(
        name='node_category',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='eg. GUARDIAN, MASTER',
        default='',
        required=True,
    ),
    # Add more parameters as needed
]

ls_of_server_ip = [
    openapi.Parameter(
        name='server_ip',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='server_ip',
        default=IP_ADD,
        required=True,
    ),
    # Add more parameters as needed
]
port_number = [
    openapi.Parameter(
        name='port_number',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='port_number',
        default=19001,
        required=True,
    ),
    # Add more parameters as needed
]

port_number1 = [
    openapi.Parameter(
        name='public_port',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='port_number',
        default=9085,
        required=True,
    ),
    openapi.Parameter(
        name='p2p_port',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='port_number',
        default=9086,
        required=True,
    ),
    # Add more parameters as needed
]

ls_of_node_set_firewall_request = ls_of_node + [
    openapi.Parameter(
        name='open_ports',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='network_status',
        default='75,2009,2000',
        required=True,
    )
]

# ls_of_node_set_firewall_request = [
#                                       openapi.Parameter(
#                                           name='network_status',
#                                           in_=openapi.IN_QUERY,
#                                           type=openapi.TYPE_INTEGER,
#                                           description='network_status',
#                                           default='75',
#                                           required=True,
#                                       ),
#                                       openapi.Parameter(
#                                           name='open_ports_protocol',
#                                           in_=openapi.IN_QUERY,
#                                           type=openapi.TYPE_STRING,
#                                           description='open_ports_protocol',
#                                           default='TCP',
#                                           required=True,
#                                       ),
#                                       openapi.Parameter(
#                                           name='open_ports_port_number',
#                                           in_=openapi.IN_QUERY,
#                                           type=openapi.TYPE_INTEGER,
#                                           description='open_ports_port_number',
#                                           default='1234',
#                                           required=True,
#                                       ),
#                                       openapi.Parameter(
#                                           name='close_ports_protocol',
#                                           in_=openapi.IN_QUERY,
#                                           type=openapi.TYPE_STRING,
#                                           description='close_ports_protocol',
#                                           default='TCP',
#                                           required=True,
#                                       ),
#                                       openapi.Parameter(
#                                           name='close_ports_port_number',
#                                           in_=openapi.IN_QUERY,
#                                           type=openapi.TYPE_INTEGER,
#                                           description='close_ports_port_number',
#                                           default='1235',
#                                           required=True,
#                                       ),
#                                       # Add more parameters as needed
#                                   ] + ls_of_node

dt_of_response = {
    200: openapi.Response(
        description='Success',
        examples={'application/json': {'status': 'Success', 'message': 'Registration Successful'}},
    ),
    400: openapi.Response(
        description='Bad Request',
        examples={'application/json': {'status': 'Fail', 'message': 'Invalid Parameters'}},
    ),
    # Add more response codes and schemas as needed
}
