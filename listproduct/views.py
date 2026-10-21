from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def hello(request):
    return HttpResponse("Hello, world. You're at the listproduct index.")

def second_method(request):
    return HttpResponse("This is the second method in the listproduct app.")

