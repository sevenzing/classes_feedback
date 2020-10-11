from django.test import TestCase
from django.contrib.auth import get_user_model

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from surveys.models import *

# various model testing

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

# user creation testing

class UserManagerTests(TestCase):
	'''
	Test for user creation
	'''
	def createUser(self):
		new_user = get_user_model()
		user = new_user.objects.create_user(email='elliot@local.com', password='alderson')
		self.assertEqual(user.email, 'elliot@local.com')
		self.assertTrue(user.is_active)
		self.assertTrue(user.is_staff)
		self.assertFalse(user.is_doe)
		self.assertFalse(user.is_ta)
		self.assertFalse(user.is_prof)
		self.assertFalse(user.is_superuser)

	'''
	Test for super user creation
	'''
	def createSuperuser(self):
		new_user = get_user_model()
		user = new_user.objects.create_superuser(email='admin@local.com', password='strong_password')
		self.assertEqual(user.email, 'admin@local.com')
		self.assertTrue(user.is_active)
		self.assertTrue(user.is_staff)
		self.assertFalse(user.is_doe)
		self.assertFalse(user.is_ta)
		self.assertFalse(user.is_prof)
		self.assertTrue(user.is_superuser)
