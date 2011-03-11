import datetime
import os
from google.appengine.api.labs import taskqueue
from google.appengine.ext import deferred

import config
import models
import static
import utils


BLOGGART_VERSION = (1, 0, 1)


"""
Page content regenerator.
"""
class PageRegenerator(object):
  def __init__(self):
    self.seen = set()

  def regenerate(self, batch_size=50, start_ts=None, classes=None):
    q = models.Page.all().order('-published');
    q.filter('published <', start_ts or datetime.datetime.max);
    pages = q.fetch(batch_size);
    # For every Page published before 'start_ts'
    for page in pages:
      # For every Page dependency
      for generator_class, deps in page.get_deps(True):
        # Check if 'generator_class' is part of the kind of content to regenerate
        if classes and (not generator_class.__name__ in classes):
          continue;
        # For every dependency
        for dep in deps:
          # Ensure a generator is never used twice
          if (generator_class.__name__, dep) not in self.seen:
            self.seen.add((generator_class.__name__, dep));
            # Create a Deferred Taask for the regeneration
            deferred.defer(generator_class.generate_resource, None, dep);
      # Save the current Page info
      page.put();
    # If there are still pages to regenerate, launch a new Deferred Task
    if len(pages) == batch_size:
      deferred.defer(self.regenerate, batch_size, pages[-1].published)


class PostRegenerator(object):
  def __init__(self):
    self.seen = set()

  def regenerate(self, batch_size=50, start_ts=None, classes=None):
    q = models.BlogPost.all().order('-published')
    q.filter('published <', start_ts or datetime.datetime.max)
    posts = q.fetch(batch_size)
    for post in posts:
      for generator_class, deps in post.get_deps(True):
        if classes and (not generator_class.__name__ in classes):
          continue
        for dep in deps:
          if (generator_class.__name__, dep) not in self.seen:
            self.seen.add((generator_class.__name__, dep))
            deferred.defer(generator_class.generate_resource, None, dep)
      post.put()
    if len(posts) == batch_size:
      deferred.defer(self.regenerate, batch_size, posts[-1].published)


post_deploy_tasks = []


def generate_static_pages(pages):
  def generate(previous_version):
    for path, template, indexed, type in pages:
      rendered = utils.render_template(template)
      static.set(path, rendered, config.html_mime_type, indexed, type=type);
  return generate

post_deploy_tasks.append(generate_static_pages([
    ('/search', 'search.html', True, static.TYPE_INDEX),
    ('/cse.xml', 'cse.xml', False, static.TYPE_OTHER),
    ('/robots.txt', 'robots.txt', False, static.TYPE_OTHER),
]));


def regenerate_all(previous_version):
  if (previous_version.bloggart_major, previous_version.bloggart_minor, previous_version.bloggart_rev,) < BLOGGART_VERSION:
    deferred.defer(PostRegenerator().regenerate);
    deferred.defer(PageRegenerator().regenerate);

post_deploy_tasks.append(regenerate_all);


def site_verification(previous_version):
  static.set('/' + config.google_site_verification,
             utils.render_template('site_verification.html'),
             config.html_mime_type, False)

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
