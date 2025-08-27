from django.shortcuts import render


# Create your views here.
def index(request):
    context = {}
    return render(request, "fitness/index.html", context)


def login(request):
    context = {}
    return render(request, "fitness/login.html", context)


def userDashboard(request):
    context = {}
    return render(request, "fitness/userDashboard.html", context)


def planner(request):
    context = {}
    return render(request, "fitness/planner.html", context)


def recordPage(request):
    context = {}
    return render(request, "fitness/record.html", context)
