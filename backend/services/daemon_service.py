import time
import logging
import threading
from backend.services.secure_storage_service import SecureKeyManager
from backend.services.error_handler import ErrorHandler
from backend.services.reporter import Reporter

class DaemonService(threading.Thread):
    def __init__(self, task_queue, storage_service):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.storage_service = storage_service
        self.error_handler = ErrorHandler(storage_service)
        self.reporter = Reporter(storage_service)
        self.running = True
        self.logger = logging.getLogger("DaemonService")

    def run(self):
        self.logger.info("Daemon started.")
        while self.running:
            try:
                # Check for reporting
                self.reporter.check_and_report()
                
                task = self.task_queue.get(timeout=1)
                if task:
                    self.logger.info(f"Executing task: {task.id}")
                    self.storage_service.update_task_state(task.id, "IN_PROGRESS")
                    # Task execution logic
                    task.execute()
                    self.storage_service.update_task_state(task.id, "COMPLETED")
            except Exception as e:
                self.logger.error(f"Daemon error: {e}")
                self.error_handler.handle(e)
                time.sleep(5) # Backoff on error

    def stop(self):
        self.running = False
