# Author Joe Tan
from google.appengine.ext import ndb
from google.appengine.api import users

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
    friends = ndb.PickleProperty(repeated = True)

def getCurrentUser():
    key = False
    user = users.get_current_user()
    if user:
        user = UserModel.query(UserModel.user_id == user.user_id()).fetch(keys_only=True)
        if len(user) > 0:
            key = user[0]
    return key

def createUser(user,username, major, first_name, last_name, email_address):
    user = UserModel(user_id = user, username = username, major = major, first_name = first_name, last_name =last_name, email_address = email_address)
    user.put()

def getAllUsersLatLng():
    keys = UserModel.query().fetch(keys_only=True)
    userInfoArray = []
    for key in keys:
        user = key.get()
        userInfoArray.append({"user_id":str(user.user_id), "latlng": user.latlng, "username": user.username})
    return userInfoArray

def getAllOtherActiveUsersLatLng():
    user = users.get_current_user()
    keys = UserModel.query(UserModel.isActive == True, UserModel.user_id != user.user_id()).fetch(keys_only=True)
    userInfoArray = []
    for key in keys:
        user = key.get()
        userInfoArray.append({"user_id":str(user.user_id), "latlng": user.latlng, "username": user.username, "subject": user.subject})
    return userInfoArray

def setCurrentUserActive():
    user = getCurrentUser().get()
    user.isActive = True
    user.put()

def setCurrentUserInactive():
    user = getCurrentUser().get()
    user.isActive = False
    user.put()

def addFriend(username):
    other = UserModel.query(UserModel.username == username).fetch(keys_only = True)
    user = getCurrentUser().get()
    if(len(other) > 0 and other not in user.friends):
        user.friends.append(other[0])
        user.put()

def getFriends():
    user = getCurrentUser().get()
    return user.friends
