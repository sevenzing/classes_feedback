from rest_framework import  serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Survey, Question, Course, Student, Track

from json.decoder import JSONDecodeError
import json
from typing import List
import logging

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['degree', 'year', 'id']

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    subject = serializers.StringRelatedField()
    track = TrackSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ['track', 'subject', 'id']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'number', 'required', 'question_text', 'question_type', 'data']


class SurveysSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Survey
        fields = ['id','survey_short_name', 'is_available', 'questions', 'course']


class SurveyViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    
    serializer_class = SurveysSerializer
    
    def get_queryset(self):
        return Survey.objects.all()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email']
    

class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post', 'get'])    
    def validate(self, request):
        logging.warning(f'Got data: {request.body}')
            
        try:
            data = json.loads(request.body)
            assert isinstance(data, dict)
            email, code = data['email'], data['code']
        except (AssertionError, JSONDecodeError) as e:
            return Response({'error': 'Incorrect format. Send json bytes'})
        except KeyError:
            return Response({'error': 'email and code field does\'t provided'})

        try:
            student: Student = Student.objects.get(email=email, code=code)
        except Student.DoesNotExist:
            return Response({'confirmed': False})

        return Response({'confirmed': True, 'track': TrackSerializer(student.track).data})
            