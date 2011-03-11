Bloggart is a _blog application_ for Google App Engine.
Is written in Python and uses all the Google App Engine Python goodness.

## ATTENTION --- ATTENTION --- ATTENTION
### "default" and "coolblue" themes are currently broken
If you plan to use my fork of Bloggart, bear in mind that currently the _"default"_ and _"coolblue"_
themes are not working. New features (i.e. 'Pages') have made me change the name of some values
passed to the templates: I forgot to promptly update the themes, and now they are broken
(mostly the 'admin' pages).

If you would like to take on the task to fix them (it's "just" a matter to fix the template
variables), **please**, feel free to fork. I'll be more than happy to pull in your changes!

*2011-03-11* > detro  

## A bit of history

It was originally developed as a demonstration app from Nick Johnson for
[a series of blog posts](http://blog.notdot.net/2009/10/Writing-a-blog-system-on-App-Engine),
and intended to be a useful and versatile blogging system for App Engine by the time it's done.

I forked it up and I'm making it "mine", feature by feature.

## Features

This engine is not designed to be in anyway comparable to stuff like _Wordpress et similia_.
The idea is to provide a developer, possibly an App Engine developer, a way to run a personal
blog on the Google Cloud: Quickly set it up and, if necessary, tweak the hell out of it!

There are different features I want to add. This is a live list of what's pending and what's done:

* Support for 'Pages', instead of just 'Posts'
* **[DONE]** JS and CSS 'Minification' (no obfuscation though)
* **[DONE]** JS and CSS 'Templating' (i.e. Being able to use App Engine Djiango Template grammar into JS and CSS files)
* **[DONE]** JS and CSS 'Memcaching'
* **[DONE]** Show line numbers for '&lt;pre&gt;sourcecode&lt;/pre&gt;' areas in posts
* Add more themes:
    * **[DONE]** Coolblue
    * A personal, HTML5-based theme

## Original Logo

This is Bloggart original logo from Nick. I'd like to steak with it for now.

![Bloggart](http://github.com/Arachnid/bloggart/raw/master/themes/default/static/images/bloggart-ae.png)

## Who is _detro_?

_detro_, aka _Detronizator_, is Ivan De Marino. Italian, CompSci, Developer, Cook and Father-wonnabe.
[Google me](http://www.google.com/search?q=Ivan+De+Marino) if you need to know more: it's all online.
