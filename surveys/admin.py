from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Survey, Question, Course, Subject, Track, Student, Answer, Question
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

import logging

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
        '''
        Returns a query set of only those courses that can be accessed.
        If superuser, than returns full query
        '''
        q = super().get_queryset(request)
        user = request.user 
        if user.is_superuser:
            return q
        return q.filter(id__in=user.courses.all())

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'track')
    fields = ('email', 'track')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'data')

class SurveyAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        '''
        Returns a query set of only those surveys that can be accessed.
        If superuser, than returns full query
        '''
        q = super().get_queryset(request)
        user = request.user 
        if user.is_superuser:
            return q
        return q.filter(course__in=user.courses.all())
    list_display = ('__str__', 'url', 'deadline')
    list_filter = ('course',)
    fieldsets = (
        ('Main', {
            'fields': (
                'survey_short_name',
                'deadline',
                'course',
            ),

        }),
    )

    inlines = [QuestionInline]
    search_fields = ('survey_short_name', )
    
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_superuser', 'name', 'surname', 'list_of_courses')
    list_filter = ('email', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'surname')}),
        ('Group', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('is_staff', 'is_doe', 'is_ta', 'is_prof', 'is_active')}),
        ('Courses', {'fields': ('courses', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ()
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Survey, SurveyAdmin)