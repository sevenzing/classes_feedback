from django.db import models
from django.utils import timezone

import datetime
import random

class Survey(models.Model):
    survey_short_name = models.CharField(max_length=100) 
    
    deadline = models.DateTimeField('deadline')

    # set default value to current time
    pub_date = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    question_text = models.CharField(max_length=200, default='Sample question text')

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
