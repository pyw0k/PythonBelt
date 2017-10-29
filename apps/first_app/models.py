from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    user_id = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField()