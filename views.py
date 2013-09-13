# coding=utf-8

from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from registration_auth.forms import RegistrationForm, LoginForm
from django.contrib import auth
from django.shortcuts import render

def registration(request, template='user_management/login.html'):

    context = {'login_form': LoginForm()}

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()


            # если нужна активация по email
            # берем никнайем юзера как ключ активации (он случайно сгенерирован)
            # отправка письма с кодом активации
    else:
        registration_form = RegistrationForm()

    context['registration_form'] = registration_form
    return render(request, template, context)

def login(request, template='user_management/login.html'):
    context = {'registration_form': RegistrationForm()}

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=login_form.cleaned_data['email'],
                                     password=login_form.cleaned_data['password'])
            auth.login(request, user)
            return HttpResponseRedirect('/profile/')
    else:
        login_form = LoginForm()

    context['login_form'] = login_form
    return render(request, template, context)

def auth_page(request, template='user_management/login.html'):
    context = {'registration_form': RegistrationForm(), 'login_form': LoginForm()}
    return render(request, template, context)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/auth/enter/')