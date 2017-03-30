from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
from dateutil.parser import parse as parse_date
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        errors = [] #make a list of strings and append errors
        reply_to_veiws = {} # make an object to give a status and user_id back
        if len(postData["name"]) < 2:
            errors.append("First Name must be at least 3 character long")
        if len(postData["user_name"]) < 2:
            errors.append("user_name must be at least 3 character long")
        if self.filter(user_name = postData["user_name"]):
            errors.append("User name already in use")
        #check is password is null
        if len(postData["password"]) < 8:
            errors.append("Password must be more than 8 character long")
        if not postData["password"] == postData["password_confirm"]:
            errors.append("Passwords don't match")

        if not errors:
            #hash post data password
            hashed_password = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
            #create the user self.create?
            user = self.create(name = postData["name"], user_name = postData["user_name"], password = hashed_password)
            #create a reply to the veiws with the user and a status true back to veiws
            reply_to_veiws["user"] = user
            reply_to_veiws["status"] = True

        # if errors
        else:
            #create a reply to the veiws with the user and a status true back to veiws
            reply_to_veiws["errors"] = errors
            reply_to_veiws["status"] = False
        return reply_to_veiws

    def login(self, postData):
        user =[]
        errors = [] #make a list of strings and append erros
        reply_to_veiws = {}

        if postData:

            user = self.filter(user_name = postData["user_name"])


        if not user:

            errors.append("No User Name found please try again or register")
        #ok so here is where I want to do the password match to whats in the database
        #so its going to check the post data against the password thats stored for the email address and use bcrypts check hash, becuase i can return an empty user I should be ok to just check it against user.password
        #so first off find the password
        else:
            if not bcrypt.checkpw(postData["password"].encode(), user[0].password.encode()):
                errors.append("Password doesn't match login email")
        if not errors:
            reply_to_veiws["user"] = user.first()
            reply_to_veiws["status"] = True
        else:
            reply_to_veiws["errors"] = errors
            reply_to_veiws["status"] = False
        #Dump all the errors into errors{} so you can pass it back
        #return errors and a status of false
        return reply_to_veiws

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 45)
    user_name = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
