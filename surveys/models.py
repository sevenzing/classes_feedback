from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import datetime
import random

from .managers import CustomUserManager

class Subject(models.Model):
    title = models.CharField(max_length=200, default='PS')
    description = models.CharField(max_length=1000, default='Default description')
    is_elective = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class Course(models.Model):
    DEGREE_CHOICES = [
        ('BS', 'Bachelor'),
        ('MS', 'Master'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    degree = models.CharField(max_length=2, choices=DEGREE_CHOICES, default='BS')
    year = models.CharField(max_length=2, default="19")

    def __str__(self):
        return f"{self.degree}-{self.year} {self.subject}"

class CourseGroup(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.CharField(max_length=2, default='01')
    all_groups = models.BooleanField(default=False)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, default="Nikolai")
    surname = models.CharField(max_length=200, default="Shilov")

    is_doe = models.BooleanField(default=False)
    is_prof = models.BooleanField(default=False)
    is_ta = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # can user access admin page?
    is_staff = models.BooleanField(default=False)
    # designates that this user has all permissions without explicitly assigning them
    is_superuser = models.BooleanField(default=False)
    
    courses = models.ManyToManyField(Course)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()
    
    def list_of_courses(self):
        return self.courses.all().__str__()

    def __str__(self):
        return self.email.__str__()

class Survey(models.Model):
    
    survey_short_name = models.CharField(max_length=100) 
    
    deadline = models.DateTimeField('deadline')

    # set default value to current time
    pub_date = models.DateTimeField(auto_now_add=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course} - \"{self.survey_short_name}\""

class Question(models.Model):
    question_text = models.CharField(max_length=200, default='Sample question text')

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question('{self.question_text}')"