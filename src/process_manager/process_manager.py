import asyncio
import queue
from enum import Enum

import concurrent.futures

from src.query_processor.query_ast.plan import Operation

# TODO set some state of operations
# TODO stop threads on exit !

DEFAULT_PROCESSES_LIMIT = 3
QUEUE_MAX_SIZE = 30
MAX_BLOCK_TIME = 60  # seconds


class TaskStatuses(Enum):
    NEW = 'new'
    WAITING = 'waiting'
    RUNNING = 'running'
    FINISHEd = 'finished'


class OperationTask:
    def __init__(self, operation, future=None):
        """
        An operation task.
        Args:
            operation:
            future (Future): Whether a notification to be sent
        """
        self.operation = operation
        self.future = future
        self.state = TaskStatuses.NEW


### MAIN ###


class ProcessManager(concurrent.futures.ThreadPoolExecutor):
    def __init__(self, processes_limit=DEFAULT_PROCESSES_LIMIT):
        super().__init__(processes_limit)

    def submit(self, operation):
        """
        Schedules an operation for execution
        Args:
            operation (Operation):

        Returns:
            Future:
        """
        return super().submit(operation.method, *operation.args)

    def operation_worker(self):
        # get task
        pass
