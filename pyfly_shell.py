# Echo client program
import socket

# Cap response to 2048 bytes

QUERY_END_SYMBOL = ';'

PROMPT = '> '

HOST = 'localhost'  # The remote host
PORT = 50003  # The same port as used by the server
print('Welcome to PyFlyDB shell. Make your queries.')
print('Use Ctrl+C to exit.')
print('Establishing connection')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
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
            line = input(PROMPT if not query else '... ').strip()
            query.append(line)
        # Send the final query
        s.sendall(bytearray(' '.join(query), encoding='utf-8'))
        print('Waiting response ...')
        data = s.recv(2048)
        print('Received', repr(data))
