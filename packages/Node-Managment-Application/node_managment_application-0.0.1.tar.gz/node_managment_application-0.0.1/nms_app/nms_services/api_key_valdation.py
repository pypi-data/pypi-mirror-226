import datetime

from nms_app.models import NodeDetails
from nms_project_settings.settings import API_KEY


def custom_api_key_validation(input_key):
    if input_key:
        if input_key.upper() == API_KEY:
            return {"status": True, "Message": "Successfully Authenticated."}
        else:
            return {"status": False, "Message": "Invalid API key."}
    else:
        return {"status": False, "Message": "Blank API key provided."}

def get_node_id():
    try:
        all_values = NodeDetails.objects.all()
        if not all_values:
            node_id = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
            unique_value = NodeDetails(nms_node_id=node_id)
            unique_value.save()
        else:
            node_id = str(all_values.first().nms_node_id)
        return node_id
    except:
        return ''
