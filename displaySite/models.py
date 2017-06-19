# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/bogdan/Documents/python/vkDonate/vkapi/class")
sys.path.append("/home/django/vkdonate/vkapi/class")

from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User

from User import User as vk_user
from Group import Group as vk_group

# Create your models here.

########################################################################################

class Admin(models.Model):

  def __str__(self):
    return str(self.admin_id)

  class Meta():
    db_table = "admins"

  @staticmethod
  def getDonations(request):
    return Donation.objects.filter(donation_admin = Admin.getUsername(request))

  @staticmethod
  def getDonaters(request):
    return Donater.objects.filter(donater_admin = Admin.getUsername(request))

  @staticmethod
  def getGroups(request):
    return Group.objects.filter(group_admin = Admin.getUsername(request))

  @staticmethod
  def getLastDonate(request):
    return Admin.getDonations(request)[:1]

  @staticmethod
  def hasDonaters(request):
    return Admin.getDonaters(request).exists()

  @staticmethod
  def hasDonations(request):
    return Admin.getDonaters(request).exists()

  @staticmethod
  def hasGroups(request):
    return Admin.getGroups(request).exists()

  @staticmethod
  def getUsername(request):
    return auth.get_user(request).username

  @staticmethod
  def isAuthenticated(request):
    return auth.get_user(request).is_authenticated

  admin_id = models.IntegerField(primary_key=True, unique=True)
  admin_token = models.CharField(max_length=200)
  user = models.OneToOneField(User)

########################################################################################

class Group(models.Model):

  def __str__(self):
    return str(self.group_id)

  class Meta():
    db_table = "groups"

  @staticmethod
  def getGroup(group):
    return Group.objects.get(group_id = group)

  @staticmethod
  def belongToAdmin(request, group):
    return Group.objects.filter(group_id = group,
      group_admin = Admin.getUsername(request)).exists()

  @staticmethod
  def getDonations(request, group):
    return Donation.objects.filter(donation_admin =
      Admin.objects.get(admin_id = Admin.getUsername(request)),
        donation_group = group)

  @staticmethod
  def countDonations(request, group):
    return Group.getDonations(request, group).count()

  @staticmethod
  def hasDonations(request, group):
    return Group.getDonations(request, group).exists()

  @staticmethod
  def getMaxDonate(request, group):
    return Group.getDonations(request, group).order_by('-donation_size')[:1].values()

  @staticmethod
  def getAverageDonate(request, group):
    from django.db.models import Avg
    if Group.hasDonations(request, group):
      averageDonate = Group.getDonations(request, group).aggregate(Avg('donation_size'))
      return round(averageDonate['donation_size__avg'], 1)
    else:
      return 0

  group_id = models.IntegerField(primary_key=True)
  group_admin = models.ForeignKey(Admin)
  group_summOfAllDonations = models.FloatField(default= 0)

########################################################################################

class Donater(models.Model):

  def __str__(self):
    return '%s %s' % (self.donater_firtstName.encode('utf8'), self.donater_secondName.encode('utf8'))

  class Meta():
    db_table = "donaters"
    ordering = ['donater_secondName']

  @staticmethod
  def getDonater(donater):
    return  Donater.objects.get(donater_id = donater)

  @staticmethod
  def getDonations(request, donater):
    return Donation.objects.filter(donation_admin =
      Admin.objects.get(admin_id = Admin.getUsername(request)),
        donation_donater = donater)

  @staticmethod
  def hasDonations(request, donater):
    return Donater.getDonations(request, donater).exists()

  @staticmethod
  def countDonations(request, donater):
    return Donater.getDonations(request, donater).count()

  @staticmethod
  def getAverageDonate(request, donater):
    from django.db.models import Avg
    if Donater.hasDonations(request, donater):
      averageDonate = Donater.getDonations(request, donater).aggregate(Avg('donation_size'))
      return round(averageDonate['donation_size__avg'], 1)
    else:
      return 0

  @staticmethod
  def getMaxDonate(request, donater):
    return Donater.getDonations(request, donater).order_by('-donation_size')[:1].values()

  @staticmethod
  def belongToAdmin(request, donater):
    return Donater.objects.filter(donater_id = donater,
      donater_admin = Admin.getUsername(request)).exists()

  donater_firtstName = models.CharField(max_length=50, default='FirstName')
  donater_secondName = models.CharField(max_length=50, default='SecondName')
  donater_id = models.IntegerField(primary_key=True)
  donater_admin = models.ForeignKey(Admin)
  donater_summOfAllDonations = models.FloatField(default= 0)

########################################################################################

class Donation(models.Model):

  def __str__(self):
    return '%s' % self.donation_text.encode('utf8')

  class Meta():
    db_table = "donations"
    ordering = ['-donation_date']

  donation_date = models.DateTimeField()
  donation_text = models.CharField(max_length=100)
  donation_size = models.FloatField()
  donation_donater = models.ForeignKey(Donater)
  donation_group = models.ForeignKey(Group)
  donation_admin = models.ForeignKey(Admin)
