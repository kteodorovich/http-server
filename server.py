#!/usr/bin/env python3
import socket
import os
import sys
import re


def generate_headers(response_code, content_length):
    header = ''

    if response_code == 200:
        header += 'HTTP/1.1 200 OK\r\n'
        header += 'Content-length ' + str(content_length) + '\r\n'
    elif response_code == 404:
        header += 'HTTP/1.1 404 Not Found\r\n'

    header += 'Server: Simple-Python-Server\r\n'
    header += 'Connection: close\r\n\r\n'  # Signal that connection will be closed after completing the request
    return header


def main():
    if len(sys.argv) != 2:
        print('Server requires one CLI argument in format `hostname:port`', file=sys.stderr)
        return

    args = re.match('([a-zA-Z0-9.]+):([0-9]+)', sys.argv[1])
    if args is None:
        print('CLI argument must be in format `hostname:port`', file=sys.stderr)
        return

    host = args.group(1)
    port = int(args.group(2))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('made socket')

    s.bind((host, port))

    s.listen(5)
    print('listening...\n')

    while True:
        client, address = s.accept()
        print('got connection from %s' % str(address))

        PACKET_SIZE = 1024
        print("CLIENT", client)

        # receive client data, decode
        data = client.recv(PACKET_SIZE).decode()

        request_method = data.split(' ')[0]

        if request_method == 'GET':
            file_requested = data.split(' ')[1]
            filepath_to_serve = '.' + file_requested

            print("serving web page [{fp}]".format(fp=filepath_to_serve))
            response_data = ''

            if os.path.isdir(filepath_to_serve):
                response_data = 'Directory listing of ' + filepath_to_serve + ':\n\n'.join(os.listdir(filepath_to_serve))
                response_header = generate_headers(200, len(response_data))

            else:
                try:
                    with open(filepath_to_serve, 'rb') as f:
                        response_data = f.read()
                        response_header = generate_headers(200, len(response_data))

                except EnvironmentError:
                    print("file not found. serving 404 page.")
                    response_header = generate_headers(404, 0)

            response = response_header.encode() + response_data.encode()

            client.send(response)
        client.close()


if __name__ == '__main__':
    main()
