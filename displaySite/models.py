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
    return "%s %s" %(self.admin_firstName, self.admin_secondName)

  class Meta():
    db_table = "admins"

  @staticmethod
  def GetMaxDonate(request):
    from django.db.models import Max
    maxDonate = Admin.getDonations(request).aggregate(max_donate=Max('donation_size'))
    if maxDonate['max_donate'] == None:
      return 0
    else:
      return maxDonate['max_donate']

  @staticmethod
  def getAverageDonate(request):
    from django.db.models import Avg
    average = Admin.getDonations(request).aggregate(average_donate=Avg('donation_size'))
    if average['average_donate'] == None:
      return 0
    else:
      return average['average_donate']

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
    return Admin.getDonations(request).exists()

  @staticmethod
  def hasGroups(request):
    return Admin.getGroups(request).exists()

  @staticmethod
  def getUsername(request):
    return auth.get_user(request).username

  @staticmethod
  def isAuthenticated(request):
    return auth.get_user(request).is_authenticated

  admin_firstName = models.CharField(max_length=50, default="FirstName")
  admin_secondName = models.CharField(max_length=50, default="SecondName")
  admin_id = models.IntegerField(primary_key=True, unique=True)
  admin_token = models.CharField(max_length=200)
  user = models.OneToOneField(User)

########################################################################################

class Group(models.Model):

  def __str__(self):
    return "%s" % vk_group.getName(self.group_id)

  class Meta():
    db_table = "groups"

  @staticmethod
  def getSumOfDonations(request, group):
    from django.db.models import Sum
    donations = Group.getDonations(request, group).aggregate(donation_sum = Sum('donation_size'))
    if donations['donation_sum'] == None:
      return 0
    else:
      return donations['donation_sum']

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
    from django.db.models import Max
    maxDonate = Group.getDonations(request, group).aggregate(max_donate = Max('donation_size'))
    if maxDonate['max_donate'] == None:
      return 0
    else:
      return maxDonate['max_donate']

  @staticmethod
  def getAverageDonate(request, group):
    from django.db.models import Avg
    average = Group.getDonations(request, group).aggregate(average_donate=Avg('donation_size'))
    if average['average_donate'] == None:
      return 0
    else:
      return average['average_donate']

  group_id = models.IntegerField(primary_key=True)
  group_admin = models.ForeignKey(Admin)

########################################################################################

class Donater(models.Model):

  def __str__(self):
    return '%s %s' % (self.donater_firtstName, self.donater_secondName)

  class Meta():
    db_table = "donaters"
    ordering = ['donater_secondName']

  @staticmethod
  def getSumOfDonations(request, donater):
    from django.db.models import Sum
    donations = Donater.getDonations(request, donater).aggregate(donation_sum = Sum('donation_size'))
    if donations['donation_sum'] == None:
      return 0
    else:
      return donations['donation_sum']

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
    average = Donater.getDonations(request, donater).aggregate(average_donate = Avg('donation_size'))
    if average['average_donate'] == None:
      return 0
    else:
      return average['average_donate']

  @staticmethod
  def getMaxDonate(request, donater):
    from django.db.models import Max
    donation = Donater.getDonations(request, donater).aggregate(max_donate = Max('donation_size'))
    if donation['max_donate'] == None:
      return 0
    else:
      return donation['max_donate']

  @staticmethod
  def belongToAdmin(request, donater):
    return Donater.objects.filter(donater_id = donater,
      donater_admin = Admin.getUsername(request)).exists()

  donater_firtstName = models.CharField(max_length=50, default='FirstName')
  donater_secondName = models.CharField(max_length=50, default='SecondName')
  donater_id = models.IntegerField(primary_key=True)
  donater_admin = models.ForeignKey(Admin)

########################################################################################

class Donation(models.Model):

  def __str__(self):
    return '%s' % self.donation_text

  class Meta():
    db_table = "donations"
    ordering = ['-donation_date']

  donation_date = models.DateTimeField()
  donation_text = models.CharField(max_length=100)
  donation_size = models.IntegerField()
  donation_donater = models.ForeignKey(Donater)
  donation_group = models.ForeignKey(Group)
  donation_admin = models.ForeignKey(Admin)
