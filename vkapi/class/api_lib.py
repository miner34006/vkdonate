# -*- coding: utf-8 -*-

import requests
import json

#Мой id
MY_ID_ = "6081502"

#Ссылка на API
API_LINK_ = "https://api.vk.com/method/"

#Токен
API_TOKEN = 'f476b87ff476b87ff476b87f8bf42a73a1ff476f476b87fad3eb8b88c74b8720746dda9'

#Версия API
V = '5.63'

def getRequest(get, options = {}):
  import time
  oldOptions = options
  options.update({'access_token': API_TOKEN, 'v': V})
  response = requests.get(API_LINK_ + get, options)
  data = json.loads(response.text)
  if 'error' in data:
    return getRequest(get, oldOptions)
  else:
    data = data['response']
    return data

