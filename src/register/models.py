from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    job_start_date = models.DateTimeField('Job start date')
    job_finish_date = models.DateTimeField('Job finish date')
    sign = models.ImageField()
    stamp = models.ImageField()


    def __str__(self):
    	return self.name + " " + self.surname