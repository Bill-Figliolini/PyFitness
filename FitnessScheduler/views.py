from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("Hello World, Welcome to fitness Tracker")


def login(request) -> HttpResponse:
    return HttpResponse("TODO - Login")


def userDashboard(request) -> HttpResponse:
    return HttpResponse("TODO - Dashboard")


def planner(request) -> HttpResponse:
    return HttpResponse("TODO - Planner")


def recordPage(request) -> HttpResponse:
    return HttpResponse("TODO - Records")
