# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Article(models.Model):

  class Meta():
    db_table = "articles"
    ordering = ['-article_datePub']

  article_title = models.CharField(max_length=100)
  article_text = models.CharField(max_length=1000)
  article_datePub = models.DateTimeField()
  article_image = models.ImageField(upload_to = 'images/')