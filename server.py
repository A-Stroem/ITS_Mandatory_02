#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *
from datetime import *
import logging

logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(message)s', datefmt='[%d/%b/%Y:%H:%M:%S +0000]')
logger = logging.getLogger(__name__)

server_port = 15000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)

print('The server is', server_port ,'ready to receive')

def get_file(path):

    try:
        file = open("." + path,"rb")
        content = file.read()
        return b"HTTP/1.1 200 OK\r\n\r\n" + content
    except FileNotFoundError as e:
        file = open("./error.html", "rb")
        content = file.read()
        return b"HTTP/1.1 404 Not Found\r\n\r\n" + content
    except Exception as e:
        return b"HTTP/1.1 500 Internal Server Error\r\n\r\nServer error"

def http_handler(request):
    request = request.split()

    method = request[0]
    path = request[1]
    protocol = request[2]

    if method != "GET":
        return b"HTTP/1.1 400 Bad Request\r\n\r\n"
    if method == "GET":        
        if protocol == "HTTP/1.0":
            response = b"HTTP/1.0 200 OK\r\n\r\n" + get_file(path)
            return response
        if protocol == "HTTP/1.1":
            response = b"HTTP/1.1 200 OK\r\n\r\n" + get_file(path)
            return response
    else:
        return get_file('/error.html')

    # Add this line to return an error response when the method is not GET or the protocol is not supported
    return b"HTTP/1.1 400 Bad Request\r\n\r\n"

while True:
    connection_socket, addr = server_socket.accept()
    request = connection_socket.recv(2048).decode()
    response = http_handler(request)
    connection_socket.sendall(response)

    logger.info('%s - - %s "%s %s %s" %s %s',
                addr[0], # Client IP address
                datetime.now().strftime('[%d/%b/%Y:%H:%M:%S +0000]'), # Current date and time
                request.split()[0], # Request method
                request.split()[1], # Request URI
                request.split()[2], # Response status
                response.decode().split()[1],
                len(response) # Response size
               )
    connection_socket.close()
