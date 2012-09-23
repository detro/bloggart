# Bloggart is currently based on Django 0.96
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '0.96')

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import fix_path
import models
import appengine_rest_server

# Handler for /rest/ calls
application = webapp.WSGIApplication([
    ('/rest/.*', appengine_rest_server.Dispatcher)
])

# Configure the REST dispatcher
# URL
appengine_rest_server.Dispatcher.base_url = "/rest"
# Models to expose
appengine_rest_server.Dispatcher.add_models({
    "post": models.BlogPost,
    "page": models.Page}
)


def main():
    fix_path.fix_sys_path()
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
