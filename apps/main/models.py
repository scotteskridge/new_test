from __future__ import unicode_literals
from django.db import models
from datetime import date, time, datetime
from dateutil.parser import parse as parse_date
from .. login.models import User

# Create your models here.
class AppointmentManager(models.Manager):
    def create_appointment(self, postData, user_id):
        #make an appointment with validations
        reply_to_veiws = {}
        errors = []

        #do some validations
        if not len(postData["task"]):
            errors.append("Please enter a task")
        if not len(postData["date"]):
            errors.append("Due Date can't be empty")
        if not len(postData["time"]):
            errors.append("Time can't be empty")
        print("8"*80)
        print ("Am I checking lengths?")
        print (errors)
        #if no fields are blank then do more validations
        if not errors:
            #check if the entered data and time match any other dates and times for this user
            user = User.objects.get(id = user_id)
            current_appointments = Appointment.objects.filter(created_by = user)
            for appointment in current_appointments:
                if parse_date(postData["date"]) == appointment.start_date and parse_date(postData["time"]) == appointment.start_time:
                    errors.append("Time slot already filled")
            print("8"*80)
            print ("Am I past checking lengths?")
            #if date equals today check time for future
            if parse_date(postData["date"]).date() == datetime.today().date():
                if parse_date(postData["time"]) < datetime.today():
                    errors.append("Appointment time must be in the future")

            #else if the date is not today that it's in the future
            elif parse_date(postData["date"]).date() < datetime.today().date():
                errors.append("Appointment date must be in the future")
        #might need a few more validations for time but lets run with this for now
        if not errors:
            user = User.objects.get(id = user_id)
            print("8"*80)
            print ("do i get a user?")
            print (user.name)
            date_from_form = parse_date(postData["date"])
            print (date_from_form)
            time_from_form = parse_date(postData["time"])
            print (time_from_form)
            appointment = self.create(task = postData["task"], created_by = user, start_date =  parse_date(postData["date"]), start_time =  parse_date(postData["time"]), status = "Pending")
            reply_to_veiws["appointment"] = appointment
            reply_to_veiws["status"] = True

        else:
            reply_to_veiws["errors"] = errors
            reply_to_veiws["status"] = False
        return reply_to_veiws

    def edit_appointment(self, postData, appointment_id):
        #make an appointment with validations
        reply_to_veiws = {}
        errors = []
        if not len(postData["task"]):
            errors.append("Please enter a task")
        if not len(postData["date"]):
            errors.append("Due Date can't be empty")
        if not len(postData["time"]):
            errors.append("Time can't be empty")
        print("8"*80)
        print ("Am I checking lengths?")
        print (errors)
        #if no fields are blank then do mroe validations
        if not errors:
            print("8"*80)
            print ("Am I past checking lengths?")
            #if date equals today check time for future
            if parse_date(postData["date"]).date() == datetime.today().date():
                if parse_date(postData["time"]) < datetime.today():
                    errors.append("Appointment time must be in the future")

            #else if the date is not today check that it's in the future
            elif parse_date(postData["date"]).date() < datetime.today().date():
                errors.append("Appointment date must be in the future")
        #might need a few more validations for time but lets run with this for now
        if not errors:
            date_from_form = parse_date(postData["date"])
            print (date_from_form)
            time_from_form = parse_date(postData["time"])
            print (time_from_form)
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
        print("8"*80)
        print ("Am I updating statuses?")
        all_appointments = Appointment.objects.all()
        for appointment in all_appointments:

            if not appointment.status == "Done" and (appointment.start_date <= date.today() and appointment.start_time < datetime.today().time() ):
                print("8"*80)
                print ("Am I making any changes to appointment statuses??")
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
