import asyncio
from events import threshold, profile, anomaly

random_events = [
    {"deviceId": "abc", "data": {"type": "load", "value": 56}},
    {"deviceId": "abc", "data": {"type": "load", "value": 86}},
    {"deviceId": "123", "data": {"type": "load", "value": 16}},  # 123 anomaly 1 start
    {"deviceId": "abc", "data": {"type": "load", "value": 55}},
    {"deviceId": "abc", "data": {"type": "load", "value": 55}},
    {"deviceId": "abc", "data": {"type": "load", "value": 55}},
    {"deviceId": "123", "data": {"type": "load", "value": 16}},  # 123 anomaly 2 start
    {"deviceId": "123", "data": {"type": "load", "value": 16}},
    {"deviceId": "abc", "data": {"type": "load", "value": 55}},
    {"deviceId": "abc", "data": {"type": "load", "value": 55}},
    {"deviceId": "123", "data": {"type": "load", "value": 86}},
    {"deviceId": "123", "data": {"type": "load", "value": 16}},
    {"deviceId": "123", "data": {"type": "load", "value": 56}},
    {"deviceId": "abc", "data": {"type": "load", "value": 56}},
    {"deviceId": "abc", "data": {"type": "load", "value": 56}},
    {"deviceId": "abc", "data": {"type": "load", "value": 86}},  # abc anomaly 1 start
    {"deviceId": "abc", "data": {"type": "load", "value": 16}},
    {"deviceId": "abc", "data": {"type": "load", "value": 16}},
    {"deviceId": "abc", "data": {"type": "load", "value": 16}},
    {"deviceId": "abc", "data": {"type": "load", "value": 16}},
    {"deviceId": "abc", "data": {"type": "load", "value": 16}},
    {"deviceId": "abc", "data": {"type": "load", "value": 16}},
    {"deviceId": "123", "data": {"type": "load", "value": 16}},  # 123 anomaly 3 start
    {"deviceId": "abc", "data": {"type": "load", "value": 16}},
    {"deviceId": "abc", "data": {"type": "load", "value": 86}},
    {"deviceId": "abc", "data": {"type": "load", "value": 16}},
    {"deviceId": "abc", "data": {"type": "load", "value": 56}},
    {"deviceId": "abc", "data": {"type": "load", "value": 56}},
    {"deviceId": "abc", "data": {"type": "load", "value": 56}},
]
timer_handles = {}

# unclear: if a device reports an anomaly and sends no new events for a while,
# i.e. device stays in faulty state, should we keep posting anomaly reports until
# it goes back to normal? Currently we don't.


async def process_events(loop):
    print("processing events", end="", flush=True)
    for event in random_events:
        print(".", end="", flush=True)
        _process_event(event, loop)
        await asyncio.sleep(0.5)  # simulating delay between events
    print()  # just a new line for console


def _process_event(event, loop):
    if threshold.is_within(event):
        _reset_event_timer(event)
    else:
        _start_event_timer(event, loop)


def _reset_event_timer(event):
    device = event["deviceId"]
    if device in timer_handles:
        timer_handles[device].cancel()
        timer_handles.pop(device)


def _start_event_timer(event, loop):
    device = event["deviceId"]
    if not device in timer_handles:
        device_profile = profile.fetch_for_device(event)
        timer_handles[device] = loop.call_later(
            device_profile["window"], _report_new_anomaly_callback, event
        )


def _report_new_anomaly_callback(event):
    anomaly.new_anomaly(event)
    _reset_event_timer(event)
