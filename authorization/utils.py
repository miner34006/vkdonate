def random_id(length = 8, strong = False):
  import random
  import string

  rid = ''
  for x in range(length):
    rid += random.choice(('!@#$%^&*()_-+=' if strong else '') + string.ascii_letters + string.digits)
  return rid

def createUser(id, data):
  import sys
  sys.path.append("/home/bogdan/Documents/python/vkDonate/vkapi/class")
  sys.path.append("/home/django/vkdonate/vkapi/class")
  from User import User as vk_user
  from displaySite.models import Admin
  from django.contrib.auth.models import User
  import re

  user = User.objects.create_user(username=int(id), password=random_id(15, True),
                                  first_name=vk_user.getENFirstName(id), last_name=vk_user.getENLastName(id))
  user.save()
  token = re.findall(r'access_token":"(\w+)"', data)[0]

  admin = Admin(admin_id=int(id), admin_token=token, user=user,
                admin_firstName=vk_user.getENFirstName(id), admin_secondName=vk_user.getENLastName(id))
  admin.save()
  return user

def sendRegistrationMail(id):
  """Send mail when new user has registered"""
  from django.core.mail import send_mail
  from User import User as vk_user
  from django.conf import settings

  subject = "New user registration"
  message = "New registration on vkDonate. " \
            "User %s %s with id %d has been registered on vkDonate. " \
            "My congratulations master." \
            % (vk_user.getFirstName(id), vk_user.getLastName(id), int(id))

  send_mail(subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER])
