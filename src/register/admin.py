from django.contrib import admin

from .models import Person, Department, Organ, Signet, Document, Apostille, ApostilleRequest, DepartmentUser

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

class ApostilleRequestAdmin(admin.ModelAdmin):
	list_display = ('document', 'is_open')

	def get_form(self, request, obj=None, **kwargs):
		if not request.user.is_superuser:
			self.exclude = ('application_date', 'is_open')
			
		form = super(ApostilleRequestAdmin, self).get_form(request, obj, **kwargs)
		return form

	def get_queryset(self, request):
		qs = super(ApostilleRequestAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(user__user=request.user)


class DepartmentUserInline(admin.StackedInline):
	model = DepartmentUser
	can_delete = False
	verbose_name_plural = 'Department User'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
	inlines = (DepartmentUserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Person)
admin.site.register(Department)
admin.site.register(Organ)
admin.site.register(Signet)
admin.site.register(Document)
admin.site.register(Apostille)
admin.site.register(ApostilleRequest, ApostilleRequestAdmin)