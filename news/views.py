# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from news.models import Article

def news(request):
  template = 'news/_w_news.html'
  articles = {'articles' : Article.objects.all()}
  return render(request, template, articles)

#################################################################################