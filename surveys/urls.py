from django.urls import path 

from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('create'),
]
