#!/usr/bin/env python
import random
import socket
import time

def main():
    s = socket.socket()	# Create a socket object
    host = socket.getfqdn()	# Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))	# Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)

    # Now wait for client connection.
    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)
    return

def handle_connection(conn):
    request = conn.recv(1000)
    method = request.split('\n')[0].split(' ')[0]
    path = request.split('\n')[0].split(' ')[1]

    # Send intial line and headers.
    conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')

    # Send the appropriate payload.
    if method == 'POST':
        handle_post(conn)
    elif path == '/':
        handle_default(conn)
    elif path == '/content':
        handle_content(conn)
    elif path == '/file':
        handle_file(conn)
    elif path == '/image':
        handle_image(conn)

    conn.close()
    return

def handle_default(conn):
    conn.send('<h1>Welcome to john3209\'s Web Server!</h1>')
    conn.send('<a href="/content">Content</a><br />')
    conn.send('<a href="/file">File</a><br />')
    conn.send('<a href="/image">Image</a><br />')
    return

def handle_content(conn):
    conn.send('<h1>This is john3209\'s content!</h1>')
    return

def handle_file(conn):
    conn.send('<h1>This is john3209\'s file!</h1>')
    return

def handle_image(conn):
    conn.send('<h1>This is john3209\'s image!</h1>')
    return

def handle_post(conn):
    conn.send('<h1>Hello World!</h1>')
    return


if __name__ == '__main__':
    main()
