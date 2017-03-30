from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from datetime import date, datetime
from dateutil.parser import parse as parse_date
from .. login.models import User
from .models import Trip

# Create your views here.

def index(request):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:index")

    current_user = User.objects.get(id = request.session["user_id"])
    my_trips = Trip.objects.filter(joined_by = request.session["user_id"])
    others_trips = Trip.objects.all().exclude(joined_by = request.session["user_id"])
    context = {
        "current_user" : current_user,
        "my_trips" : my_trips,
        "others_trips" : others_trips
    }
    return render(request, "main/index.html", context)

def create_trip(request):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:index")


    return render(request, "main/create_trip.html")

def confirm_create_trip(request):
    if not request.method == "POST":
        return redirect ("main:index")
    responce_from_model = Trip.objects.create_trip(request.POST, request.session["user_id"])
    if responce_from_model["status"]:
        messages.error(request, "You Planned a Trip")
        return redirect("main:index")
    else:
        for error in responce_from_model["errors"]:
            messages.error(request, error)
        return redirect("main:create_trip")

def view_trip(request, trip_id):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:index")
    if not request.method == "POST":
        return redirect ("main:index")
    current_trip = Trip.objects.get(id = trip_id)
    other_travlers = User.objects.filter(users_joined = trip_id).exclude(users_created_by = trip_id)
    context = {
        "current_trip" : current_trip,
        "other_travlers" : other_travlers,

    }

    return render(request, "main/view_trip.html", context)

def join_trip(request, trip_id ):
    if not request.method == "POST":
        return redirect ("main:index")

    Trip.objects.join_trip(request.session["user_id"], trip_id)

    return redirect("main:index")
