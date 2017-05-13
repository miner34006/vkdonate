# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from displaySite import views

urlpatterns = [
    url(r'^$', views.mainPage),
    url(r'^groups/$', views.groups),
    url(r'^donations/$', views.donations),
    url(r'^donations/page/(\d+)/$', views.donations),
    url(r'^donaters/$', views.donaters),
    url(r'^donaters/page/(\d+)/$', views.donaters),
    url(r'^currentDonater/get/(?P<donater_id>\w+)/$', views.currentDonater),
    url(r'^currentDonater/get/(\d+)/page/(\d+)/$', views.currentDonater),
    url(r'^currentGroup/get/(?P<group_id>\w+)/$', views.currentGroup),
    url(r'^currentGroup/get/(\d+)/page/(\d+)/$', views.currentGroup),
]
