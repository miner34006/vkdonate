# -*- coding: utf-8 -*-

import api_lib as VK

class Group:

    __groupID = None

    def __init__(self,id):
        self.__groupID = id

    #Получение ID группы
    def getID(self):
        return self.__groupID
    
    #Получение фото группы
    def getPhoto(self):
        options = ({'group_id': self.__groupID})
        link = VK.getRequest("groups.getById", options)[0]["photo_200"]
        return link

    #Получение фото групп
    @staticmethod
    def getGroupsImg(str):
        options = ({'group_ids': str})
        link = VK.getRequest("groups.getById", options)
        give = []
        for i in link:
            give.append({'img':i["photo_200"], 'id':i['id']})
        return give
