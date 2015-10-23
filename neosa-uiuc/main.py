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
from google.appengine.ext import ndb
from google.appengine.api import users
import logging

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class UserModel(ndb.Model):
    username = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    email_address = ndb.StringProperty(required = True)
    latlng = ndb.JsonProperty()
    # calendar = ndb.PickleProperty(repeated = True)

def getUser(username, password):
    user = UserModel.query(UserModel.username == username and UserModel.password == password).fetch(keys_only=True)
    if len(user) > 0:
        key = user[0]
        current_user = key
    else:
        return "User Not Found"
    return key

def createUser(username, password, first_name, last_name, email_address,location):
    user = UserModel(username = username, password = password, first_name = first_name, last_name =last_name, email_address = email_address)
    user.put()


current_user = getUser('foo','bar')
class Test(webapp2.RequestHandler):
    def get(self):
        user = getUser('foo','bar')
        info = user.get()
        # info.email_address = "Joe@joe"
        # info.put()
        self.response.out.write(info)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render())

class MapHandler(webapp2.RequestHandler):
    def get(self):
        if current_user is 'none':
            self.redirect('/login')
        template = jinja_environment.get_template('templates/map.html')
        self.response.out.write(template.render())
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

class ProfilePageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/profilepage.html')
        self.response.out.write(template.render())



app = webapp2.WSGIApplication([
    ('/map', MapHandler),
    ('/calendar', CalendarHandler),
    ('/about', AboutHandler),
    ('/signup', SignUpHandler),
    ('/login', LoginHandler),
    ('/profilepage', ProfilePageHandler),
    ('/test', Test),
    ('/.*', MainHandler)
], debug=True)
