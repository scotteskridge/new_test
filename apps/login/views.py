from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
# Create your views here.
# should need

def index(request):



    return render(request, "login/index.html")

def login(request):
    if not request.method == "POST":
        return redirect ("login:index")
    reply_from_model = User.objects.login(request.POST)
    #if login status is true
    if reply_from_model["status"]:
        #return redirect("login:success")
        #save user id to session
        request.session["user_id"] = reply_from_model["user"].id
        return redirect("login:success")
    # if login status is false
    else:
        for error in reply_from_model["errors"]:
            messages.error(request, error)
        return redirect ("login:index")


def register(request):
    if not request.method == "POST":
        return redirect ("login:index")
    reply_from_model = User.objects.register(request.POST)
    #if login status is true
    if reply_from_model["status"]:
        #return redirect("login:success")
        #save user id to session
        request.session["user_id"] = reply_from_model["user"].id
        return redirect("login:success")
    # if login status is false
    else:
        for error in reply_from_model["errors"]:
            messages.error(request, error)
        return redirect ("login:index")

def success(request):
    
    # don't forget to filter to ensure that there is a user_id in sessions
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:index")
    return redirect("main:index")


def logout(request):
    request.session.clear()
    messages.error(request, "You are now logged out")
    return redirect("login:index")
