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

  def __unicode__(self):
    return str(self.admin_id)

  class Meta():
    db_table = "admin"

  admin_id = models.IntegerField(primary_key=True, unique=True)
  admin_token = models.CharField(max_length=200)
  user = models.OneToOneField(User)

########################################################################################

class Group(models.Model):

  def __unicode__(self):
    return str(self.group_id)

  class Meta():
    db_table = "group"

  group_id = models.IntegerField(primary_key=True)
  group_admin = models.ForeignKey(Admin)
  group_summOfAllDonations = models.BigIntegerField(default= 0)

########################################################################################

class Donater(models.Model):

  def __unicode__(self):
    return '%s %s' % (self.donater_firtstName, self.donater_secondName)

  class Meta():
    db_table = "donater"
    ordering = ['donater_secondName']

  donater_firtstName = models.CharField(max_length=50, default='FirstName')
  donater_secondName = models.CharField(max_length=50, default='SecondName')
  donater_id = models.IntegerField(primary_key=True)
  donater_admin = models.ForeignKey(Admin)
  donater_summOfAllDonations = models.BigIntegerField(default= 0)

########################################################################################

class Donation(models.Model):

  def __unicode__(self):
    return '%s' % (self.donation_text)

  class Meta():
    db_table = "donation"
    ordering = ['-donation_date']

  donation_date = models.DateTimeField()
  donation_text = models.CharField(max_length=100)
  donation_size = models.IntegerField()
  donation_donater = models.ForeignKey(Donater)
  donation_group = models.ForeignKey(Group)
  donation_admin = models.ForeignKey(Admin)
