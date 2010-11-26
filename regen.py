from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import fix_path
import config
import utils
import post_deploy


class StaticContentHandler(webapp.RequestHandler):
   def get(self):
      if ( config.allow_forced_regen ):
         post_deploy.PostRegenerator().regenerate();
         post_deploy.post_deploy(post_deploy.BLOGGART_VERSION);
         self.response.out.write("Regenerating...");
      else:
         self.error(404)
         self.response.out.write(utils.render_template('404.html'))


application = webapp.WSGIApplication( [('/__regen', StaticContentHandler)] )


def main():
  fix_path.fix_sys_path()
  run_wsgi_app(application)


if __name__ == '__main__':
  main()