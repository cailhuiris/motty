import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
from django.core.wsgi import get_wsgi_application

# in production.
projectpath = [path for path in sys.path if 'site-packages' in path][0] + "/motty"

# in development.
# projectpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(projectpath)

def run_motty():
    try:
        STATIC_ROOT = projectpath + '/app/static'

        os.environ['DJANGO_SETTINGS_MODULE'] = 'motty.settings' # path to your settings module
        application = get_wsgi_application()
        container = tornado.wsgi.WSGIContainer(application)

        print("Hi, motty is now running on http://localhost:7000/ \nYou can terminate it by pressing Ctrl + C on the keyboard.")

        tornado_app = tornado.web.Application([
            (r'/static/(.*)', tornado.web.StaticFileHandler, { 'path':STATIC_ROOT }),
            (r'.*', tornado.web.FallbackHandler, dict(fallback=container))
        ])

        http_server = tornado.httpserver.HTTPServer(tornado_app)
        http_server.listen(7000)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\n\nThe motty is stopped.")

run_motty();