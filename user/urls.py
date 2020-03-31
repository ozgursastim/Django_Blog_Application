from django.contrib import admin
from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('register/', views.register, name = "register"),
    path('login/', views.loginuser, name = "loginuser"),
    path('logout/', views.logoutuser, name = "logoutuser"),
]