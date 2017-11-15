import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
from django.core.wsgi import get_wsgi_application

libpath = [path for path in sys.path if 'site-packages' in path][0]
sys.path.append(libpath + "/motty")

def run_motty():
    STATIC_ROOT = libpath + '/motty/app/static'

    os.environ['DJANGO_SETTINGS_MODULE'] = 'motty.settings' # path to your settings module
    application = get_wsgi_application()
    container = tornado.wsgi.WSGIContainer(application)

    tornado_app = tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, { 'path':STATIC_ROOT }),
        (r'.*', tornado.web.FallbackHandler, dict(fallback=container))
    ])

    http_server = tornado.httpserver.HTTPServer(tornado_app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

run_motty();