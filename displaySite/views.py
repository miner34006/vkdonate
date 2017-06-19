# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/bogdan/Documents/python/vkDonate/vkapi/class")
sys.path.append("/home/django/vkdonate/vkapi/class")

from django.shortcuts import render_to_response, redirect
from displaySite.models import Donater, Donation, Admin, Group
from django.core.paginator import Paginator

########################################################################################

def currentDonater(request, donater_id, pageNumber = 1):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Donater.belongToAdmin(request, donater_id):
    from django.http import Http404
    raise Http404

  donationList = Donater.getDonations(request, donater_id)
  paginator = Paginator(donationList, 10)

  return render_to_response('currentDonater.html',
    {'donater' : Donater.getDonater(donater_id),
     'objects' : paginator.page(pageNumber),
     'pages' : paginator.num_pages,
     'objectName': "currentDonater/get/%s" % donater_id,
     'last_donate': Admin.getLastDonate(request),
     'maxDonate': Donater.getMaxDonate(request, donater_id),
     'averageDonate': Donater.getAverageDonate(request, donater_id),
     'numberOfDonations' : Donater.countDonations(request, donater_id),
     'user_id' : Admin.getUsername(request)})

########################################################################################

def currentGroup(request, group_id, pageNumber = 1):
  from Group import Group as vk_group

  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Group.belongToAdmin(request, group_id):
    from django.http import Http404
    raise Http404

  donationsList = Group.getDonations(request, group_id)
  paginator = Paginator(donationsList, 10)

  return render_to_response('currentGroup.html',
    {'group' : Group.getGroup(group_id),
     'objects' : paginator.page(pageNumber),
     'pages' : paginator.num_pages,
     'objectName' : "currentGroup/get/%s" % group_id,
     'name' : vk_group.getName(group_id),
     'last_donate' : Admin.getLastDonate(request),
     'maxDonate' : Group.getMaxDonate(request, group_id),
     'numberOfDonations' : Group.countDonations(request, group_id),
     'averageDonate': Group.getAverageDonate(request, group_id),
     'user_id' : Admin.getUsername(request)})

########################################################################################

def donaters(request, pageNumber = 1):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Admin.hasDonaters(request):
    return render_to_response \
      ('donaters.html',
      {'user_id': Admin.getUsername(request)})

  donaterList = Admin.getDonaters(request)
  paginator = Paginator(donaterList, 10)

  return render_to_response\
    ('donaters.html',
      {'objects': paginator.page(pageNumber),
       'pages': paginator.num_pages,
       'objectName' : "donaters",
       'last_donate': Admin.getLastDonate(request),
       'user_id': Admin.getUsername(request)})

########################################################################################

def donations(request, pageNumber = 1):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Admin.hasDonations(request):
    return render_to_response \
      ('donations.html',
       {'user_id': Admin.getUsername(request)})

  donationList = Admin.getDonations(request)
  paginator = Paginator(donationList, 10)

  return render_to_response\
    ('donations.html',
      {'objects':paginator.page(pageNumber),
       'pages': paginator.num_pages,
       'objectName': "donations",
       'last_donate': Admin.getLastDonate(request),
       'user_id': Admin.getUsername(request)})

########################################################################################

def groups(request):
  from  utils import getGroupsPhoto, connectImgAndId

  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Admin.hasGroups(request):
    return render_to_response \
      ('groups.html',
       {'user_id': Admin.getUsername(request)})

  groups = getGroupsPhoto(Admin.getGroups(request))

  data = connectImgAndId(groups)
  data.update({'last_donate': Admin.getLastDonate(request),
               'user_id': Admin.getUsername(request)})
  return render_to_response('groups.html', data)

########################################################################################

def settings(request):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Admin.hasDonations(request):
    return render_to_response \
      ('settings.html',
       {'user_id': Admin.getUsername(request)})

  return render_to_response('settings.html',
    {'last_donate': Admin.getLastDonate(request),
     'user_id': Admin.getUsername(request)})

########################################################################################

def statistics(request):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Admin.hasDonations(request):
    return render_to_response \
      ('statistics.html',
       {'user_id': Admin.getUsername(request)})

  return render_to_response('statistics.html',
    {'last_donate': Admin.getLastDonate(request),
     'user_id': Admin.getUsername(request)})

########################################################################################

def information(request):
  if not Admin.isAuthenticated(request):
    return render_to_response('information.html')

  if not Admin.hasDonations(request):
    return render_to_response \
      ('information.html',
       {'user_id': Admin.getUsername(request)})

  return render_to_response('information.html',
    {'last_donate': Admin.getLastDonate(request),
     'user_id': Admin.getUsername(request)})



########################################################################################
