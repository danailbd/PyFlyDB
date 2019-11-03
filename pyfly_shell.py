# Echo client program
import socket

# Cap response to 2048 bytes

QUERY_END_SYMBOL = ';'

PROMPT = '> '

HOST = 'localhost'  # The remote host
PORT = 50003  # The same port as used by the server


def default_input_method(cur_query):
    return input(PROMPT if not cur_query else '... ').strip()


class PyflyShell:
    def __init__(self, host=HOST, port=PORT, input_method=default_input_method):
        """"""
        self.input_method = input_method
        self.host = host
        self.port = port

    def run(self):
        print('Welcome to PyFlyDB shell. Make your queries.')
        print('Use Ctrl+C to exit.')
        print('Establishing connection')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
            except OSError as e:
                s.close()
                print(e, 'Exiting ...')
                print('Try restarting. ')
                exit()
            print('Connected!')
            print('Enter your commands')

            # Prompt loop
            while True:
                query = []
                line = ''
                while not line or line[-1] != QUERY_END_SYMBOL:
                    line = self.input_method(query)
                    query.append(line)
                # Send the final query
                s.sendall(bytearray(' '.join(query), encoding='utf-8'))
                print('Waiting response ...')
                data = s.recv(2048)
                print('Received', repr(data))


if __name__ == '__main__':
    PyflyShell().run()
