from django.shortcuts import render
from django.http import HttpResponse

def tast_list(request):
    return HttpResponse("To Do List")
