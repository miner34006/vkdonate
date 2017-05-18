# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Article(models.Model):
  article_title = models.CharField(max_length=100)
  article_text = models.CharField(max_length=1000)
  #article_date = models.DateField()
  article_image = models.ImageField(upload_to = 'images/')