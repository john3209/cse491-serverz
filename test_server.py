import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection_default():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Welcome to john3209\'s Web Server!</h1>' + \
                      '<a href="/content">Content</a><br />' + \
                      '<a href="/file">File</a><br />' + \
                      '<a href="/image">Image</a><br />' + \
                      '<a href="/form">Form</a>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>This is john3209\'s content!</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>This is john3209\'s file!</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>This is john3209\'s image!</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello World!</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form_get():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<form action='/submit' method='GET'>" + \
                      "First Name: <input type='text' name='firstname'><br>" + \
                      "Last Name: <input type-'text' name='lastname'><br>" + \
                      "<input type='submit' value='Submit'>" + \
                      "</form>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form_post():
    conn = FakeConnection("GET /form-post HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<form action='/submit-post' method='POST' " + \
                      "enctype='application/x-www-form-urlencoded'>" + \
                      "First Name: <input type='text' name='firstname'><br>" + \
                      "Last Name: <input type-'text' name='lastname'><br>" + \
                      "<input type='submit' value='Submit'>" + \
                      "</form>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit_get():
    conn = FakeConnection("GET /submit?firstname=Jeff&lastname=Johnson HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<h1>Hello Mr. Jeff Johnson.</h1>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit_post():
    fakeRequest = "POST /submit-post HTTP/1.0\r\n" + \
                  "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
                  "firstname=Jeff&lastname=Johnson"

    conn = FakeConnection(fakeRequest)
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<h1>Hello Mr. Jeff Johnson.</h1>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

