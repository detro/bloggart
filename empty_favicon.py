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
