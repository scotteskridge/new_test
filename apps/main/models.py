from __future__ import unicode_literals
from django.db import models
from datetime import date, time, datetime
from dateutil.parser import parse as parse_date
from .. login.models import User


def validate_empty_fields(postData, errors):
    if not len(postData["destination"]):
        errors.append("Please enter a Destination")
    if not len(postData["plan"]):
        errors.append("Please describe your Plan")
    if not len(postData["start_date"]):
        errors.append("Please enter a start date")
    if not len(postData["end_date"]):
        errors.append("Please enter an end date")

def validate_future_trip(postData, errors):
    if parse_date(postData["start_date"]) < datetime.today():
        errors.append("Start Date must be in the future")

    if parse_date(postData["end_date"]) < parse_date(postData["start_date"]):
        errors.append("End Date must be after Start Date")




class TripManager(models.Manager):
    def create_trip(self, postData, user_id):
        reply_to_veiws = {}
        errors = []
        validate_empty_fields(postData, errors)
        if not errors:
            validate_future_trip(postData, errors)

        if not errors:
            user = User.objects.get(id = user_id)
            print ("8"*80)
            print("am I getting a user")
            print(user.name)
            print(parse_date(postData["start_date"]).date())
            print(parse_date(postData["end_date"]).date())
            trip = self.create(destination = postData["destination"], start_date = parse_date(postData["start_date"]), end_date = parse_date(postData["end_date"]), plan = postData["plan"], created_by = user)
            trip.joined_by.add(user)

            print ("8"*80)
            print("am I getting a trip")
            print(trip.destination)
            reply_to_veiws["trip"] = trip
            reply_to_veiws["status"] = True

        else:
            reply_to_veiws["errors"] = errors
            reply_to_veiws["status"] = False
        return reply_to_veiws


    def join_trip(self, user_id, trip_id):
        user = User.objects.get(id = user_id)
        trip = Trip.objects.get(id = trip_id)
        trip.joined_by.add(user)

class Trip(models.Model):
    destination = models.CharField(max_length = 45)
    start_date = models.DateField(blank = True)
    end_date = models.DateField(blank = True)
    plan = models.CharField(max_length = 255)
    created_by = models.ForeignKey(User, related_name = 'users_created_by')
    joined_by = models.ManyToManyField(User, related_name = 'users_joined')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()
