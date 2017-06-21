# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/bogdan/Documents/python/vkDonate/vkapi/class")
sys.path.append("/home/django/vkdonate/vkapi/class")

sys.path.append("/home/bogdan/Documents/python/vkDonate/authorization")
sys.path.append("/home/django/vkdonate/authorization")

from displaySite.models import Admin
from django.contrib import auth
from django.shortcuts import redirect

import requests
import re

from utils import createUser, sendRegistrationMail

########################################################################################

def authorization(request):

  if request.GET.get('error'):
    return redirect('/')

  code = request.GET.get('code')
  url = 'https://oauth.vk.com/access_token?client_id=6020313&client_secret=0keFBizaFCyyD8YJo93s' \
        '&redirect_uri=http://vkdonate.ru/auth/callback/' \
        '&code=%s' % code
  data = requests.get(url).text
  id = re.findall(r'user_id":(\d+)', data)[0]

  if Admin.objects.filter(admin_id = int(id)).exists():
    user = auth.authenticate(username = id)
    auth.login(request, user)
    return redirect('/')
  else:
    createUser(id, data)

    user = auth.authenticate(username = id)
    auth.login(request, user)

    sendRegistrationMail(id)

    return redirect('/')

########################################################################################

def logout(request):
  auth.logout(request)
  return redirect("/")

########################################################################################