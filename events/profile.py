profiles = {
    "abc": [{"type": "load", "thresholds": {"upper": 80, "lower": 20}, "window": 10}]
}

# In real life this would need some thought. We might call this a lot so we probably
# can't fetch device profile from server everytime this is called. So we might refresh
# profiles only every now and then or something.
def fetch_for_device(event):
    profile = profiles[event["deviceId"]]
    type = event["data"]["type"]
    return next((x for x in profile if x["type"] == type), None)
