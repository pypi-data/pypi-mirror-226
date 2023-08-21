from flask import Flask, request
import json
import requests
#from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)

#auth = HTTPBasicAuth()

""""
@auth.verify_password
def verify_password(username, password):
    # Check if the username and password are valid
    # Return True if valid, False otherwise
    return username == 'myusername' and password == 'mypassword'
"""

@app.route("/handle_alert", methods=['POST', 'GET'])
def handle_alert():
    print(f"Received alert: {request.data}")
    alerts = json.loads(request.data)["alerts"]
    for a in alerts:
        # Handle the alert as desired
        # if a['labels']['Timestamp'] == list[0]:
        #     print(f"Summary: {a['annotations']['summary']}")
        #     print(f"Customer ID: {a['labels']['CustomerID']}")
        #     print(f"Task ID: {a['labels']['TaskID']}")
        #     print(f"OPE Task ID: {a['labels']['OpeTaskID']}")
        #     print(f"Task Name: {a['labels']['TaskName']}")
        #     print(f"Timestamp: {a['labels']['Timestamp']}")
        #     print(f"EndsAt: {a['labels']['endsAt']}")
        #     summary = a['annotations']['summary']
        #     description = a['annotations']['description'] + " for " + a['labels']['TaskName'] + "." + "CustomerID:" + \
        #                   a['labels']['CustomerID'] + "." + "Error:" + a['labels']['Error'] + "." + "TaskID:" + \
        #                   a['labels']['TaskID'] + "." + "OpeTaskID:" + a['labels']['OpeTaskID'] + "." + "Timestamp:" + \
        #                   a['labels']['Timestamp'] + "."
        #     message = "/jira create bug " + summary + "\n" + description
        #     payload = {
        #         "text": message
        #     }
        #     response = requests.post(
        #         "https://hooks.slack.com/services/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",
        #         data=json.dumps(payload))
        message = a["annotations"]["description"]
        payload = {
            "text": message
        }
        # #cds-vmware-alerts
        response = requests.post(
            "https://hooks.slack.com/services/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",
            data=json.dumps(payload))
        print(f"response: {response}")

    return "Ok"


if __name__ == '__main__':
    server = app.run('172.17.29.165', 5001)
    print('Starting the server')
    server.serve_forever()

# http://127.0.0.1:5000/home


"""
After starting this, start alert manager, promethus server, and export_alert_metrics.py
aafak@aafak-virtual-machine:~$ python3  alert_reciver.py
 * Serving Flask app 'alert_rec'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://172.17.29.165:5001
Press CTRL+C to quit

Received alert: b'{"receiver":"web\\\\.hook","status":"firing",
"alerts":[{"status":"firing","labels":{"alertname":"vmware_vcentre_reg_failure",
"customer_id":"2","hypervisor_manager":"hyper-v","instance":"localhost:8080","
job":"fast_api_py_app","owner":"glbr-vmware-protection","severity":"critical","source":"cloud"},
"annotations":{"description":"vCenter register failure alert","summary":"vCenter register failed"},
"startsAt":"2023-08-18T07:01:57.562Z","endsAt":"0001-01-01T00:00:00Z",
"generatorURL":"http://WHDCIS4TDR:9090/graph?g0.expr=hm_register_failure_alert+%3D%3D+1\\u0026g0.tab=1",
"fingerprint":"25e0957ca5f63e33"},
{"status":"firing",
"labels":{"alertname":"vmware_vcentre_reg_failure","customer_id":"4",
"hypervisor_manager":"hyper-v","instance":"localhost:8080","job":"fast_api_py_app",
"owner":"glbr-vmware-protection","severity":"critical","source":"cloud"},
"annotations":{"description":"vCenter register failure alert","summary":"vCenter register failed"},
"startsAt":"2023-08-18T07:00:42.562Z","endsAt":"0001-01-01T00:00:00Z",
"generatorURL":"http://WHDCIS4TDR:9090/graph?g0.expr=hm_register_failure_alert+%3D%3D+1\\u0026g0.tab=1",
"fingerprint":"2aaa663ad7329a75"}],"groupLabels":{"alertname":"vmware_vcentre_reg_failure"},
"commonLabels":{"alertname":"vmware_vcentre_reg_failure","hypervisor_manager":"hyper-v",
"instance":"localhost:8080","job":"fast_api_py_app","owner":"glbr-vmware-protection",
"severity":"critical","source":"cloud"},"commonAnnotations":{"description":"vCenter register failure alert",
"summary":"vCenter register failed"},"externalURL":"http://WHDCIS4TDR:9093",
"version":"4","groupKey":"{}:{alertname=\\"vmware_vcentre_reg_failure\\"}","truncatedAlerts":0}\n'
response: <Response [200]>
response: <Response [200]>
172.17.160.160 - - [18/Aug/2023 13:23:13] "POST /handle_alert HTTP/1.1" 200 -


"""