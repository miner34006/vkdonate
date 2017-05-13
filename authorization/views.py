# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from displaySite.models import Admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from importlib import import_module
from django.http import HttpResponse

import requests
import re

from django.shortcuts import render

########################################################################################

def authorization(request):
  code = request.GET.get('code')
  url = 'https://oauth.vk.com/access_token?client_id=6020313&client_secret=0keFBizaFCyyD8YJo93s' \
        '&redirect_uri=http://vkdonate.ru/auth/callback/' \
        '&code=%s' % code
  data = requests.get(url).text
  id = re.findall(r'user_id":(\d+)', data)[0]
  token = re.findall(r'access_token":"(\w+)"',data)[0]

  if Admin.objects.filter(admin_id=int(id)).exists():
    admin = Admin.objects.get(admin_id=int(id))
    admin.admin_token = token
    admin.save()
    user = auth.authenticate(username=id)
    auth.login(request, user)
    return redirect('/')
  else:
    user = User.objects.create_user(username=int(id), password=int(id))
    user.save()
    admin = Admin(admin_id=int(id), admin_token=token, user=user)
    admin.save()
    user = auth.authenticate(username=id)
    auth.login(request, user)
    return redirect('/')

########################################################################################

def logout(request):
  auth.logout(request)
  return redirect("/")

########################################################################################