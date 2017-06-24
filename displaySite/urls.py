# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from displaySite import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  url(r'^settings/$', views.settings, name="settings"),
  url(r'^statistics/$', views.statistics, name="statistics"),
  url(r'^information/$', views.information, name="information"),
  url(r'^groups/$', views.groups, name="groups"),
  url(r'^donations/$', views.donations, name="donations"),
  url(r'^donations/page/(\d+)/$', views.donations, name="donations_page"),
  url(r'^donators/$', views.donators, name="donators"),
  url(r'^donators/page/(\d+)/$', views.donators, name="donators_page"),
  url(r'^currentDonator/get/(?P<donater_id>\w+)/$', views.currentDonater, name="select_donator"),
  url(r'^currentDonator/get/(\d+)/page/(\d+)/$', views.currentDonater, name="select_donator_page"),
  url(r'^currentGroup/get/(?P<group_id>\w+)/$', views.currentGroup, name="select_group"),
  url(r'^currentGroup/get/(\d+)/page/(\d+)/$', views.currentGroup, name="select_group_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
