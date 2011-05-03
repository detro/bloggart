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

# A nested list of sidebar menus/links.
# For more complex/versatile scenarios, just edit the theme directly.
sidebar_links = [
  ('Blogroll', [
    { 'title' : 'GitHub', 'url' : 'https://github.com/detro', 'target' : '_blank', 'rel' : 'me' },
    { 'title' : 'Linked In', 'url' : 'http://www.linkedin.com/in/ivandemarino', 'target' : '_blank', 'rel' : 'me' },
    { 'title' : 'Twitter', 'url' : 'http://twitter.com/detronizator', 'target' : '_blank', 'rel' : 'me' },
    { 'title' : 'Kickstarter', 'url' : 'http://www.kickstarter.com/profile/ivandemarino', 'target' : '_blank', 'rel' : 'me' },
  ]),
]

# Custom Blocks.
# Useful to do some personalisation without the need of modifying the specific theme.
# This feature needs to be supported by the specific theme.
custom_blocks = [
  ('License', '../../custom_blocks/license.html')    # A 'title' and a 'path' to a html file with the custom content
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

# Content in Bloggart is generated using App Engine Deferred Task API
# For website with a lot of content, is preferable to generate the sitemap with a delay, to
# ensure that the rest of the content is ready, before the 'sitemap.xml' is generated
sitemap_generation_delay_sec = 900 # 15min

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
highlighting_style = 'emacs'

# Absolute url of the blog application use '/blog' for host/blog/
# and '' for host/.Also remember to change app.yaml accordingly
url_prefix = ''

# For use a feed proxy like feedburner.google.com
feed_proxy = "http://feeds.feedburner.com/BlogIvanDeMarino"

# To use Google Friends Connect.
# If you want use Google Friends Connect, go to http://www.google.com/friendconnect/
# and register your domain for get a Google Friends connect ID.
google_friends_id = None
google_friends_comments = True # For comments.
google_friends_members  = True # For a members container.

# To use Twitter.
# Add here your Twitter ID and, based on the specific theme,
# it will be used to mark tweets or show a side widget.
twitter_id = "detronizator"

# The dotted module name of a concrete implementation of tzinfo.
tzinfo_class = 'timezones.sst.SST'

# To format the date of your post.
# http://docs.djangoproject.com/en/1.1/ref/templates/builtins/#now
date_format = "D j F Y"

# Enable Sharing Buttons.
sharing_buttons = True
