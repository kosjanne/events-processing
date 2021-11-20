import asyncio
from events import processor, anomaly


async def main(loop):
    await processor.process_events(loop)
    await asyncio.sleep(0.1)
    anomaly.report()


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
