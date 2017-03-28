from django.shortcuts import render, HttpResponse, redirect
# Create your views here.

def index(request):
    return render(request, "login/index.html")

def next_page(request):
    return render(request, "login/next_page.html")
