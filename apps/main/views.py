from django.shortcuts import render, HttpResponse, redirect
from .. login.models import User
# Create your views here.

def index(request):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:index")
    #pass over my user to make it accessable in my template
    current_user = User.objects.get(id = request.session["user_id"])
    all_users = User.objects.all()
    context = {
        "current_user" : current_user,
        "all_users" : all_users,
    }
    return render(request, "main/index.html", context)

def next_page(request):
    if not "user_id" in request.session:
        return redirect ("login:index")
    return render(request, "main/next_page.html")
