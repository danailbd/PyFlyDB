import asyncio

from src.communications_manager import SocketCommunicationsManager
from src.process_manager.process_manager import ProcessManager
from src.query_processor.query_processor import QueryProcessor

loop = asyncio.get_event_loop()
loop.run_forever()

# communication_manager = None
# query_engine = None
# plan_executor = None
# process_manager = None

"""
Set up environment
"""


def init():
    # XXX
    # storage_manager = StorageManager()
    process_manager = ProcessManager()
    query_processor = QueryProcessor(process_manager=process_manager,
                                     storage_manager=None) #,storage_manager)

    communications_manager = SocketCommunicationsManager(query_processor)
    # Initialize the main process
    communications_manager.run()


if __name__ == '__main__':
    init()
