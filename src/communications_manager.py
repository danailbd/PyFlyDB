import logging
import socket
import sys
from threading import Thread

# TODO proper SIGUP handling (close connections ?)

### SUPPORTS ###
# Support only UTF-8 messages
# A message must end on ; in order to be processed
# Parallel request processing
###

logging.basicConfig(
    level=logging.NOTSET,
    format='%(threadName)10s %(name)18s: %(message)s',
    stream=sys.stderr
)

Logger = logging.getLogger('Communications')

HOST = ''  # Symbolic name meaning all available interfaces (lo, eth0, ...)
PORT = 50003  # Arbitrary non-privileged port
MAX_CONNECTIONS = 2
QUERY_END_SYMBOL = ';'
UTF8 = 'utf-8'


# XXX testing
class DummyRepeaterProcessor:
    def process(self, query):
        Logger.debug(query)
        return query


def is_request_end(data):
    return data.strip()[-1] == QUERY_END_SYMBOL


class SocketCommunicationsManager:
    def __init__(self, query_processor=DummyRepeaterProcessor):
        self.processor = query_processor
        self.connection_trds = []

    # TODO rename
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            Logger.info('Socket created: %s:%s', HOST or 'ALL', PORT)
            s.listen(1)
            while True:
                Logger.info('Listening ...')
                conn, addr = s.accept()

                t = Thread(target=self.connection_worker, args=(conn, addr))
                t.start()
                self.connection_trds.append(t)
            # TODO send signals to threads upon close

            # TODO is this needed ?
            for t in self.connection_trds:
                t.join()

    def connection_worker(self, conn, addr):
        """The assigned worker for the established connection."""

        def process_request(query):
            Logger.debug('Processing request: %s', query)
            result = self.processor.process(query[:-1])

            print('Sending result ...')
            conn.sendall(bytearray(result, encoding=UTF8))

        Logger.info('Connections established: %s', conn)
        with conn:
            Logger.info('Connected by %s', addr)
            query_builder = []
            while True:
                data = str(conn.recv(1024), encoding=UTF8)
                if not data:
                    # on connection close
                    break
                query_builder.append(data)
                Logger.debug('Data: %s', data)
                # check and run
                # executor
                if is_request_end(data):
                    process_request(''.join(query_builder))

            Logger.info('Connection closed %s', addr)

    # TODO what to do on connection close ?
    def close_connection(self):
        pass


if __name__ == '__main__':
    SocketCommunicationsManager(DummyRepeaterProcessor()).run()
