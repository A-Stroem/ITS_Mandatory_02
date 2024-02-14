#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *

server_port = 15000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)

print('The server is', server_port ,'ready to receive')

def get_file(path):

    try:
        file = open("." + path,"rb")
        content = file.read()
    except Exception as e:
        print(e)
        file = open("./error.html", "rb")
        content = file.read()
    return content

def http_handler(request):
    request = request.split(" ") #GET /index.html HTTP/1.0/r/n/r/n

    method = request[0]
    path = request[1]
    protocol = request[2]

    print(f"Protocol: {protocol}") 

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
    connection_socket.close()
