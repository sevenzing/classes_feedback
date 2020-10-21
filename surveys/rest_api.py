from rest_framework import routers, serializers, viewsets
from .models import Survey, Question
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

import logging
from typing import List

router = routers.DefaultRouter()

class SurveysSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Survey
        fields = ['survey_short_name', 'deadline']

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['number', 'required', 'question_text', 'question_type', 'data']

class SurveyViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def get_quesitons(self, survey: Survey) -> List[QuestionSerializer]:
        questions = survey.questions.all()
        q_ = []
        for question in questions:
            q_.append(QuestionSerializer(question).data)
        
        return q_

    def retrieve(self, request, pk=None):
        queryset = Survey.objects.all()
        survey = get_object_or_404(queryset, pk=pk)
        serializer = SurveysSerializer(survey)
        data = serializer.data
        data['questions'] = self.get_quesitons(survey)
        logging.warning(data)
        return Response(data)

    queryset = Survey.objects.none() 
router.register(r'users', SurveyViewSet, basename='user')