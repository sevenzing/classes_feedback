from rest_framework import routers, serializers, viewsets
from .models import Survey, Question, Course
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

import logging
from typing import List

router = routers.DefaultRouter()

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    subject = serializers.StringRelatedField()
    class Meta:
        model = Course
        fields = ['subject', 'degree', 'year', 'id']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'number', 'required', 'question_text', 'question_type', 'data']


class SurveysSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Survey
        fields = ['id','survey_short_name', 'deadline', 'questions', 'course']


class SurveyViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    
    serializer_class = SurveysSerializer
    
    def get_queryset(self):
        return Survey.objects.all()

router.register(r'survey', SurveyViewSet, basename='survey')