# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from displaySite.models import Admin
from news.models import Article

def news(request):
  if not Admin.isAuthenticated(request):
    return render_to_response('news.html',
    {'articles': Article.objects.all()})

  if not Admin.hasDonations(request):
    return render_to_response('news.html',
      {'user_id': Admin.getUsername(request),
       'articles': Article.objects.all()})

  return render_to_response('news.html',
  {'last_donate': Admin.getLastDonate(request),
   'user_id': Admin.getUsername(request),
   'articles': Article.objects.all()})

#################################################################################