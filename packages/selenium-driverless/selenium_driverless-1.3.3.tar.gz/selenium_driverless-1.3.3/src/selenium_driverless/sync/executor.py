import asyncio
import threading
from concurrent.futures import Future
import functools


class Executor(threading.Thread):
    def __init__(self, loop=None):
        super().__init__()
        if not loop:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        self.loop = loop
        self.start()

    def run(self):
        self.loop.run_forever()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.join()

    def _add_task(self, future, coro):
        task = self.loop.create_task(coro)
        future.set_result(task)

    def add_task(self, coro) -> asyncio.Future:
        future = Future()
        p = functools.partial(self._add_task, future, coro)
        self.loop.call_soon_threadsafe(p)
        return future

    # noinspection PyProtectedMember
    def exec_task(self, coro):
        res = self.add_task(coro).result()
        if res._exception:
            raise res._exception
        else:
            return res._result

    def cancel(self, task):
        self.loop.call_soon_threadsafe(task.cancel)

    @property
    def is_async(self):
        return self.ident == threading.current_thread().ident
