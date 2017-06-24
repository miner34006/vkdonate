# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/bogdan/Documents/python/vkDonate/vkapi/class")
sys.path.append("/home/django/vkdonate/vkapi/class")
sys.path.append("/home/django/vkdonate/displaySite")

from django.shortcuts import render_to_response, redirect, render
from displaySite.models import Donater, Admin, Group
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import Http404

from Group import Group as vk_group
from User import User as vk_user

from displaySite.utils import dayDonator, monthDonator
from displaySite.utils import getGroupsPhoto, connectImgAndId


def processor(request):
  "A context processor that provides 'url', 'user_id'"

  if Admin.isAuthenticated(request):
    return {
      'url': request.resolver_match.url_name,
      'user_id': Admin.getUsername(request),
      'last_donate': Admin.getLastDonate(request)
    }
  else:
    return {'url': request.resolver_match.url_name}


########################################################################################

def currentDonater(request, donater_id, pageNumber = 1):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Donater.belongToAdmin(request, donater_id):
    raise Http404

  donationList = Donater.getDonations(request, donater_id)
  paginator = Paginator(donationList, 10)

  template = 'displaySite/_w_donator_selected.html'
  context = {
    'donater': Donater.getDonater(donater_id),
    'objects': paginator.page(pageNumber),
    'pages': paginator.num_pages,
    'objectName': "currentDonater/get/%s" % donater_id,
    'max_donate': Donater.getMaxDonate(request, donater_id),
    'sum_donation': Donater.getSumOfDonations(request, donater_id),
    'average_donate': Donater.getAverageDonate(request, donater_id),
    'number_donation': Donater.countDonations(request, donater_id),
  }
  return render(request, template, context)

########################################################################################


@login_required
def currentGroup(request, group_id, pageNumber = 1):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  if not Group.belongToAdmin(request, group_id):
    from django.http import Http404
    raise Http404

  donationsList = Group.getDonations(request, group_id)
  paginator = Paginator(donationsList, 10)

  groups = getGroupsPhoto(Admin.getGroups(request))
  data = connectImgAndId(groups)

  data = {
          'objects': paginator.page(pageNumber),
          'pages': paginator.num_pages,
          'group_id': group_id,
          'objectName': "currentGroup/get/%s" % group_id,
          'name': vk_group.getName(group_id),
          'max_donate': Group.getMaxDonate(request, group_id),
          'sum_donation': Group.getSumOfDonations(request, group_id),
          'number_donation': Group.countDonations(request, group_id),
          'average_donate': Group.getAverageDonate(request, group_id),
  }
  return render_to_response('displaySite/_w_group_selected.html', data)

########################################################################################

def donators(request, pageNumber = 1):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  donaterList = Admin.getDonaters(request).annotate(donation_sum = Sum('donation__donation_size'))
  paginator = Paginator(donaterList, 1)

  template = 'displaySite/_w_donator_list.html'
  context = {
    'objects': paginator.page(pageNumber),
    'pages': paginator.num_pages,
    'objectName': "donators",
  }
  return render(request, template, context)

########################################################################################

def donations(request, pageNumber = 1):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  donationList = Admin.getDonations(request)
  paginator = Paginator(donationList, 1)

  template = 'displaySite/_w_donation_list.html'
  context = {
    'objects': paginator.page(pageNumber),
    'pages': paginator.num_pages,
    'objectName': "donations",
  }
  return render(request, template, context)

########################################################################################

def groups(request):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  groups = getGroupsPhoto(Admin.getGroups(request))
  context = connectImgAndId(groups)

  template = 'displaySite/_w_group_list.html'
  context.update({
    'last_donate' : Admin.getLastDonate(request),
    'user_id' : Admin.getUsername(request)
  })
  return render(request, template, context)

########################################################################################

def settings(request):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  groups = getGroupsPhoto(Admin.getGroups(request))
  context = connectImgAndId(groups)

  template = 'displaySite/_w_settings.html'

  context.update({
    'last_donate': Admin.getLastDonate(request),
    'user_id': Admin.getUsername(request)
  })
  return render(request, template, context)

########################################################################################

def statistics(request):
  if not Admin.isAuthenticated(request):
    return redirect('/')

  template = 'displaySite/_w_statistics.html'
  if not Admin.hasDonations(request):
    return render(request, template,{'has_data' : False})

  dayD = dayDonator(request)
  if dayD:
    day_donator_img = vk_user.getImage(dayD.donater_id)
  else:
    day_donator_img = None

  monthD = monthDonator(request)
  if monthD:
    month_donator_img = vk_user.getImage(monthD.donater_id)
  else:
    month_donator_img = None

  sum_donation = Admin.getDonations(request).aggregate(Sum('donation_size'))['donation_size__sum']
  if sum_donation == None:
    sum_donation = 0

  context = {
    'max_donate': Admin.GetMaxDonate(request),
    'number_donation': Admin.getDonations(request).count(),
    'sum_donation': sum_donation,
    'average_donate': Admin.getAverageDonate(request),
    'day_donator': dayD,
    'day_donator_img': day_donator_img,
    'month_donator_img': month_donator_img,
    'month_donator': monthD,
    'has_data': True
  }
  return render(request, template, context)

########################################################################################

def information(request):
  template = 'displaySite/_w_information.html'
  return render(request, template)



########################################################################################
