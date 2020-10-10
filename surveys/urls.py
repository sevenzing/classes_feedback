from django.urls import path 
from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    url(r'^login$', views.PTD_login_page, name='login')    
]
