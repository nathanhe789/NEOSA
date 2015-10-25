# Author Joe Tan
from google.appengine.ext import ndb
from google.appengine.api import users

class UserModel(ndb.Model):
    user_id = ndb.StringProperty(required = True)
    username = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email_address = ndb.StringProperty(required = True)
    latlng = ndb.JsonProperty()

def getUser(username, password):
    key = False
    user = UserModel.query(UserModel.username == username and UserModel.password == password).fetch(keys_only=True)
    if len(user) > 0:
        key = user[0]
    return key

def getCurrentUser():
    key = False
    user = users.get_current_user()
    if user:
        user = UserModel.query(UserModel.user_id == user.user_id()).fetch(keys_only=True)
        if len(user) > 0:
            key = user[0]
    return key

def createUser(user,username, password, first_name, last_name, email_address):
    user = UserModel(user_id = user, username = username, password = password, first_name = first_name, last_name =last_name, email_address = email_address)
    user.put()

def getAllUsersLatLng():
    keys = UserModel.query().fetch(keys_only=True)
    latlng = []
    for key in keys:
        latlng.append(key.get().latlng)
    return latlng
