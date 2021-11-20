import asyncio
from events import threshold, profile, anomaly

random_events = [
    {"deviceId": "abc", "data": {"type": "load", "value": 56}},
    {"deviceId": "abc", "data": {"type": "load", "value": 86}},
    {"deviceId": "abc", "data": {"type": "load", "value": 16}},
]
timer_handles = {}

loop = asyncio.get_event_loop()


def _process_events():
    for event in random_events:
        _process_event(event)


def _process_event(event):
    if threshold.is_within(event):
        _reset_event_timer(event)
    else:
        _start_event_timer(event)


def _reset_event_timer(event):
    device = event["deviceId"]
    if device in timer_handles:
        timer_handles[device].cancel()
        timer_handles.pop(device)


def _start_event_timer(event):
    device = event["deviceId"]
    if not device in timer_handles:
        device_profile = profile.fetch_for_device(event)
        timer_handles[device] = loop.call_later(
            device_profile["window"], anomaly.new_anomaly, event
        )


async def main():
    _process_events()
    await asyncio.sleep(0.1)
    anomaly.report()


loop.run_until_complete(main())
