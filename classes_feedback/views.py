from django.shortcuts import redirect

def redirect_to_surveys(request):
    response = redirect('surveys/')
    return response