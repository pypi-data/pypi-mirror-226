from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from nms_app.api_services.node_apis import transaction_count
from nms_app.nms_services.get_json_result import get_json_result_func, put_json_result_func
from nms_project_settings.settings import IP_ADD


def hit_url():
    url = f"http://{IP_ADD}:19001/ads/ping"  # Replace with the desired URL
    try:
        response = requests.get(url)
        res = response.json()
    except:
        res = "Not Found"

    data = get_json_result_func('IPHealthStatus')

    if len(data['IPHealthStatus']) > 2:
        data['IPHealthStatus'] = data['IPHealthStatus'][-2:]
    dt = {
        "ihs_url": url,
        "ihs_response": res,
        "ihs_cr_dt": datetime.now().isoformat()
    }
    data['IPHealthStatus'].append(dt)
    put_json_result_func('IPHealthStatus', data)


def hit_transaction_info_url():
    count, err = transaction_count()
    data = get_json_result_func('TransactionDetails')
    data.update({"td_cr_timestamp": datetime.now().isoformat(),
                 "td_count": count,
                 "td_api_status": err,
                 })

    put_json_result_func("TransactionDetails", data)


scheduler = BackgroundScheduler()
scheduler.add_job(hit_url, 'interval', seconds=30)
scheduler.add_job(hit_transaction_info_url, 'interval', hours=1)
scheduler.start()
