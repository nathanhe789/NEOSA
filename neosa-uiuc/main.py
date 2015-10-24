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
import os
import logging
from google.appengine.api import users
from neosa import *

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Test(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(getAllUsersLatLng())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        current_user = {'current_user':'Stranger'}
        request = self.request.get('logout_button')
        if request:
            self.redirect(users.create_logout_url('/'))
        user = getCurrentUser()
        if user:
            first_name = user.get().first_name
            current_user['current_user'] = first_name
            self.response.out.write(template.render(current_user))
        else:
            self.response.out.write(template.render(current_user))

class MapHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = jinja_environment.get_template('templates/map.html')
        if user:
            latlng = {'latlng':json.dumps(getAllUsersLatLng())}
            self.response.out.write(template.render(latlng))
        else:
            self.redirect('/login')
    def post(self):
        user = users.get_current_user()
        if user:
            latlng = self.request.body
            user = getCurrentUser().get()
            user.latlng = latlng
            user.put()

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/calendar.html')
        self.response.out.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/about.html')
        self.response.out.write(template.render())

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_login_url('/'))


class ProfilePageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/profilepage.html')
        self.response.out.write(template.render())


class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/signup.html')
        self.response.out.write(template.render())
    def post(self):
        user = users.get_current_user()
        user_id = user.user_id()
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        email_address = user.email()
        username = self.request.get("username")
        password = self.request.get("password")
        createUser(user_id,username, password, first_name, last_name, email_address)


app = webapp2.WSGIApplication([
    ('/map', MapHandler),
    ('/calendar', CalendarHandler),
    ('/about', AboutHandler),
    ('/profilepage', ProfilePageHandler),
    ('/signup', SignUpHandler),
    ('/login', LoginHandler),
    ('/test', Test),
    ('/.*', MainHandler)
], debug=True)
