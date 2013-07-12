# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class EditorImage(models.Model):
    image = models.ImageField(upload_to="editor-images/")
    created = models.DateTimeField(auto_now_add=True)

