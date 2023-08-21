from rest_framework import serializers

class GetnodeIdAndProjectId(serializers.Serializer):
    node_id = serializers.IntegerField(required=True)
    project_id = serializers.IntegerField(required=True)

class SetFirewallRequestSerializer(serializers.Serializer):
    node_id = serializers.IntegerField(required=True)
    project_it = serializers.CharField(required=True)
    network_status = serializers.IntegerField(required=True)
    open_ports_protocol = serializers.CharField(required=True)
    open_ports_port_number = serializers.IntegerField(required=True)
    close_ports_protocol = serializers.CharField(required=True)
    close_ports_port_number = serializers.IntegerField(required=True)



