import datetime
import logging
import os

from google.appengine.ext import deferred
from google.appengine.ext import webapp

import config
import markup
import models
import post_deploy
import utils

# Bloggart is currently based on Django 0.96
from google.appengine.dist import use_library
use_library('django', '0.96')
from django import newforms as forms
from google.appengine.ext.db import djangoforms


class PostForm(djangoforms.ModelForm):
  title = forms.CharField(widget=forms.TextInput( attrs={'id':'name'} ));
  body = forms.CharField(widget=forms.Textarea( attrs={'id':'message', 'rows': 10, 'cols': 20} ));
  body_markup = forms.ChoiceField( choices=[(k, v[0]) for k, v in markup.MARKUP_MAP.iteritems()] );
  tags = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}));
  draft = forms.BooleanField(required=False);
  class Meta:
    model = models.BlogPost
    fields = [ 'title', 'body', 'tags' ]
    

class PageForm(djangoforms.ModelForm):
  # Overridden constructor to initialise the Form properly
  def __init__(self, current_page, *args, **kwargs):
    self.base_fields['parent_page'].query = models.Page.all();
    if ( current_page ):
      # Show all the pages, except the one associated with the current form instance
      self.base_fields['parent_page'].query.filter("__key__ != ", current_page.key());
        
    self.base_fields['parent_page'].widget.choices = self.base_fields['parent_page'].choices;
    super(PageForm, self).__init__(*args, **kwargs);
  
  title = forms.CharField( widget=forms.TextInput( attrs={'id':'name'} ));
  parent_page = djangoforms.ModelChoiceField( models.Page, None, required=False, initial=None, empty_label="none" );
  body = forms.CharField( widget=forms.Textarea( attrs={'id':'message', 'rows': 10, 'cols': 20} ));
  body_markup = forms.ChoiceField( choices=[(k, v[0]) for k, v in markup.MARKUP_MAP.iteritems()] );
  draft = forms.BooleanField( required=False );
  class Meta:
    model = models.Page
    fields = [ 'title', 'parent_page', 'body' ]


def with_post(fun):
  def decorate(self, post_id=None):
    post = None
    if post_id:
      post = models.BlogPost.get_by_id(int(post_id))
      if not post:
        self.error(404)
        return
    fun(self, post)
  return decorate
  

def with_page(fun):
  def decorate(self, page_id=None):
    page = None
    if page_id:
      page = models.Page.get_by_id(int(page_id));
      if not page:
        self.error(404);
        return
    fun(self, page)
  return decorate;


class BaseHandler(webapp.RequestHandler):
  def render_to_response(self, template_name, template_vals=None, theme=None):
    if not template_vals:
      template_vals = {}
    template_vals.update({
        'path': self.request.path,
        'handler_class': self.__class__.__name__,
        'is_admin': True,
    })
    template_name = os.path.join("admin", template_name)
    self.response.out.write(utils.render_template(template_name, template_vals,
                                                  theme))


class AdminHandler(BaseHandler):
  def get(self):
    from generators import generator_list
    posts_offset = int(self.request.get('posts_start', 0));
    posts_count = int(self.request.get('posts_count', 20));
    posts = models.BlogPost.all().order('-published').fetch(posts_count, posts_offset);
    pages_offset = int(self.request.get('pages_start', 0));
    pages_count = int(self.request.get('pages_count', 20));
    pages = models.Page.all().order('-published').fetch(pages_count, pages_offset);
    template_vals = {
        'posts_offset': posts_offset,
        'posts_count': posts_count,
        'posts_last_post': posts_offset + len(posts) - 1,
        'posts_prev_offset': max(0, posts_offset - posts_count),
        'posts_next_offset': posts_offset + posts_count,
        'posts': posts,
        'pages_offset': pages_offset,
        'pages_count': pages_count,
        'pages_last_page': pages_offset + len(pages) - 1,
        'pages_prev_offset': max(0, pages_offset - pages_count),
        'pages_next_offset': pages_offset + pages_count,
        'pages': pages,
        'generators': [cls.__name__ for cls in generator_list],
    };
    self.render_to_response("index.html", template_vals);


class PostHandler(BaseHandler):
  def render_form(self, form):
    self.render_to_response("edit_post.html", {'form': form})

  @with_post
  def get(self, post):
    self.render_form(PostForm(
        instance=post,
        initial={
          'draft': post and not post.path,
          'body_markup': post and post.body_markup or config.default_markup,
        }))

  @with_post
  def post(self, post):
    form = PostForm(data=self.request.POST, instance=post,
                    initial={'draft': post and post.published is None})
    if form.is_valid():
      post = form.save(commit=False)
      if form.clean_data['draft']: # Draft post
        post.published = datetime.datetime.max
        post.put()
      else:
        if not post.path: # Publish post
          post.updated = post.published = datetime.datetime.now(utils.tzinfo())
        else: # Edit post
          post.updated = datetime.datetime.now(utils.tzinfo())
        post.publish()
      self.render_to_response("published.html", {
          'content': post,
          'type' : 'post',
          'draft': form.clean_data['draft']})
    else:
      self.render_form(form)

class DeletePostHandler(BaseHandler):
  @with_post
  def post(self, post):
    # TODO
    if post.path: # Published post
      post.remove();
    else: # Draft
      post.delete();
    self.render_to_response("deleted.html", {'type' : 'post'});


class PreviewPostHandler(BaseHandler):
  @with_post
  def get(self, post):
    # Temporary set a published date iff it's still
    # datetime.max. Django's date filter has a problem with
    # datetime.max and a "real" date looks better.
    if post.published == datetime.datetime.max:
      post.published = datetime.datetime.now(utils.tzinfo());
    self.response.out.write(utils.render_template('post.html', {'post' : post, 'is_admin' : True}));


class PageHandler(BaseHandler):
  def render_form(self, form):
    self.render_to_response("edit_page.html", {'form': form})

  @with_page
  def get(self, page):
    self.render_form(PageForm(instance=page,
      current_page=page,
      initial={
        'draft': page and not page.path,
        'body_markup': page and page.body_markup or config.default_markup
      }));

  @with_page
  def post(self, page):
    form = PageForm(current_page=page, data=self.request.POST, instance=page, initial={'draft': page and page.published is None});
    if form.is_valid():
      page = form.save(commit=False);
      
      # Ensure that a 'Child Page' is never asigned as 'Parent Page' as well
      page.put();
      for p in page.child_pages:
        if ( page.parent_page.key() == p.key() ):
          page.parent_page = None;
          page.put();
          break;
      
      if form.clean_data['draft']: # Draft page
        page.published = datetime.datetime.max;
        page.put();
      else:
        if not page.path: # Publish page
          page.updated = page.published = datetime.datetime.now(utils.tzinfo());
        else: # Edit post
          page.updated = datetime.datetime.now(utils.tzinfo());
        page.publish();
      self.render_to_response("published.html", {'content': page, 'type' : 'page', 'draft': form.clean_data['draft']});
    else:
      self.render_form(form);

class DeletePageHandler(BaseHandler):
  @with_page
  def post(self, page):
    if page.path: # Published page
      page.remove();
    else: # Draft
      page.delete();
    self.render_to_response("deleted.html", {'type' : 'page'});


class PreviewPageHandler(BaseHandler):
  @with_page
  def get(self, page):
    # Temporary set a published date iff it's still
    # datetime.max. Django's date filter has a problem with
    # datetime.max and a "real" date looks better.
    if page.published == datetime.datetime.max:
      page.published = datetime.datetime.now(utils.tzinfo());
    self.response.out.write(utils.render_template('page.html', {'page' : page, 'is_admin' : True}));


class RegenerateHandler(BaseHandler):
  def post(self):
    # Get which "generator" the User requested to run
    generators = self.request.get_all("generators");
    
    # Launch a deferred task for Regeneration
    deferred.defer(post_deploy.PostRegenerator().regenerate, classes=generators);
    # Launch a deferred task for Regeneration
    deferred.defer(post_deploy.PageRegenerator().regenerate, classes=generators);
    
    # Post-Deploy tasks
    deferred.defer(post_deploy.try_post_deploy, force=True);

    # Render a "regenerating" page 
    self.render_to_response("regenerating.html")
