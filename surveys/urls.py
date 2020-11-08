from django.urls import path , include
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers

from . import rest_api
from . import views
from classes_feedback.settings import API_KEY

app_name = 'surveys'

router = routers.DefaultRouter()
router.register(r'survey', rest_api.SurveyViewSet, basename='survey')
router.register(r'student', rest_api.StudentViewSet, basename='student')
router.register(r'answer', rest_api.AnswerViewSet, basename='answer')

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api-auth/', include('rest_framework.urls')),
    path(f'api/{API_KEY}/', include(router.urls)),
    url(r'^login$', views.PTD_login_page, name='login'),
    url(r'^logout$', views.PTD_logout, name='logout'),
]

