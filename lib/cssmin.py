#!/usr/bin/python
#
# @author Ivan De Marino - ivan.de.marino@gmail.com
#
# Inspired by:
#    CSS Minifier found on StackOverflow:
#    http://stackoverflow.com/questions/222581/python-script-for-minifying-css
#
# It should also be able to provide:
# - Support for '@import' rules
# - Support for '@media' rules
# - Support for '@charset' rules
# - Support for '@font-face' rules
# - Support for '@page' rules
#
# Why 'should'? Because I didn't test it thoroughly yet
#


import logging
import sys
import re

def minify( incss ):
   outcss = "";
   
   # remove comments - this will break a lot of hacks :-P
   incss = re.sub( r'\s*/\*\s*\*/', "$$HACK1$$", incss ); # preserve IE<6 comment hack
   incss = re.sub( r'/\*[\s\S]*?\*/', "", incss );
   incss = incss.replace( "$$HACK1$$", '/**/' ); # preserve IE<6 comment hack

   # url() doesn't need quotes
   incss = re.sub( r'url\((["\'])([^)]*)\1\)', r'url(\2)', incss );

   # spaces may be safely collapsed as generated content will collapse them anyway
   incss = re.sub( r'\s+', ' ', incss );

   # shorten collapsable colors: #aabbcc to #abc
   incss = re.sub( r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)', r'#\1\2\3\4', incss );

   # fragment values can loose zeros
   incss = re.sub( r':\s*0(\.\d+([cm]m|e[mx]|in|p[ctx]))\s*;', r':\1;', incss );
   
   # First, handle "@import" rules, given their 'grammar difference' from normal rules
   for includeRule in re.findall( r'@import\s+url\s*\(([\w\s\.\/]+)\);', incss ):
      outcss += "@import url(%s);" % (includeRule);

   for rule in re.findall( r'([^{]+){([^}]*)}', incss ):
      # we don't need spaces around operators
      selectors = [re.sub( r'(?<=[\[\(>+=])\s+|\s+(?=[=~^$*|>+\]\)])', r'', selector.strip() ) for selector in rule[0].split( ',' )];
      
      # put together all the properties, stripping out spaces
      properties = "";
      for prop in re.findall( '(.*?):(.*?)(;|$)', rule[1] ):
         properties += '%s:%s;' % (prop[0].strip().lower(), prop[1].strip());
      
      # add to the final string
      outcss += "%s{%s}" % (','.join( selectors ), properties);
   
   return outcss;
