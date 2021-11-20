from events import profile


def is_within(event):
    value = event["data"]["value"]
    lower, upper = _fetch_threshold(event)
    return value <= upper and value >= lower


def _fetch_threshold(event):
    device_profile = profile.fetch_for_device(event)
    threshold = device_profile["thresholds"]
    return (threshold["lower"], threshold["upper"])
