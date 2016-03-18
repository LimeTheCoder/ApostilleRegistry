from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Organ(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=75)

    def __str__(self):
        return self.name.encode('utf8')


class Department(models.Model):
    code = models.IntegerField(primary_key=True)
    organ = models.OneToOneField(Organ, on_delete=models.CASCADE)

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
    signer = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.encode('utf8')


class Apostille(models.Model):
    placing_date = models.DateField('Placing date')
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    validator = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.document.name.encode('utf8')


class ApostilleRequest(models.Model):
    applicant_name = models.CharField(max_length=150)
    receiving_date = models.DateTimeField('Receiving Date')
    payment_file = models.FileField()
    is_open = models.BooleanField()
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.document.name.encode('utf8')
