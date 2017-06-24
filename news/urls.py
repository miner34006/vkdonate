# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from news import views

urlpatterns = [
  url(r'^$', views.news, name="news"),
]
