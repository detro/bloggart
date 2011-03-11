import os
import re
import unicodedata

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.template import _swap_settings

# Bloggart is currently based on Django 0.96
from google.appengine.dist import use_library
use_library('django', '0.96')
import django.conf
from django import template
from django.template import loader

import config

BASE_DIR = os.path.dirname(__file__)

if isinstance(config.theme, (list, tuple)):
  TEMPLATE_DIRS = config.theme
else:
  TEMPLATE_DIRS = [os.path.abspath(os.path.join(BASE_DIR, 'themes/default'))]
  if config.theme and config.theme != 'default':
    TEMPLATE_DIRS.insert(0,
                         os.path.abspath(os.path.join(BASE_DIR, 'themes', config.theme)))


def slugify(s):
  s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
  return re.sub('[^a-zA-Z0-9-]+', '-', s).strip('-')


def format_page_path(page, num):
    slug = format_page_path(page.parent_page, 0) if page.parent_page else "";
    slug += '/' + slugify(page.title);
    if num > 0:
        slug += "-" + str(num);
    return slug;


def format_post_path(post, num):
  slug = slugify(post.title)
  if num > 0:
    slug += "-" + str(num)
  date = post.published_tz
  return config.post_path_format % {
      'slug': slug,
      'year': date.year,
      'month': date.month,
      'day': date.day,
  }


def get_template_vals_defaults(template_vals=None):
    import models;
    
    if template_vals is None:
        template_vals = {}
    
    template_vals.update({
        'config': config,
        'devel': os.environ['SERVER_SOFTWARE'].startswith('Devel'),
        'top_pages' : models.Page.all().filter("parent_page = ", None)
    });
    return template_vals;


def render_template(template_name, template_vals=None, theme=None):
  template_vals = get_template_vals_defaults(template_vals)
  template_vals.update({'template_name': template_name})
  old_settings = _swap_settings({'TEMPLATE_DIRS': TEMPLATE_DIRS})
  try:
    tpl = loader.get_template(template_name)
    rendered = tpl.render(template.Context(template_vals))
  finally:
    _swap_settings(old_settings)
  return rendered


def _get_all_paths():
  import static
  keys = []
  q = static.StaticContent.all(keys_only=True).filter('indexed', True)
  cur = q.fetch(1000)
  while len(cur) == 1000:
    keys.extend(cur)
    q = static.StaticContent.all(keys_only=True)
    q.filter('indexed', True)
    q.filter('__key__ >', cur[-1])
    cur = q.fetch(1000)
  keys.extend(cur)
  return [x.name() for x in keys]


def _regenerate_sitemap():
  import static
  import gzip
  from StringIO import StringIO
  paths = _get_all_paths()
  rendered = render_template('sitemap.xml', {'paths': paths})
  static.set('/sitemap.xml', rendered, 'application/xml', False, type=static.TYPE_OTHER)
  s = StringIO()
  gzip.GzipFile(fileobj=s,mode='wb').write(rendered)
  s.seek(0)
  renderedgz = s.read()
  static.set('/sitemap.xml.gz',renderedgz, 'application/x-gzip', False, type=static.TYPE_OTHER)
  # Ping Google only if configured to do so and NOT on localhost
  if ( config.google_sitemap_ping and not (config.host.find("localhost") > -1) ):
    ping_googlesitemap();

def ping_googlesitemap():
  import urllib
  from google.appengine.api import urlfetch
  google_url = 'http://www.google.com/webmasters/tools/ping?sitemap=http://' + config.host + '/sitemap.xml.gz'
  response = urlfetch.fetch(google_url, '', urlfetch.GET)
  if response.status_code / 100 != 2:
    raise Warning("Google Sitemap ping failed", response.status_code, response.content)

def tzinfo():
  """
  Returns an instance of a tzinfo implementation, as specified in
  config.tzinfo_class; else, None.
  """

  if not config.tzinfo_class:
    return None

  str = config.tzinfo_class
  i = str.rfind(".")

  try:
    # from str[:i] import str[i+1:]
    klass_str = str[i+1:]
    mod = __import__(str[:i], globals(), locals(), [klass_str])
    klass = getattr(mod, klass_str)
    return klass()
  except ImportError:
    return None

def tz_field(property):
  """
  For a DateTime property, make it timezone-aware if possible.

  If it already is timezone-aware, don't do anything.
  """
  if property.tzinfo:
    return property

  tz = tzinfo()
  if tz:
    # delay importing, hopefully after fix_path is done
    from timezones.utc import UTC

    return property.replace(tzinfo=UTC()).astimezone(tz)
  else:
    return property


class memoize_content(object):
  """
  A memcache-based memoizer for content; keys are the content's path.
  """
  def __init__(self, namespace):
    self.namespace = namespace

  def __call__(self, func):
    def _dec(content):
      if content.path:
        data = None;
        if ( config.memcaching ):
          data = memcache.get(content.path, namespace=self.namespace);
          
        if data:
          return data
        else:
          data = func(content)
          memcache.set(content.path, data, namespace=self.namespace)
          return data
      else:
        return func(content)
    return _dec

  def delete(self, content):
    if content.path:
      memcache.delete(content.path, namespace=self.namespace)

# BlogPost Memoizers
post_body_memoizer = memoize_content('BlogPost.rendered');
post_summary_memoizer = memoize_content('BlogPost.summary');
post_hash_memoizer = memoize_content('BlogPost.hash');
post_summary_hash_memoizer = memoize_content('BlogPost.summary_hash');

# Page Memoizers
page_body_memoizer = memoize_content('Page.rendered');
page_hash_memoizer = memoize_content('Page.hash');

def clear_post_memoizer_cache(post):
    post_body_memoizer.delete(post);
    post_summary_memoizer.delete(post);
    post_hash_memoizer.delete(post);
    post_summary_hash_memoizer.delete(post);
  
def clear_page_memoizer_cache(page):
    page_body_memoizer.delete(page);
    page_hash_memoizer.delete(page);

