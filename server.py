import socket


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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('made socket')

host = socket.gethostname()
port = 8080

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

        try:
            f = open(filepath_to_serve, 'rb')
            response_data = f.read()
            f.close()
            response_header = generate_headers(200, len(response_data))

        except Exception as e:
            print("file not found. serving 404 page.")
            response_header = generate_headers(404, 0)

        f = open(filepath_to_serve, 'rb')

        response = response_header.encode() + response_data
        f.close()

        client.send(response)
    client.close()
