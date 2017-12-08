import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
import re
from django.core.wsgi import get_wsgi_application

# options
DEFAULT_PORT = 7000
ARGUMENT_SET = {
    '-h': { 'single': True, 'given': False },
    '--port': { 'single': False, 'given': False, 'pattern': 'numberOnly' }
}

# in production.
projectpath = [path for path in sys.path if 'site-packages' in path][0] + "/motty"

# in development.
# projectpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(projectpath)

class InvalidOptionError(RuntimeError):
    def __init__(self, message):
        self.message = message

class NoValueDefinedError(RuntimeError):
    def __init__(self, arg):
        self.arg = arg

class ValueTypeError(RuntimeError):
    def __init__(self, message):
        self.message = message

def print_help_messages():
    print("""
Usage : runmotty <command>

1. runmotty                    run powerful motty server!
2. runmotty --port <number>    run motty server on <number> port.
""")

def evaluate_arguments(argv):
    """
    Basically this function converts argument list as map which consists of key and value.
    Key-Value data structure is more intuitive than list. If we want to get 'port' number. we can simply get this from calling 'arg_map['--port']'

    In addition, this function evaluates whether invalid arguments belongs to options or not.
    If the user enter alphabets next to '--port' option. the command must stop and tell users what is wrong.
    """
    is_value = False

    for i, arg in enumerate(argv):
        if is_value:
            is_value = False
            continue
        
        # if there is no key in argument set
        if arg not in ARGUMENT_SET.keys():
            raise InvalidOptionError("Unknown option error: '{0}'".format(arg))
        
        argument = ARGUMENT_SET[arg]
        if argument['single'] :
            argument['given'] = True
        else :
            # if parameter dependent option is not given with parameter.
            if len(argv)-1 < i+1:
                raise NoValueDefinedError(arg)

            # if value format is invalid.
            value = argv[i+1]

            if argument['pattern'] == 'numberOnly':
                match = re.search('^([0-9]+)$', value)
                if not match :
                    raise ValueTypeError("The '{0}' option parameter must be numbers".format(arg))

            argument['given'] = True
            argument['value'] = value
            is_value = True

def run_motty(argv):
    STATIC_ROOT = projectpath + '/app/static'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'motty.settings'

    try:
        evaluate_arguments(argv)
        # help check.
        if ARGUMENT_SET['-h']['given'] :
            print_help_messages();
            return

        port = DEFAULT_PORT if not ARGUMENT_SET['--port']['given'] else ARGUMENT_SET['--port']['value']
        application = get_wsgi_application()
        container = tornado.wsgi.WSGIContainer(application)

        print("Hi, motty is now running on http://localhost:{0}/ \nYou can terminate it by pressing Ctrl + C on the keyboard.".format(port))
        print("\nThe help is displayed when you execute '$ runmotty -h'")

        tornado_app = tornado.web.Application([
            (r'/static/(.*)', tornado.web.StaticFileHandler, { 'path':STATIC_ROOT }),
            (r'.*', tornado.web.FallbackHandler, dict(fallback=container))
        ])

        http_server = tornado.httpserver.HTTPServer(tornado_app)
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\n\nThe motty is stopped.")
    except InvalidOptionError as e:
        print(e.message, "\nAvailable options can be displayed by executing '$ runmotty -h' command")
    except NoValueDefinedError as e:
        print("'{0}' option's value should be provided.\nYou should enter command like this '$ runmotty {1} [value]'".format(e.arg, e.arg))
    except Exception as e:
        print("Unknown error occured.", e)

run_motty(sys.argv[1:]);