# -*- coding: utf-8 -*-
from django.conf.urls import url, include
# Импорт
from authorization import views

urlpatterns = [
    url(r'^logout/$', views.logout),
    url(r'^callback/', views.authorization),
]