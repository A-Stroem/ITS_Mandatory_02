#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *

server_port = 15000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print('The server is ready to receive')
while True:
    connection_socket, addr = server_socket.accept()
    msg = connection_socket.recv(2048)
    modified_msg = msg.upper()
    connection_socket.send(modified_msg)
    connection_socket.close()