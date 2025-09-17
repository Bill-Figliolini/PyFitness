from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User
from fitness.models import Exercise

# Register your models here.
admin.site.register(Exercise)
