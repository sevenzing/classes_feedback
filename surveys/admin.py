from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Survey, Question
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

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
    
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'name', 'surname')
    list_filter = ('email', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'surname')}),
        ('Permissions', {'fields': ('is_doe', 'is_ta', 'is_prof', 'is_active')}),
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