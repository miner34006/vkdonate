# -*- coding: utf-8 -*-
import api_lib as VK

import json
import requests

class User():

    ID = None
    Information = None

    def __init__(self,id):
        self.ID = id
        self.Information = self.getUser()

    #Получение информации о пользователе
    def getUser(self, options = {}):
        options.update({'user_id': self.ID})
        data = VK.getRequest("users.get", options)
        return dict(data[0].items())

    @staticmethod
    def getFirstName(id):
      options = {}
      options.update({'user_id': id})
      data = VK.getRequest("users.get", options)
      data = dict(data[0].items())
      return data['first_name']

    @staticmethod
    def getLastName(id):
      options = {}
      options.update({'user_id': id})
      data = VK.getRequest("users.get", options)
      data = dict(data[0].items())
      return data['last_name']

    def getID(self):
        return self.ID




