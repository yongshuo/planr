#init file
from django.core.handlers.wsgi import WSGIHandler
import django
import os, sys

class WSGIEnvironment(WSGIHandler):

    def __call__(self, environ, start_response):
	sys.path.append('/home/yongshuo/planr')
	sys.path.append('/home/yongshuo/planr/gantterenv/lib/python2.7/site-packages/django')
	sys.path.append('/home/yongshuo/planr/config')
	
        os.environ['GDB_PROJECT_ROOT'] = environ['GDB_PROJECT_ROOT']
	os.environ['GDB_PROJECT_ENV'] = environ['GDB_PROJECT_ENV']
	os.environ['GDB_NAME'] = environ['GDB_NAME']
	os.environ['GDB_USER'] = environ['GDB_USER']
	os.environ['GDB_PASSWORD'] = environ['GDB_PASSWORD']
	os.environ['GDB_HOST'] = environ['GDB_HOST']
	
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
        django.setup()

        return super(WSGIEnvironment, self).__call__(environ, start_response)

application = WSGIEnvironment()
