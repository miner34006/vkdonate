# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from displaySite import views
from news import views as new

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^currentarticle/(?P<article_id>\d+)/$', new.currentArticle),
    url(r'^$', new.news),

    url(r'^groups/$', views.groups),
    url(r'^donations/$', views.donations),
    url(r'^donations/page/(\d+)/$', views.donations),
    url(r'^donaters/$', views.donaters),
    url(r'^donaters/page/(\d+)/$', views.donaters),
    url(r'^currentDonater/get/(?P<donater_id>\w+)/$', views.currentDonater),
    url(r'^currentDonater/get/(\d+)/page/(\d+)/$', views.currentDonater),
    url(r'^currentGroup/get/(?P<group_id>\w+)/$', views.currentGroup),
    url(r'^currentGroup/get/(\d+)/page/(\d+)/$', views.currentGroup),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
