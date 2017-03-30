from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from datetime import date, datetime
from dateutil.parser import parse as parse_date
from .. login.models import User

# Create your views here.

def index(request):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:index")
    now = datetime.today()
    current_user = User.objects.get(id = request.session["user_id"])
    context = {
        "current_user" : current_user,
        "now" : now
    }
    return render(request, "main/index.html", context)
