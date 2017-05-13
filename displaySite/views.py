# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/bogdan/Documents/python/vkDonate/vkapi/class")

from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from displaySite.models import Donater, Donation, Admin, Group
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.models import User as SiteUser
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404

from User import User as vk_user
from Group import Group as vk_group

########################################################################################

#Главная страница
def mainPage(request):
  # Проверяем авторизован ли пользователь
  if auth.get_user(request).is_authenticated:

    # Выводим 'особую' страницу, когда у пользователя нет донатов
    if not Donation.objects.filter(donation_admin=
      Admin.objects.get(admin_id=int(auth.get_user(request).username))).exists():
      return render_to_response('voidMain.html',
        {'user_id': auth.get_user(request).username})

    #Если пользователь авторизован и у него есть донаты, отправляем ему 'обычную' страницу
    return render_to_response('mainPage.html',
      {'last_donate':Donation.objects.filter
        (donation_admin=auth.get_user(request).username)[:1],
       'user_id': auth.get_user(request).username})

  # Если пользователь не авторизован, ограничиваем информацию, расположенную на странице
  else:
    return render_to_response('voidMain.html',
      {'user_id': auth.get_user(request).username})

########################################################################################

def currentDonater(request, donater_id, pageNumber = 1):
  # Проверяем авторизован ли пользователь
  if auth.get_user(request).is_authenticated:

    # Проверяем наличие донатера у пользователя (донатили ли пользователю донатеры)
    get_object_or_404(Donater.objects.filter(donater_id=donater_id, donater_admin=auth.get_user(request).username))

    # Получем аватарку донатера
    user = vk_user(donater_id)
    image = user.getUser({'fields':'photo_200'})['photo_200']

    # Получаем все донаты, связанные с текущим донатером
    donationList = Donation.objects.filter(donation_donater = donater_id)

    # Пагинируем их по 10 штук
    paginator = Paginator(donationList, 10)

    return render_to_response('currentDonater.html',
      {'donater':Donater.objects.get(donater_id = donater_id),
       'donations':paginator.page(pageNumber),
       'paginator':paginator,
       'image':image,
       'last_donate':Donation.objects.filter
          (donation_admin=auth.get_user(request).username)[:1],
       'theBiggestSize': Donation.objects.filter(donation_donater = donater_id).order_by('-donation_size')[:1],
       'numberOfDonations':Donation.objects.filter(donation_donater = donater_id).count(),
       'user_id': auth.get_user(request).username})

  # Если пользователь не авторизован, перенаправялем его на главную страницу
  else:
    return redirect('/')

########################################################################################

def currentGroup(request, group_id, pageNumber = 1):
  #Проверяем авторизован ли пользователь
  if auth.get_user(request).is_authenticated:

    #Проверяем наличие группы у пользователя (является ли он её админом)
    get_object_or_404(Group.objects.filter(group_admin=auth.get_user(request).username, group_id=group_id))

    #Получем аватарку группы
    group = vk_group(group_id)
    image = group.getPhoto()

    #Получаем все донаты, связанные с текущей группой
    donationsList = Donation.objects.filter(donation_group=group_id)

    #Пагинируем их по 10 штук
    paginator = Paginator(donationsList, 10)

    return render_to_response('currentGroup.html',
      {'image':image,
       'id':group_id,
       'group_summOfAllDonations':Group.objects.get(group_id = group_id).group_summOfAllDonations,
       'donations':paginator.page(pageNumber),
       'paginator':paginator,
       'last_donate': Donation.objects.filter
          (donation_admin=auth.get_user(request).username)[:1],
       'theBiggestSize': Donation.objects.filter(donation_group=group_id).order_by('-donation_size')[:1],
       'numberOfDonations': Donation.objects.filter(donation_group=group_id).count(),
       'user_id': auth.get_user(request).username})

  # Если пользователь не авторизован, перенаправялем его на главную страницу
  else:
    return redirect('/')

########################################################################################

def donaters(request, pageNumber = 1):

  # Проверяем авторизован ли пользователь
  if auth.get_user(request).is_authenticated:

    #Выводим 'особую' страницу, когда у пользователя нет донатеров
    if not Donater.objects.filter(donater_admin=
      Admin.objects.get(admin_id=int(auth.get_user(request).username))).exists():
      return render_to_response \
        ('voidInfo.html',
         {'user_id': auth.get_user(request).username,
          'donater':True,
          'donation': False,
          'group': False})

    # Получаем всех донатеров, связанных с текущим пользователем
    donaterList = Donater.objects.filter(donater_admin=
      Admin.objects.get(admin_id=int(auth.get_user(request).username)))

    # Пагинируем их по 10 штук
    paginator = Paginator(donaterList, 10)

    return render_to_response\
      ('donaters.html',
        {'donaters': paginator.page(pageNumber),
         'paginator':paginator,
         'last_donate':Donation.objects.filter
            (donation_admin=auth.get_user(request).username)[:1],
         'user_id': auth.get_user(request).username})

  # Если пользователь не авторизован, перенаправялем его на главную страницу
  else:
    return redirect('/')

########################################################################################

def donations(request, pageNumber = 1):
  # Проверяем авторизован ли пользователь
  if auth.get_user(request).is_authenticated:

    # Выводим 'особую' страницу, когда у пользователя нет донатов
    if not Donation.objects.filter(donation_admin=
      Admin.objects.get(admin_id=int(auth.get_user(request).username))).exists():
      return render_to_response \
        ('voidInfo.html',
         {'user_id': auth.get_user(request).username,
          'donation':True,
          'donater':False,
          'group':False})

    #Получаем все донаты, связанные с текущим пользователем
    donationList = Donation.objects.filter(donation_admin=
      Admin.objects.get(admin_id=int(auth.get_user(request).username))).order_by('-donation_date')

    #Пагинируем их по 10 штук
    paginator = Paginator(donationList, 10)

    return render_to_response\
      ('donations.html',
        {'donations':paginator.page(pageNumber),
         'paginator':paginator,
         'last_donate':Donation.objects.filter
            (donation_admin=auth.get_user(request).username)[:1],
         'user_id':auth.get_user(request).username})

  # Если пользователь не авторизован, перенаправялем его на главную страницу
  else:
    return redirect('/')

########################################################################################

def groups(request):
  # Проверяем авторизован ли пользователь
  if auth.get_user(request).is_authenticated:

    # Выводим 'особую' страницу, когда у пользователя нет групп
    if not Group.objects.filter(group_admin=
      Admin.objects.get(admin_id=int(auth.get_user(request).username))).exists():
      return render_to_response \
        ('voidInfo.html',
         {'user_id': auth.get_user(request).username,
          'group': True,
          'donation':False,
          'donater':False,
          'showLastDonate':False})

    #Проверяем наличие групп у пользователя
    if Group.objects.filter(group_admin=auth.get_user(request).username).exists():

      #Получаем группы, связанные с админом
      data = Group.objects.filter(group_admin=auth.get_user(request).username)

      # Получаем аватарки групп
      links = {'data': []}
      ids = []
      for group in data.values():
        ids.append(str(group["group_id"]))
      ids = ','.join(ids)
      array = vk_group.getGroupsImg(ids)

      #Добавляем ссылку на фото и id группы
      for group in array:
        links['data'].append({'link': group['img'], 'group_id': group['id']})
      data = links

      #Добавляем последний донат
      data.update({'last_donate': Donation.objects.filter
        (donation_admin=auth.get_user(request).username)[:1]})

      #Добавляем аутентифицированного юзера
      data.update({'user_id': auth.get_user(request).username})

      return render_to_response('groups.html', data)

    #Если у пользователя нет групп
    else:
      data = ({'user_id': auth.get_user(request).username})
      return render_to_response('groups.html',data)

  # Если пользователь не авторизован, перенаправялем его на главную страницу
  else:
    return redirect('/')

########################################################################################