# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from displaySite.models import Donater, Donation, Admin, Group
from news.models import Article
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.models import User as SiteUser
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.db.models import Avg

def news(request):
  # Проверяем авторизован ли пользователь
  if auth.get_user(request).is_authenticated:

    # Выводим 'особую' страницу, когда у пользователя нет донатов
    if not Donation.objects.filter(donation_admin=
    Admin.objects.get(admin_id=int(auth.get_user(request).username))).exists():
      return render_to_response('news.html',
      {'user_id': auth.get_user(request).username,
       'articles': Article.objects.all()})

    # Если пользователь авторизован и у него есть донаты, отправляем ему 'обычную' страницу
    return render_to_response('news.html',
    {'last_donate': Donation.objects.filter(donation_admin=auth.get_user(request).username)[:1],
     'user_id': auth.get_user(request).username,
     'articles': Article.objects.all()})

  # Если пользователь не авторизован, ограничиваем информацию, расположенную на странице
  else:
    return render_to_response('news.html',
    {'user_id': auth.get_user(request).username,
     'articles': Article.objects.all()})

#################################################################################

""""
def currentArticle(request, article_id):
  # Проверяем авторизован ли пользователь
  if auth.get_user(request).is_authenticated:

    # Выводим 'особую' страницу, когда у пользователя нет донатов
    if not Donation.objects.filter(donation_admin=
      Admin.objects.get(admin_id=int(auth.get_user(request).username))).exists():
        return render_to_response('currentArticle.html',
        {'user_id': auth.get_user(request).username,
         'article': Article.objects.get(id = article_id),
         'last_articles':Article.objects.all().order_by()[:1]})

    # Если пользователь авторизован и у него есть донаты, отправляем ему 'обычную' страницу
    return render_to_response('currentArticle.html',
      {'last_donate': Donation.objects.filter
       (donation_admin=auth.get_user(request).username)[:1],
       'user_id': auth.get_user(request).username,
       'article': Article.objects.get(id = article_id),
       'last_articles': Article.objects.all().order_by()[:1]})

    # Если пользователь не авторизован, ограничиваем информацию, расположенную на странице
  else:
    return render_to_response('currentArticle.html',
    {'user_id': auth.get_user(request).username,
    'article': Article.objects.get(id = article_id),
    'last_articles': Article.objects.all().order_by()[:1]})
"""""