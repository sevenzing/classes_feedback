from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Survey

class IndexView(generic.ListView):
    template_name = 'surveys/index.html'
    context_object_name = 'surveys_list'

    def get_queryset(self):
        return Survey.objects.order_by('-pub_date')