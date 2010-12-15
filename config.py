import logging

# In production, use 'True'
memcaching = True

# In production, use 'logging.WARNING'
logging_level = logging.WARNING

# Name of the blog
blog_name = 'blog. Ivan De Marino'

# Your name (used for copyright info)
author_name = 'Ivan De Marino'

# (Optional) slogan
slogan = 'Converting caffeine into Code, most of the time...'

# The hostname this site will primarially serve off (used for Atom feeds)
host = 'blog.ivandemarino.me'

# Selects the theme to use. Theme names correspond to directories under
# the 'themes' directory, containing templates and static content.
theme = 'squared'

# Defines the URL organization to use for blog postings. Valid substitutions:
#   slug - the identifier for the post, derived from the title
#   year - the year the post was published in
#   month - the month the post was published in
#   day - the day the post was published in
post_path_format = '/%(year)d/%(month)02d/%(day)02d/%(slug)s'

# Sidebar configuration.
# It is a sequence of DIV Blocks with various types of content supported.
# The format is an array of Dictionary like:
#  [
#     {
#        'enabled'   : True (absent or set to False will make the Section disappear)   ,
#        'type'      : 'links' (just a set of links)
#                       or 'gfc' (Google Friends Connect Widget)
#                       or 'twitter' (Twitter Widget)
#                       or 'code' (Generic HTML Code Block: stuff like Ads or Licenses),
#        'title'     : Title to give to this Section in the Sidebar                    ,
#        TYPE-SPECIFIC key-values (see examples below)                                 ,
#     },
#     ...
#  ]
# More can be supported easily, tweaking the theme. Or just using the block of type 'code'.
sidebar_blocks = [
   # Twitter Widget
   {
      'enabled'   : True,
      'type'      : 'twitter',
      'title'     : 'Twitter stream',
      'username'  : 'detronizator',    # Twitter Username
      'ntweets'   : 5,                 # Number of Tweets to Show
      'height'    : 400                # Widget Height (='ntweets * 100' is adviced)
   },
   # Block of Links: Working on
   {
      'enabled'   : True,
      'type'      : 'links',     
      'title'     : 'Working on',
      'links'     : [
         { 'title' : 'txty.mobi', 'url' : 'http://www.txty.mobi', 'external' : True, 'rel' : 'bookmark author' },
      ]
   },
   # Block of Links: Me elsewhere
   {
      'enabled'   : True,
      'type'      : 'links',     
      'title'     : 'Me elsewhere',
      'links'     : [
         { 'title' : '@Github', 'url' : 'http://github.com/detro', 'external' : True, 'rel' : 'bookmark author me' },
         { 'title' : '@LinkedIn', 'url' : 'http://www.linkedin.com/in/ivandemarino', 'external' : True, 'rel' : 'bookmark author me' },
         { 'title' : '@Twitter', 'url' : 'http://twitter.com/detronizator', 'external' : True, 'rel' : 'bookmark author me' },
         { 'title' : '@Facebook', 'url' : 'http://www.facebook.com/detronizator', 'external' : True, 'rel' : 'bookmark author me' },
         { 'title' : '@Google', 'url' : 'http://www.google.com/profiles/detronizator', 'external' : True, 'rel' : 'bookmark author me' },
         { 'title' : '@Anoobi', 'url' : 'http://www.anobii.com/detronizator', 'external' : True, 'rel' : 'bookmark author me' },
      ]
   },
   # Block of Links: Code
   {
      'enabled'   : True,
      'type'      : 'links',     
      'title'     : 'My code',
      'links'     : [
         { 'title' : 'My Bloggart\'s branch', 'url' : 'http://github.com/detro/bloggart', 'external' : True, 'rel' : 'bookmark author me' },
         { 'title' : 'qtoolbox', 'url' : 'http://github.com/detro/qtoolbox', 'external' : True, 'rel' : 'bookmark author me' },
         { 'title' : 'coding exercises', 'url' : 'http://github.com/detro/coding-exercises', 'external' : True, 'rel' : 'bookmark author me' },
      ]
   },
   # Google Friends Connect Widget
   {
      'enabled'   : False,
      'type'      : 'gfc',                   
      'title'     : 'Members',
      'id'        : None,              # Google Friends Connect ID
      'nrows'     : 4,                 # Number of Rows in the Widget
      'comments'  : True               # Enable Comments in Post
   },
   # Google Ads
   {
      'enabled'   : True,
      'type'      : 'code',
      'title'     : 'Ads',
      'path'      : '../../custom_blocks/google_ads.html',   # Path to any custom HTML Code that you want to include
   },
   # An HTML Code Block (this license one is a good example)
   {
      'enabled'   : True,
      'type'      : 'code',
      'title'     : 'License',
      'path'      : '../../custom_blocks/license.html',   # Path to any custom HTML Code that you want to include
   },
]

# Links to External Services on which the User has an Account.
# This will be listed in a theme-specific way.
external_accounts = [
   { 'service' : 'github', 'url' : 'https://github.com/detro' },
   { 'service' : 'linkedin', 'url' : 'http://www.linkedin.com/in/ivandemarino' },
   { 'service' : 'twitter', 'url' : 'http://twitter.com/detronizator' },
   { 'service' : 'kickstarter', 'url' : 'http://www.kickstarter.com/profile/ivandemarino' }
]

# Number of entries per page in indexes.
posts_per_page = 6

# The mime type to serve HTML files as.
html_mime_type = "text/html; charset=utf-8"

# To use disqus for comments, set this to the 'short name' of the disqus forum
# created for the purpose.
disqus_forum = "blogivandemarinome"

# Length (in words) of summaries, by default
summary_length = 50

# If you want to use Google Analytics, enter your 'web property id' here
analytics_id = "UA-136869-8"

# If you want to use PubSubHubbub, supply the hub URL to use here.
hubbub_hub_url = 'http://pubsubhubbub.appspot.com/'

# If you want to ping Google Sitemap when your sitemap is generated change this to True, else False
# see: http://www.google.com/support/webmasters/bin/answer.py?hl=en&answer=34609 for more information
google_sitemap_ping = True

# If you want to use Google Site verification, go to
# https://www.google.com/webmasters/tools/ , add your site, choose the 'upload
# an html file' method, then set the NAME of the file below.
# Note that you do not need to download the file provided - just enter its name
# here.
google_site_verification = "googledb30cb13b3e7812d.html"

# Default markup language for entry bodies (defaults to html).
default_markup = 'markdown'

# Syntax highlighting style for RestructuredText and Markdown,
# one of 'manni', 'perldoc', 'borland', 'colorful', 'default', 'murphy',
# 'vs', 'trac', 'tango', 'fruity', 'autumn', 'bw', 'emacs', 'pastie',
# 'friendly', 'native'.
highlighting_style = 'friendly'

# Absolute url of the blog application use '/blog' for host/blog/
# and '' for host/.Also remember to change app.yaml accordingly
url_prefix = ''

# Defines where the user is defined in the rel="me" of your pages.
# This allows you to expand on your social graph.
rel_me = "me personal blog"

# For use a feed proxy like feedburner.google.com
feed_proxy = "http://feeds.feedburner.com/BlogIvanDeMarino"

# The dotted module name of a concrete implementation of tzinfo.
tzinfo_class = 'timezones.sst.SST'

# To format the date of your post.
# http://docs.djangoproject.com/en/1.1/ref/templates/builtins/#now
date_format = "D j F Y"

# Enable Sharing Buttons.
sharing_buttons = True
