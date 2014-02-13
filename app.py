#!/usr/bin/env python
import socket
import urlparse
import cgi
import StringIO
import jinja2

def make_app():
    return simple_app

def simple_app(environ, start_response):
    return handle_request(environ, start_response)

def handle_request(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    status = '200 OK'
    headers = [('Content-type','text/html')]

    # Sets up jinja2 to help with html templates.
    loader = jinja2.FileSystemLoader('./templates')
    jenv = jinja2.Environment(loader=loader)

    # Creates the appropriate message.
    if method == 'POST':
        if path == '/submit-post-app' or path == '/submit-post-multi':
            message = create_submit_post(environ, jenv)
        else:
            message = create_post(jenv)
    else:
        if path == '/':
            message = create_default(jenv)
        elif path == '/content':
            message = create_content(jenv)
        elif path == '/file':
            message = create_file(jenv)
        elif path == '/image':
            message = create_image(jenv)
        elif path == '/form-get':
            message = create_form_get(jenv)
        elif path == '/form-post-app':
            message = create_form_app(jenv)
        elif path == '/form-post-multi':
            message = create_form_multi(jenv)
        elif path == '/submit-get':
            message = create_submit(environ, jenv)
        else:
            status = '404 Not Found'
            message = create_404_error(jenv)

    start_response(status, headers) # Starts response by sending status/headers.
    return message.encode('latin-1', 'replace') # Returns rest of the response.

def create_default(jenv):
    return jenv.get_template('Index.html').render()

def create_content(jenv):
    return jenv.get_template('Content.html').render()

def create_file(jenv):
    return jenv.get_template('File.html').render()

def create_image(jenv):
    return jenv.get_template('Image.html').render()

def create_post(jenv):
    return jenv.get_template('PostDefault.html').render()

def create_form_get(jenv):
    return jenv.get_template('FormGet.html').render()

def create_form_app(jenv):
    return jenv.get_template('FormPostApp.html').render()

def create_form_multi(jenv):
    return jenv.get_template('FormPostMulti.html').render()

def create_submit(env, jenv):
    # Parses through GET query component of URL.
    queryDict = urlparse.parse_qs(env['QUERY_STRING'])

    vars = dict(firstname=queryDict['firstname'][0],
                lastname=queryDict['lastname'][0])

    return jenv.get_template('Submit.html').render(vars)

def create_submit_post(env, jenv):
    # Holds submitted form data.
    # FieldStorage is case-sensitive when looking at content-type
    # so headers is specified with additional key in lower-case too.
    form = cgi.FieldStorage(fp=StringIO.StringIO(env['wsgi.input']),
                            headers={'content-type' : env['CONTENT-TYPE']},
                            environ=env)

    vars = dict(firstname=form.getvalue('firstname'),
                lastname=form.getvalue('lastname'))

    return jenv.get_template('Submit.html').render(vars)

def create_404_error(jenv):
    return jenv.get_template('404.html').render()

