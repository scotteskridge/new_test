from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        errors = [] #make a list of strings and append errors
        reply_to_veiws = {} # make an object to give a status and user_id back
        #put in valdatations can I validate for both login and register i dont think so so I'm going to make two methods but thats ok becuase my .Models pulls from the object?
        #check if firstname >2
        if len(postData["name"]) < 2:
            errors.append("First Name must be more than 2 character long")
        #check if user_name >2
        if len(postData["user_name"]) < 2:
            errors.append("First Name must be more than 2 character long")
        if not len(postData["date_hired"]):
            errors.append("Date can't be empty")
        #check if email matches regex and is not empty
        if not len(postData["email"].lower()):
            errors.append("Email is required")
        else:
            if not EMAIL_REGEX.match(postData["email"].lower()):
                errors.append("Enter a valid Email address")
        #check if email is unique
        if self.filter(email = postData["email"].lower()):
            errors.append("Email already in use")
        #check is password is null
        if len(postData["password"]) < 8:
            errors.append("Password must be more than 8 character long")
        if not postData["password"] == postData["password_confirm"]:
            errors.append("Passwords don't match")
        #Dump all the errors into errors{} so you can pass it back
        #return errors and a status of false

        #check is validations are true or false
        # if no errors then
        if not errors:
            #hash post data password
            hashed_password = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
            #create the user self.create?
            user = self.create(name = postData["name"], user_name = postData["user_name"], email = postData["email"].lower(), date_hired= postData["date_hired"], password = hashed_password)
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
        # make an object to give a status and user_id back
        #put in valdatations can I validate for both login and register i dont think so so I'm going to make two methods but thats ok becuase my .Models pulls from the object?
        #first thing is to find an email from post data
        if postData:
            #FIXED##!!!! i think my email is case sensative look into fixing this if you have the time !!!!####
            user = self.filter(email = postData["email"].lower())
            if not EMAIL_REGEX.match(postData["email"].lower()):
                errors.append("Enter a valid Email address")

        if not user:

            errors.append("No email found please try again or register")
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
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_hired = models.DateField(blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
