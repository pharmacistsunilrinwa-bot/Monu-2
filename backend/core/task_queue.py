import asyncio
import logging
import uuid

class TaskQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.logger = logging.getLogger("TaskQueue")

    async def enqueue(self, task_func, *args, **kwargs):
        task_id = str(uuid.uuid4())
        await self.queue.put((task_id, task_func, args, kwargs))
        self.logger.info(f"Task queued: {task_id}")
        return task_id

    async def worker(self):
        while True:
            task_id, func, args, kwargs = await self.queue.get()
            try:
                self.logger.info(f"Processing task: {task_id}")
                await func(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Task {task_id} failed: {e}")
            finally:
                self.queue.task_done()
