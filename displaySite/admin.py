# -*- coding: utf-8 -*-

from django.contrib import admin
from displaySite.models import Donation, Donater, Admin, Group

# Register your models here.

#Вычисляет сколько задонатил каждый пользователь
def count_donations_for_donater(modeladmin, request, queryset):
  for donater in queryset:
    sum = 0
    for donation in Donation.objects.filter(donation_donater=donater.donater_id):
      sum += donation.donation_size
      donater.donater_summOfAllDonations = sum
    donater.save()

#Вычисляет сколько задонатили в группе
def count_donations_for_group(modeladmin, request, queryset):
  for group in queryset:
    sum = 0
    for donation in Donation.objects.filter(donation_group=group.group_id):
      sum += donation.donation_size
      group.group_summOfAllDonations = sum
    group.save()

count_donations_for_donater.short_description = "Count donations!"
count_donations_for_group.short_description = "Count donations!"

class DonaterAdmin(admin.ModelAdmin):
  actions = [count_donations_for_donater]

class GroupAdmin(admin.ModelAdmin):
  actions = [count_donations_for_group]

admin.site.register(Donation)
admin.site.register(Donater, DonaterAdmin)
admin.site.register(Admin)
admin.site.register(Group, GroupAdmin)
