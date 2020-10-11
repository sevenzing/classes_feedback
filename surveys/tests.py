from django.test import TestCase

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from surveys.models import *

class QuestionModelTests(TestCase):
	'''
	Test for question object creation
	'''
	def createQuestion(question_text):
		return Question.objects.create(question_text=question_text,)

class SurveyModelTests(TestCase):
	'''
	Test for survey object creation
	'''
	def createSuvey(survey_short_name):
		return Survey.objects.create(survey_short_name=survey_short_name,)

class CourseeGroupModelTests(TestCase):
	'''
	Test for group object creation
	'''
	def createCourseGroup(number):
		return CourseGroup.objects.create(number=number,)
