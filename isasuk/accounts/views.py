from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect

from django.contrib.auth import views
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from .forms import *

import sys

def login_user(request):
    if 'submit' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user.details.is_active is False:
            return None
        return user
    return None

def login_view(request):
    if request.user.is_authenticated():
        return redirect('/home/')
    else:
        t = login_user(request)
        if t is not None:
            login(request, t)
            return redirect('/home/')
        else:
            form = LoginForm(request.POST) if 'submit' in request.POST else LoginForm()
            return render_to_response('accounts/login.html', {'form': form}, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')
