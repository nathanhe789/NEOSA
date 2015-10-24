#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#author Joe Tan
import webapp2
import jinja2
import json
import urllib2
import os
import logging
from neosa import *

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

current_user = getUser('sss','sss')
class Test(webapp2.RequestHandler):
    def get(self):
        # auth_handler = urllib2.HTTPBasicAuthHandler()
        # auth_handler.add_password(realm='PDQ Application',
        #                           uri='https://mahler:8092/site-updates.py',
        #                           user='klem',
        #                           passwd='kadidd!ehopper')
        # opener = urllib2.build_opener(auth_handler)
        # # ...and install it globally so it can be used with urlopen.
        # urllib2.install_opener(opener)
        # urllib2.urlopen('http://www.neosa-uiuc.appspot.com/login')
        # opener = urllib2.build_opener()
        # opener.addheaders.append(('Cookie', 'cookiename=cookievalue'))
        # # f = opener.open("http://www.python.org/")
        # # info = user.get()
        # # info.email_address = "Joe@joe"
        # # info.put()
        # # self.response.out.write(info)
        # # template = jinja_environment.get_template('templates/DO_NOT_DELETE.html')
        # # template = jinja_environment.get_template('templates/DO_NOT_DELETE.html')
        #
        self.response.out.write(getAllUsersLatLng())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render())

class MapHandler(webapp2.RequestHandler):
    def get(self):
        if current_user is 'none':
            self.redirect('/login')
        template = jinja_environment.get_template('templates/map.html')
        latlng = {'latlng':json.dumps(getAllUsersLatLng())}
        self.response.out.write(template.render(latlng))
    def post(self):
        logging.info(current_user)
        if current_user is not 'none':
            latlng = self.request.body
            info = current_user.get()
            info.latlng = latlng
            info.put()

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/calendar.html')
        self.response.out.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/about.html')
        self.response.out.write(template.render())

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/signup.html')
        self.response.out.write(template.render())
    def post(self):
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        email_address = self.request.get("email_address")
        username = self.request.get("username")
        password = self.request.get("password")
        createUser(username, password, first_name, last_name, email_address)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/login.html')
        self.response.out.write(template.render())
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        user = getUser(username,password)
        current_user = user
        if user is not 'User Not Found':
            current_user = user
            logging.info(current_user)
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/map', MapHandler),
    ('/calendar', CalendarHandler),
    ('/about', AboutHandler),
    ('/signup', SignUpHandler),
    ('/login', LoginHandler),
    ('/test', Test),
    ('/.*', MainHandler)
], debug=True)
