from django.urls import path , include
from django.conf.urls import url
from django.contrib import admin

from . import views

from .rest_api import router

app_name = 'surveys'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    url(r'^login$', views.PTD_login_page, name='login'),
    url(r'^logout$', views.PTD_logout, name='logout'),   
]

