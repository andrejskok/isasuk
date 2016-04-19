from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import Http404

from django.contrib.auth import views
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Recovery
from .forms import *

import sys
import mandrill
mandrill_client = mandrill.Mandrill('vWEYy5TI1BFYISDBXOIJyA')


def send_reset_email(request, id, email):
    url = request.META['HTTP_ORIGIN'] + '/accounts/recovery/' + str(id)
    message = {
          'from_email': 'registracia@sportrank.sk',
          'from_name': 'Obnova hesla IS AS UK',
          'to': [{'email': email}],
          'html': 'Obnova hesla pre: <a href="' + url + '">' + url + '</a>',
      }
    mandrill_client.messages.send(message=message)

def login_user(request):
    if 'submit' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user and user.details.is_active is False:
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
            error = False
            form = LoginForm(request.POST) if 'submit' in request.POST else LoginForm()
            if 'submit' in request.POST:
                error = True
            return render_to_response('accounts/login.html', {'form': form, 'error': error}, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


def reset_view(request):
    send = False
    if 'submit' in request.POST:
        email = request.POST.get('email')
        users = User.objects.filter(email=email)
        if len(users) == 1:
            user = users[0]
            recovery = Recovery(
                user_id = user.id,
            )
            recovery.save()
            send_reset_email(request, recovery.id.hex, user.email)
            send = True
        send = True
    return render_to_response(
        'accounts/reset.html',
        {'send': send},
        context_instance=RequestContext(request))

def recovery_view(request, id):
    error = False
    if not id:
        raise Http404()
    recovery = Recovery.objects.filter(id=id)
    if len(recovery) != 1:
        raise Http404()
    recovery = recovery[0]
    if 'submit' in request.POST:
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if password != password:
            error = True
        else:
            user = User.objects.get(id=recovery.user_id)
            user.set_password(password)
            user.save()
            recovery.delete()
            login(request, user)
            return redirect('/home/')
    return render_to_response(
        'accounts/recovery.html',
        {'error': error},
        context_instance=RequestContext(request))
