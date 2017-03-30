from __future__ import unicode_literals
from django.db import models
from datetime import date, time, datetime
from dateutil.parser import parse as parse_date
from .. login.models import User


# Create your models here.
def validate_empty_fields(postData, errors):
    if not len(postData["task"]):
        errors.append("Please enter a task")
    if not len(postData["date"]):
        errors.append("Due Date can't be empty")
    if not len(postData["time"]):
        errors.append("Time can't be empty")

def validate_duplicate_appointments(user_id, postData, errors):
    user = User.objects.get(id = user_id)
    current_appointments = Appointment.objects.filter(created_by = user)
    for appointment in current_appointments:
        if (parse_date(postData["date"]).date() == appointment.start_date
            and parse_date(postData["time"]).time() == appointment.start_time):
            errors.append("Time slot already filled")

def validate_future_appointments(user_id, postData, errors):
    if parse_date(postData["date"]).date() == datetime.today().date():
        if parse_date(postData["time"]).time() < datetime.today().time():
            errors.append("Appointment time must be in the future")

    #else if the date is not today that it's in the future
    elif parse_date(postData["date"]).date() < datetime.today().date():
        errors.append("Appointment date must be in the future")

class AppointmentManager(models.Manager):


    def create_appointment(self, postData, user_id):
        #make an appointment with validations
        reply_to_veiws = {}
        errors = []
        validate_empty_fields(postData, errors)
        if not errors:
            #check if the entered data and time match any other dates and times for this user
            validate_duplicate_appointments(user_id, postData, errors)
            validate_future_appointments(user_id, postData, errors)

        #might need a few more validations for time but lets run with this for now
        if not errors:
            user = User.objects.get(id = user_id)
            date_from_form = parse_date(postData["date"]).date()
            print (date_from_form)
            time_from_form = parse_date(postData["time"]).time()
            appointment = self.create(task = postData["task"], created_by = user, start_date =  parse_date(postData["date"]), start_time =  parse_date(postData["time"]), status = "Pending")
            reply_to_veiws["appointment"] = appointment
            reply_to_veiws["status"] = True

        else:
            reply_to_veiws["errors"] = errors
            reply_to_veiws["status"] = False
        return reply_to_veiws

    def edit_appointment(self, postData, appointment_id, user_id):
        #make an appointment with validations
        reply_to_veiws = {}
        errors = []
        #same validations as create_appointment
        validate_empty_fields(postData, errors)
        if not errors:
            validate_duplicate_appointments(user_id, postData, errors)
            validate_future_appointments(user_id, postData, errors)

        if not errors:

            appointment = Appointment.objects.get(id = appointment_id)

            appointment.task = postData["task"]
            appointment.start_date =  parse_date(postData["date"])
            appointment.start_time =  parse_date(postData["time"])
            appointment.status = postData["status"]
            appointment.save()

            reply_to_veiws["appointment"] = appointment
            reply_to_veiws["status"] = True

        else:
            reply_to_veiws["errors"] = errors
            reply_to_veiws["status"] = False
        return reply_to_veiws

    def update_status(self):
        #every time you log into your main page update all of the statuses the possible options are defualt = Pending, user updated = Done, in the past and not done = Missed

        all_appointments = Appointment.objects.all()
        for appointment in all_appointments:
            if (appointment.status != "Done"
                and appointment.start_date <= date.today()
                and appointment.start_time < datetime.today().time()):
                appointment.status = "Missed"
                appointment.save()

    def delete_appointment(self, appointment_id):
        #make an appointment with validations

        appointment = Appointment.objects.get(id = appointment_id)
        appointment.delete()
        return

class Appointment(models.Model):
    task = models.CharField(max_length = 255)
    created_by = models.ForeignKey(User, related_name = 'user_created_by')
    status = models.CharField(max_length = 255)
    #not sure if I need a time and date field or do both in one?
    start_date = models.DateField(blank=True)
    start_time = models.TimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AppointmentManager()
