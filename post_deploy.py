import datetime
import os
import logging

from google.appengine.api.labs import taskqueue
from google.appengine.ext import deferred
from google.appengine.runtime import DeadlineExceededError

import config
import models
import static
import utils


BLOGGART_VERSION = (1, 0, 1)


"""
Content Regenerator
"""
class ContentRegenerator(object):
  def __init__(self):
    self.processed = set()

  def regenerate(self, batch_size=30, start_ts=None, content_model=models.BlogPost):
    # Fetch 'batch_size" contents, with 'published' date before 'start_ts'
    q = content_model.all().order('-published')
    q.filter('published <', start_ts or datetime.datetime.max)
    contents = q.fetch(batch_size)
    
    try:
      # For every content fetched
      for content in contents:
        # Calculate their dependencies
        for generator_class, deps in content.get_deps(True):
          for dep in deps:
            # If the current dependency was not processed before
            if (generator_class.__name__, dep) not in self.processed:
              try:
                # (try to) regenerate dependency
                generator_class.generate_resource(None, dep)
              except:
                logging.error("Regeneration failed for dependency: ")
                logging.error(dep)
                
              # Remember not to process this dependency again              
              self.processed.add((generator_class.__name__, dep))
        
        # Store timespamp for the last processed content
        start_ts = content.published
    except DeadlineExceededError:
      # Continue from the last Content that failed to be regenerated
      deferred.defer(self.regenerate, batch_size, start_ts)


post_deploy_tasks = []


def generate_static_pages(pages):
  def generate(previous_version):
    for path, template, indexed, type in pages:
      rendered = utils.render_template(template)
      static.set(path, rendered, config.html_mime_type, indexed=indexed, type=type);
  return generate

post_deploy_tasks.append(generate_static_pages([
    ('/search', 'search.html', True, static.TYPE_INDEX),
    ('/cse.xml', 'cse.xml', False, static.TYPE_OTHER),
    ('/robots.txt', 'robots.txt', False, static.TYPE_OTHER),
]));

# Regenerate all the Content
def regenerate_all(previous_version=None, force=False):
  if (previous_version and
      (previous_version.bloggart_major,
      previous_version.bloggart_minor,
      previous_version.bloggart_rev) < BLOGGART_VERSION) or force:
    # Defer all BlogPost regeneration
    deferred.defer(ContentRegenerator().regenerate, content_model=models.BlogPost)
    # Defer all Page regeneration
    deferred.defer(ContentRegenerator().regenerate, content_model=models.Page)
    # Regenerate the Sitemap
    static.regenerate_sitemap()

post_deploy_tasks.append(regenerate_all);


def site_verification(previous_version):
  static.set('/' + config.google_site_verification,
             utils.render_template('site_verification.html'),
             config.html_mime_type, indexed=False)

if config.google_site_verification:
  post_deploy_tasks.append(site_verification)


def run_deploy_task():
  """Attempts to run the per-version deploy task."""
  task_name = 'deploy-%s' % os.environ['CURRENT_VERSION_ID'].replace('.', '-')
  try:
    deferred.defer(try_post_deploy, _name=task_name, _countdown=10)
  except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError), e:
    pass


def try_post_deploy(force=False):
  """
  Runs post_deploy() if it has not been run for this version yet.

  If force is True, run post_deploy() anyway, but don't create a new
  VersionInfo entity.
  """
  version_info = models.VersionInfo.get_by_key_name(
      os.environ['CURRENT_VERSION_ID'])
  if not version_info:
    q = models.VersionInfo.all()
    q.order('-bloggart_major')
    q.order('-bloggart_minor')
    q.order('-bloggart_rev')

    version_info = q.get()

    # This might be an initial deployment; create the first VersionInfo
    # entity.
    if not version_info:
      version_info = models.VersionInfo(
        key_name=os.environ['CURRENT_VERSION_ID'],
        bloggart_major = BLOGGART_VERSION[0],
        bloggart_minor = BLOGGART_VERSION[1],
        bloggart_rev = BLOGGART_VERSION[2])
      version_info.put()

      post_deploy(version_info, is_new=False)
    else:
      post_deploy(version_info)
  elif force: # also implies version_info is available
    post_deploy(version_info, is_new=False)


def post_deploy(previous_version, is_new=True):
  """
  Carries out post-deploy functions, such as rendering static pages.

  If is_new is true, a new VersionInfo entity will be created.
  """
  for task in post_deploy_tasks:
    task(previous_version)

  # don't proceed to create a VersionInfo entity
  if not is_new:
    return

  new_version = models.VersionInfo(
      key_name=os.environ['CURRENT_VERSION_ID'],
      bloggart_major = BLOGGART_VERSION[0],
      bloggart_minor = BLOGGART_VERSION[1],
      bloggart_rev = BLOGGART_VERSION[2])
  new_version.put()
