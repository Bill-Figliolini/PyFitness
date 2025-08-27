from django.urls import path

from . import views

app_name = "fitness"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("planner", views.planner, name="Workout Planner"),
    path("record", views.recordPage, name="Workout Record"),
]
