#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *

server_port = 15000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)

print('The server is ready to receive on port:', server_port)

def get_file(path):
    try:
        file_path = "." + path if path != "/" else "./index.html"
        with open(file_path, "rb") as file:
            content = file.read()
            return b"HTTP/1.1 200 OK\r\n\r\n" + content
    except FileNotFoundError:
        return b"HTTP/1.1 404 Not Found\r\n\r\nFile not found"
    except Exception as e:
        print(f"Server error: {e}")
        return b"HTTP/1.1 500 Internal Server Error\r\n\r\nServer error"



def http_handler(request):
    lines = request.split('\r\n')
    first_line = lines[0].split(' ')
    if len(first_line) < 3:
        return b"HTTP/1.1 400 Bad Request\r\n\r\n"  

    method, path, version = first_line

    if method != "GET":
        return b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"

    if method == "GET":        
        if version.strip() == "HTTP/1.0" or version.strip() == "HTTP/1.1":
            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + get_file(path)
            print(type(response))
            return response
    else:
        return get_file('/error.html')


while True:
    connection_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    request = connection_socket.recv(2048).decode('utf-8')
    response = http_handler(request)
    #print(f"DEBUG: Response: {response}")  # Add this line 
    if response is not None:
        connection_socket.sendall(response)
    else:
        print("Response is None")
    connection_socket.close()


