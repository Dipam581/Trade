from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', call_function, name="call_function"),
    path('login/', initiate_login, name="initiate_login"),
    path('register/', register, name="register"),
]
