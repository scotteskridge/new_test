from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from datetime import date, datetime
from dateutil.parser import parse as parse_date
from .. login.models import User
from .models import Appointment
# Create your views here.

def index(request):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:index")
    now = datetime.today()
    Appointment.objects.update_status()
    #pass over my user to make it accessable in my template
    current_user = User.objects.get(id = request.session["user_id"])
    #some logic to filter by date likely start with all appointments and then filter stuff out before shoving it into a context variable
    todays_appointments = Appointment.objects.filter(start_date = now, created_by = current_user ).order_by('start_time')
    #some logic to filter by date
    other_appointments = Appointment.objects.filter(created_by = current_user).exclude(start_date = now, ).order_by('start_date', 'start_time')

    context = {
        "current_user" : current_user,
        "todays_appointments" : todays_appointments,
        "other_appointments" : other_appointments,
        "now" : now
    }
    return render(request, "main/index.html", context)

def add_appointment(request):
    if not "user_id" in request.session:
        return redirect ("login:index")
    if not request.method == "POST":
        return redirect ("main:index")

    responce_from_model = Appointment.objects.create_appointment(request.POST, request.session["user_id"])

    if responce_from_model["status"]:
        messages.error(request, "You added an Appointment")
        return redirect("main:index")
    else:
        for error in responce_from_model["errors"]:
            messages.error(request, error)
        return redirect("main:index")

def edit_appointment(request, appointment_id):
    if not "user_id" in request.session:
        return redirect ("login:index")
    if not request.method == "POST":
        return redirect ("main:index")
    appointment = Appointment.objects.get(id = appointment_id)
    context = {
        "appointment" : appointment
    }

    return render(request, "main/edit_appointment.html", context)

def confirm_edit_appointment(request, appointment_id):
    if not "user_id" in request.session:
        return redirect ("login:index")
    if not request.method == "POST":
        return redirect ("main:index")
    appointment = Appointment.objects.get(id = appointment_id)
    responce_from_model = Appointment.objects.edit_appointment(request.POST, appointment_id, request.session["user_id"])
    context = {
        "appointment" : appointment
    }
    if responce_from_model["status"]:
        messages.error(request, "You updated an Appointment")
        return redirect("main:index")
    else:
        for error in responce_from_model["errors"]:
            messages.error(request, error)
        return render(request, "main/edit_appointment.html", context)



def delete_appointment(request, appointment_id):
    if not request.method == "POST":
        return redirect ("main:index")

    Appointment.objects.delete_appointment(appointment_id)
    return redirect("main:index")
