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