#from django.http import HttpRequest
# from django.template import loader
from django.shortcuts import render
import json

def index(request):
    return render(request, 'index.html')
