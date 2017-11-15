import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
from django.core.wsgi import get_wsgi_application
#sys.path.append('/home/david/') # path to your project ( if you have it in another dir).

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(BASE_DIR)

    STATIC_ROOT = BASE_DIR + '/app/static'

    os.environ['DJANGO_SETTINGS_MODULE'] = 'motty.settings' # path to your settings module
    application = get_wsgi_application()
    container = tornado.wsgi.WSGIContainer(application)

    print(STATIC_ROOT)

    tornado_app = tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, { 'path':STATIC_ROOT }),
        (r'.*', tornado.web.FallbackHandler, dict(fallback=container))
    ])

    http_server = tornado.httpserver.HTTPServer(tornado_app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()