# Author Joe Tan
from google.appengine.ext import ndb
from google.appengine.api import users

class UserModel(ndb.Model):
    username = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    email_address = ndb.StringProperty(required = True)
    latlng = ndb.JsonProperty()

def getUser(username, password):
    user = UserModel.query(UserModel.username == username and UserModel.password == password).fetch(keys_only=True)
    if len(user) > 0:
        key = user[0]
        current_user = key
    else:
        return "User Not Found"
    return key

def createUser(username, password, first_name, last_name, email_address):
    user = UserModel(username = username, password = password, first_name = first_name, last_name =last_name, email_address = email_address)
    user.put()

def getAllUsersLatLng():
    keys = UserModel.query().fetch(keys_only=True)
    latlng = []
    for key in keys:
        latlng.append(key.get().latlng)
        print key
    return latlng
