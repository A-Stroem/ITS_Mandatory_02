#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *
from logging import *

server_port = 15000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)

print('The server is', server_port ,'ready to receive')

#Set up logging format to apache format from the logging import
# basicConfig(filename='access.log', level=INFO, format='%(message)s')

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
    request = request.split() #GET /index.html HTTP/1.0/r/n/r/n

    method = request[0]
    path = request[1]
    protocol = request[2]

    if method != "GET":
        return b"HTTP/1.1 400 Bad Request\r\n\r\n"

    if method == "GET":        
        if protocol == "HTTP/1.0":
            if "HTTP/1.1" in response:
                response = response.replace("HTTP/1.1", "HTTP/1.0")
            response = get_file(path)
            return response
        if protocol == "HTTP/1.1":
            response = get_file(path)
            if "HTTP/1.0" in response:
                response = response.replace("HTTP/1.0", "HTTP/1.1")
            return response

while True:
    connection_socket, addr = server_socket.accept()
    request = connection_socket.recv(2048).decode()
    response = http_handler(request)
    connection_socket.sendall(response)
    connection_socket.close()



