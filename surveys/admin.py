from django.contrib import admin

from .models import Survey, Question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

class SurveyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Main', {
            'fields': (
                'survey_short_name',
                'deadline',
            ),

        }),
    )

    inlines = [QuestionInline]
    search_fields = ('survey_short_name', )
    

admin.site.register(Survey, SurveyAdmin)