# -*- coding: utf-8 -*-

import requests
import json

#Мой id
MY_ID_ = "114193285"

#Ссылка на API
API_LINK_ = "https://api.vk.com/method/"

#Мой логин
MY_LOGIN_ = "miner34006@gmail.com"

#Токен
API_TOKEN = 'f7184d6f6ac19e294cfc882b02c5819894f578df303b7b43c47f254dcbe60da87ed0fd4e45e7a3bfb3cdb'

#Версия API
V = '5.63'

def getPassword():
	file = open("password.txt", "r")
	password = file.read()
	file.close()
	return password

def getRequest(get, options = {}):
	options.update({'access_token': API_TOKEN, 'v': V})
	response = requests.get(API_LINK_ + get, options)
	data = json.loads(response.text)
	data = data['response']
	return data

