# Author Joe Tan
from google.appengine.ext import ndb
from google.appengine.api import users
import datetime
from google.appengine.api import datastore_types
from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers

class UserModel(ndb.Model):
    user_id = ndb.StringProperty(required = True)
    username = ndb.StringProperty()
    major = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email_address = ndb.StringProperty()
    latlng = ndb.JsonProperty()
    subject = ndb.StringProperty()
    schedule = ndb.DateTimeProperty(repeated = True)
    isActive = ndb.BooleanProperty()

def getCurrentUser():
    key = False
    user = users.get_current_user()
    if user:
        user = UserModel.query(UserModel.user_id == user.user_id()).fetch(keys_only=True)
        if len(user) > 0:
            key = user[0]
    return key

def createUser(user,username, major, first_name, last_name, email_address):
    user = UserModel(
                user_id = user,
                username = username,
                major = major,
                first_name = first_name,
                last_name =last_name,
                email_address = email_address,
                isActive = True
                )
    user.put()

def getAllUsersLatLng():
    keys = UserModel.query().fetch(keys_only=True)
    userLatLngTupleArray = []
    for key in keys:
        user = key.get()
        userLatLngTupleArray.append({"user_id":str(user.user_id), "latlng": user.latlng})
    return userLatLngTupleArray

def setActive(status):
    user = getCurrentUser().get()
    user.isActive = status
    user.put()
    
