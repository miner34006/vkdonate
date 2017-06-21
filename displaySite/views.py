# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/bogdan/Documents/python/vkDonate/vkapi/class")
sys.path.append("/home/django/vkdonate/vkapi/class")
sys.path.append("/home/django/vkdonate/displaySite")

from django.shortcuts import render_to_response, redirect
from displaySite.models import Donater, Donation, Admin, Group
from django.core.paginator import Paginator
from django.db.models import Sum

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
     'max_donate': Donater.getMaxDonate(request, donater_id),
     'sum_donation': Donater.getSumOfDonations(request, donater_id),
     'average_donate': Donater.getAverageDonate(request, donater_id),
     'number_donations' : Donater.countDonations(request, donater_id),
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
    {'group_id' : group_id,
     'objects' : paginator.page(pageNumber),
     'pages' : paginator.num_pages,
     'objectName' : "currentGroup/get/%s" % group_id,
     'name' : vk_group.getName(group_id),
     'last_donate' : Admin.getLastDonate(request),
     'max_donate' : Group.getMaxDonate(request, group_id),
     'sum_donation' : Group.getSumOfDonations(request, group_id),
     'number_donation' : Group.countDonations(request, group_id),
     'average_donate': Group.getAverageDonate(request, group_id),
     'user_id' : Admin.getUsername(request)})

########################################################################################

def donaters(request, pageNumber = 1):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Admin.hasDonaters(request):
    return render_to_response \
      ('donaters.html',
      {'user_id': Admin.getUsername(request)})

  donaterList = Admin.getDonaters(request).annotate(donation_sum = Sum('donation__donation_size'))
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
  from utils import getGroupsPhoto, connectImgAndId

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
  from utils import dayDonator, monthDonator
  from User import User as vk_user

  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Admin.hasDonations(request):
    return render_to_response \
      ('statistics.html',
       {'user_id': Admin.getUsername(request),
        'has_data' : False})

  dayDonator = dayDonator(request)
  if dayDonator:
    day_donator_img = vk_user.getImage(dayDonator.donater_id)
  else:
    day_donator_img = None

  monthDonator = monthDonator(request)
  if monthDonator:
    month_donator_img = vk_user.getImage(monthDonator.donater_id)
  else:
    month_donator_img = None

  return render_to_response('statistics.html',
    {'last_donate': Admin.getLastDonate(request),
     'user_id': Admin.getUsername(request),
     'max_donate': Admin.GetMaxDonate(request),
     'number_donation' : Admin.getDonations(request).count(),
     'sum_donation' : Admin.getDonations(request).aggregate(Sum('donation_size'))['donation_size__sum'],
     'average_donate': Admin.getAverageDonate(request),
     'day_donator' : dayDonator,
     'day_donator_img' : day_donator_img,
     'month_donator_img': month_donator_img,
     'month_donator': monthDonator,
     'has_data': True})

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
