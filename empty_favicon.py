# Bloggart is currently based on Django 0.96
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '0.96')

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class EmptyFaviconHandler(webapp.RequestHandler):
    def get(self):
        self.response.set_status(204)

application = webapp.WSGIApplication([
    ('/favicon.ico', EmptyFaviconHandler)
])

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
