from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def view_one(request):
    return HttpResponse("This is the first view of anotherapp.")

def view_two(request):
    return HttpResponse("This is the second view of anotherapp.")
