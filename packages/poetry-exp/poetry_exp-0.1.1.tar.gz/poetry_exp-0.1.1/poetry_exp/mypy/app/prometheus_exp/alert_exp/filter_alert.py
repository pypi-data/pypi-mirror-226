from datetime import datetime, timedelta
from time import sleep
alert_dict = {}


def send_alert_required(customer_id, alert_type):
    send_alert_required = True
    print(f'alert_dict: {alert_dict}')
    print(f'customer_id: {customer_id}, alert_type: {alert_type}')

    if (customer_id, alert_type) in alert_dict:
        alert_details = alert_dict.get((customer_id, alert_type))
        last_sent_time = alert_details.get("timestamp")
        current_time = datetime.utcnow()
        print(f'@@@@@last_sent_time: {last_sent_time}, current_time: {current_time}, diff: {(current_time - last_sent_time).seconds} sec')
        #if (current_time - last_sent_time).days > 1:
        if (current_time - last_sent_time).seconds > 1:
            print('24 hours have passed')
        else:
            print('Date is within 24 hours!')
            send_alert_required = False
    print(f'send_alert_required: {send_alert_required}')
    return send_alert_required


def send_alert(customer_id, alert_type):
    #previous_date_time = datetime.today() - timedelta(days=2)
    if send_alert_required(customer_id, alert_type):
        print(f"Alert sent, customer_id: {customer_id}, alert_type: {alert_type}")
        alert_dict[(customer_id, alert_type)] = {
            "timestamp": datetime.utcnow()
        }


if __name__ == '__main__':
    alert_types = ['Snapshot', 'Backup']
    for i in range(4):
        sleep(1)
        send_alert(i, alert_types[i%2])

    for i in range(4):
        sleep(1)
        send_alert(i, alert_types[i%2])