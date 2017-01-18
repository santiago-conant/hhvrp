from django.shortcuts import render
from django.http import HttpResponse

def capture(request):
    return HttpResponse("Hello, world. You're at the customers capture.")
