import asyncio
from AccessUrl import AccessUrl
import signal
import sys

async def shutdown(loop):
    tasks = [task for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    asyncio.ensure_future(asyncio.gather(*tasks))
    loop.stop()

		
loop = asyncio.get_event_loop()

#KeyBoardInterrupt
s = signal.SIGINT
loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(loop)))       

access = AccessUrl(loop=loop, file_in = sys.argv[1], file_out = sys.argv[2])

async def constant_update():
    while True:
        await access()
        await asyncio.sleep(3, loop=loop)

task = loop.create_task(constant_update())
loop.run_forever()
