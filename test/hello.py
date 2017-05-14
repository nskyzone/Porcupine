# # Example of the queue how to work
# import asyncio
# from asyncio import Queue
#
# async def work(q):
#     while True:
#         i = await q.get()
#         try:
#             print(i)
#             print('q.qsize(): ', q.qsize())
#         finally:
#             q.task_done()
#
# async def run():
#     q = Queue()
#     await asyncio.wait([q.put(i) for i in range(10)])
#     tasks = [asyncio.ensure_future(work(q))]
#     print('wait join')
#     # await q.join()
#     while(True):1
#     print('end join')
#     for task in tasks:
#         task.cancel()
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(run())
#     loop.close()
import time
while True:
    try:
        print('in try')
        time.sleep(2)
        continue

    except Exception as e:
        print('in except')
    finally:
        print('in finally')