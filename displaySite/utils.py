import sys
sys.path.append("/home/bogdan/Documents/python/vkDonate/vkapi/class")
sys.path.append("/home/django/vkdonate/vkapi/class")

def getGroupsPhoto(groupList):
  """take groups information such as: link to image and id's"""
  from Group import Group as vk_group
  ids = []
  for group in groupList.values():
    ids.append(str(group["group_id"]))
  ids = ','.join(ids)
  data = vk_group.getGroupsImg(ids)
  return data

def connectImgAndId(groups):
  """Connect group_id with link to the group image for the future give to template"""
  data = {'data': []}
  for group in groups:
    data['data'].append({'link': group['img'], 'group_id': group['id']})
  return  data

def dayDonator(request):
  """return top donator of the day"""
  from displaySite.models import Donater, Admin
  import datetime
  from django.db.models import Sum, Q

  donater = Donater.objects.filter(donater_admin = Admin.getUsername(request))
  donater = donater.filter(donation__donation_date__date = datetime.date.today())\
    .annotate(sum_donations = Sum('donation__donation_size'))\
    .order_by('-sum_donations')[:1]

  if donater:
    return donater[0]
  else:
    return None


def monthDonator(request):
  """return top donator of the month"""
  from displaySite.models import Donater, Admin
  import datetime
  from django.db.models import Sum, Q

  donater = Donater.objects.filter(donater_admin=Admin.getUsername(request))
  donater = donater.filter(Q(donation__donation_date__month = datetime.date.today().month)\
                           &Q(donation__donation_date__year = datetime.date.today().year))\
                           .annotate(sum_donations=Sum('donation__donation_size'))\
                           .order_by('-sum_donations')[:1]

  if donater:
    return donater[0]
  else:
    return None