import cgi
import threading
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server


urls = []


def run_server(environ, star_response):
    star_response('200 OK', [('Content-Type', 'text/html;charset=urf-8')])
    url = environ['PATH_INFO']
    func = None
    for i in urls:
        if i[0] == url:
            func = i[2]
            break
    if func:
        response = str(func(environ)).encode('utf-8')
    else:
        response = b'404 not found!'
    return [response, ]


def route(url, method=['GET', 'POST']):
    def wrapper(handler):
        urls.append([url, method, handler])
        return handler
    return wrapper


def run(host='127.0.0.1', port=8080, **kwargs):
    '''
    启动监听服务
    '''
    httpd = make_server(host, port, run_server)
    print('Courage server starting up ...')
    print('Listening on http://%s:%d/' % (host, port))
    print('Use Ctrl-C to quit.')
    print('')
    httpd.serve_forever()
