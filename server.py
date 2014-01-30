#!/usr/bin/env python
import random
import socket
import time
import urlparse

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
    if not request: # Avoids indexing error.
        conn.close()
        return
    print request

    method = request.splitlines()[0].split(' ')[0]
    url = urlparse.urlparse(request.splitlines()[0].split(' ')[1])

    # Send intial line and headers.
    conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')

    # Send the appropriate payload.
    if method == 'POST' and url.path != '/submit-post':
        handle_post(conn)
    elif url.path == '/':
        handle_default(conn)
    elif url.path == '/content':
        handle_content(conn)
    elif url.path == '/file':
        handle_file(conn)
    elif url.path == '/image':
        handle_image(conn)
    elif url.path == '/form':
        handle_form_get(conn)
    elif url.path == '/form-post':
        handle_form_post(conn)
    elif url.path == '/submit':
        handle_submit(conn, url.query)
    elif url.path == '/submit-post':
        handle_submit(conn, request.splitlines()[-1])

    conn.close()
    return

def handle_default(conn):
    conn.send('<h1>Welcome to john3209\'s Web Server!</h1>')
    conn.send('<a href="/content">Content</a><br />')
    conn.send('<a href="/file">File</a><br />')
    conn.send('<a href="/image">Image</a><br />')
    conn.send('<a href="/form">Form</a>')
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

def handle_form_get(conn):
    conn.send("<form action='/submit' method='GET'>")
    conn.send("First Name: <input type='text' name='firstname'><br>")
    conn.send("Last Name: <input type-'text' name='lastname'><br>")
    conn.send("<input type='submit' value='Submit'>")
    conn.send("</form>")
    return

def handle_form_post(conn):
    conn.send("<form action='/submit-post' method='POST' ")
    conn.send("enctype='application/x-www-form-urlencoded'>")
    conn.send("First Name: <input type='text' name='firstname'><br>")
    conn.send("Last Name: <input type-'text' name='lastname'><br>")
    conn.send("<input type='submit' value='Submit'>")
    conn.send("</form>")
    return

def handle_submit(conn, query):
    queryDict = urlparse.parse_qs(query)
    firstname = queryDict['firstname'][0]
    lastname = queryDict['lastname'][0]
    conn.send("<h1>Hello Mr. {0} {1}.</h1>".format(firstname, lastname))
    return


if __name__ == '__main__':
    main()
