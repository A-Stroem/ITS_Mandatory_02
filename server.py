#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *
from logging import *

# Change filename as needed
# handler = FileHandler('access.log') 
# handler.setLevel(WARNING)

# formatter = Formatter('%(asctime)s - %(levelname)s - %(name)s - [%(remote_addr)s] "%(request_line)s" %(status)s %(body_bytes_sent)s')
# handler.setFormatter(formatter)

# logger = getLogger()
# logger.setLevel(INFO)
# logger.addHandler(handler)

# logger.info('Server started')

formatter = Formatter('%(asctime)s - %(levelname)s - %(name)s - [%(remote_addr)s] "%(request_line)s" %(status)s %(body_bytes_sent)s')
logger = getLogger()
handler = FileHandler('access.log') 
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('Server started')


server_port = 15000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print('The server is', server_port ,'ready to receive')

def get_file(path):

    try:
        file = open("." + path,"rb")
        content = file.read()
        logger.info('GET %s 200 %d', path, len(content))
        return b"HTTP/1.1 200 OK\r\n\r\n" + content
    except FileNotFoundError as e:
        file = open("./error.html", "rb")
        content = file.read()
        logger.warning('GET %s 404 %d', path, len(content))
        return b"HTTP/1.1 404 Not Found\r\n\r\n" + content
    except Exception as e:
        logger.error('GET %s 500 %d', path, 0)
        return b"HTTP/1.1 500 Internal Server Error\r\n\r\nServer error"

def http_handler(request):
    request = request.split() #GET /index.html HTTP/1.0/r/n/r/n

    method = request[0]
    path = request[1]
    protocol = request[2]

    if method != "GET":
        logger.warning('GET %s 400 %d', path, 0)
        return b"HTTP/1.1 400 Bad Request\r\n\r\n"

    if method == "GET":        
        if protocol == "HTTP/1.0":
            if b"HTTP/1.1" in response:
                response = response.replace(b"HTTP/1.1", b"HTTP/1.0")
            response = get_file(path)
            return response
        if protocol == "HTTP/1.1":
            response = get_file(path)
            if b"HTTP/1.0" in response:
                response = response.replace(b"HTTP/1.0", b"HTTP/1.1")
            return response

while True:
    connection_socket, addr = server_socket.accept()
    request = connection_socket.recv(2048).decode()
    response = http_handler(request)
    connection_socket.sendall(response)
    connection_socket.close()



