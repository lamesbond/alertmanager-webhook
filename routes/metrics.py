from flask import Blueprint
from prometheus_client import Gauge, generate_latest

import global_vars
from flask import Response

alerts_for_firing = Gauge('alerts_for_firing','已经推送的告警信息',['ID','status','name','instance','description','startsat'])

app_metrics = Blueprint("app_metrics",__name__)
@app_metrics.route('/metrics')
def metrics():
    try:
        for key in global_vars.alert_dict:
            alerts_for_firing.labels(ID=key,status=str(global_vars.alert_dict[key]['status']),name=global_vars.alert_dict[key]['alertname'],instance=global_vars.alert_dict[key]['alertinstance'],description=global_vars.alert_dict[key]['alertdesc'],startsat=global_vars.alert_dict[key]['alertstartsat']).set(1)
        return Response(generate_latest(alerts_for_firing), mimetype='text/plain')
    finally:
        alerts_for_firing.clear()