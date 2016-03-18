from django.contrib import admin

from .models import Person, Department, Organ, Signet, Document, Apostille, ApostilleRequest

# Register your models here.

admin.site.register(Person)
admin.site.register(Department)
admin.site.register(Organ)
admin.site.register(Signet)
admin.site.register(Document)
admin.site.register(Apostille)
admin.site.register(ApostilleRequest)