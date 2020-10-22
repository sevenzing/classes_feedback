from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import datetime
import random
import ast
import uuid 
from .managers import CustomUserManager
from surveys.config import BOT_ALIAS


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

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    degree = models.CharField(max_length=2, choices=DEGREE_CHOICES, default='BS')
    year = models.CharField(max_length=2, default="19")

    def __str__(self):
        return f"{self.degree}-{self.year} {self.subject}"

class CourseGroup(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coursegroups')
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
    is_staff = models.BooleanField(default=True)
    # designates that this user has all permissions without explicitly assigning them
    is_superuser = models.BooleanField(default=False)
    
    courses = models.ManyToManyField(Course)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()
    
    def has_perm(self, perm, obj=None):
        return super().has_perm(perm, obj=obj)

    def has_perms(self, perm_list, obj=None):
        return super().has_perms(perm_list, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_superuser or app_label in ('surveys',)

    def list_of_courses(self):
        return ', '.join(list(map(str, self.courses.all())))

    def __str__(self):
        return self.email.__str__()

def make_id() -> str:
        return random.randrange(16**8)

class Survey(models.Model):
    id = models.BigIntegerField(
        primary_key=True, 
        default = make_id, 
        editable = False
    )
    survey_short_name = models.CharField('Short name for survey', max_length=100) 
    
    deadline = models.DateTimeField('deadline')

    # set default value to current time
    pub_date = models.DateTimeField(auto_now_add=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='surveys')

    def __str__(self):
        return f"{self.course} - \"{self.survey_short_name}\""
    

    @property
    def url(self) -> str:
        return f"https://t.me/{BOT_ALIAS}?start={self.id}"

class Question(models.Model):
    TYPE_CHOICES = [
        (0, 'Single choice'),
        (1, 'Multichoice'),
        (2, 'Rate question'),
        (3, 'Input text'),
        ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    number = models.IntegerField('Order of question', default=1)
    required = models.BooleanField('Required', default=False)
    question_text = models.CharField('Text of question', max_length=200, default='Sample question text')
    question_type = models.SmallIntegerField('Question type', default=0, choices=TYPE_CHOICES)
    question_data = models.TextField('Content of question', default="['Sample choice 1', 'Sample choice 2']")

    @property
    def data(self):
        data = ast.literal_eval(self.question_data)
        assert isinstance(data, list), 'Data shoud be in form of list'
        return data

    def __str__(self):
        return f"Question('{self.question_text}')"
