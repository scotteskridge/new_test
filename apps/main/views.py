from django.shortcuts import render, HttpResponse, redirect
# Create your views here.

def index(request):
    return render(request, "main/index.html")

def next_page(request):
    return render(request, "main/next_page.html")
