from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import django.utils
from django.conf import settings

# Create your models here.

STATUS_CHOICES  =(('p', 'Pending'), ('a', 'Approved'), ('r', 'Rejected'))

class Organ(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=75)

    def __str__(self):
        return self.name.encode('utf8')


class Department(models.Model):
    code = models.IntegerField(primary_key=True)
    organ = models.OneToOneField(Organ, on_delete=models.CASCADE)
    icon = models.ImageField(default=(settings.MEDIA_URL + '/apostille.jpg'))
    def __str__(self):
        return self.organ.name.encode('utf8')


class Signet(models.Model):
    sign = models.ImageField(null=True, blank=True)
    stamp = models.ImageField(null=True, blank=True)

    def __str__(self):
        return ('Signet #' + str(self.id)).encode('utf8')


class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    job_start_date = models.DateField('Job start date')
    job_finish_date = models.DateField('Job finish date', null=True, blank=True)
    position = models.CharField(max_length=75)
    signet = models.OneToOneField(Signet, on_delete=models.CASCADE)
    organ = models.ForeignKey(Organ, on_delete=models.CASCADE)

    def __str__(self):
        return (self.name + " " + self.surname).encode('utf8')


class Document(models.Model):
    name = models.CharField(max_length=100)
    issue_date = models.DateField('Issue Date')
    file = models.FileField()
    signer_name = models.CharField(max_length=50)
    signer_surname = models.CharField(max_length=50)
    signer_patronymic = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name.encode('utf8')


class Apostille(models.Model):
    placing_date = models.DateField('Placing date')
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    validator = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.document.name.encode('utf8')


class DepartmentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username.encode('utf8')


class ApostilleRequest(models.Model):
    application_date = models.DateTimeField('Application Date', default=django.utils.timezone.now)
    payment_file = models.FileField()
    status = models.CharField(max_length=1, default='p', choices=STATUS_CHOICES)
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(DepartmentUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.document.name.encode('utf8')