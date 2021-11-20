anomalies = {}


def new_anomaly(event):
    device = event["deviceId"]
    if device in anomalies:
        anomalies[device] = anomalies[device] + 1
    else:
        anomalies[device] = 1


def report():
    print(anomalies)
