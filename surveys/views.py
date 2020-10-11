from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout

from .models import Survey, Course
from .forms import PTDLoginForm

class IndexView(generic.ListView):
    template_name = 'surveys/index.html'
    context_object_name = 'surveys_list'

    #def get_context_data(self, *args, **kwargs):
    #    return 

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            available_courses = Course.objects.all()
        else:
            available_courses = user.courses.all()
        return Survey.objects.all().filter(course__in=available_courses)
        
def PTD_login_page(request):
    uservalue = ''
    passwordvalue = ''
    form = PTDLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(email=email, password=password)
        if user is not None:
            # make log in the system
            login(request, user)
            # redirect to index
            return HttpResponseRedirect(reverse('surveys:index'))
        else:
            context= {'form': form,
                      'error': 'The email or password is incorrect'}
            # return error
            return render(request, 'registration/login.html', context)

    else:
        context= {'form': form}
        # GET request
        return render(request, 'registration/login.html', context)

def PTD_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('surveys:login'))