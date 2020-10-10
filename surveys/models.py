from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
import datetime
import random

from .managers import CustomUserManager

class Course(models.Model):
    name = models.CharField(max_length=100, default="ProbStat")
    year = models.CharField(max_length=4, default="BS19")


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, default="Nikolya")
    surname = models.CharField(max_length=200, default="Shilov")

    is_doe = models.BooleanField(default=False)
    is_prof = models.BooleanField(default=False)
    is_ta = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    courses = models.ManyToManyField(Course)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.email.__str__()

class Survey(models.Model):
    survey_short_name = models.CharField(max_length=100) 
    
    deadline = models.DateTimeField('deadline')

    # set default value to current time
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Survey('{self.survey_short_name}')"

class Question(models.Model):
    question_text = models.CharField(max_length=200, default='Sample question text')

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question('{self.question_text}')"