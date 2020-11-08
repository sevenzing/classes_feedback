import json
import logging
from json.decoder import JSONDecodeError
from typing import List

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Answer, Course, Question, Student, Survey, Track


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
        fields = ['id', 'number', 'required',
                  'question_text', 'question_type', 'data']


class SurveysSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'survey_short_name',
                  'is_available', 'questions', 'course']


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


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question_id', 'data']

    def create(self, validated_data):
        return Answer(**validated_data)


class AnswerViewSet(viewsets.ViewSet):
    def create(self, request):
        data = JSONParser().parse(request)
        logging.debug(f"got request to create answer. data: {data}")
        try:
            answer = Answer(**data)
            answer.save()
            return JsonResponse({
                "success": True, 
                "id": answer.id
                })
        except Exception as e:
            logging.error(e)
            return JsonResponse({
                "success": False, 
                "error": e.__str__()
                }, status=status.HTTP_400_BAD_REQUEST)


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
