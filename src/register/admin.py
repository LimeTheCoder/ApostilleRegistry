from django.contrib import admin

from .models import Person, Department, Organ, Signet, Document, Apostille, ApostilleRequest, DepartmentUser

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.


class ApostilleRequestAdmin(admin.ModelAdmin):
	list_display = ('document', 'status')

	def get_readonly_fields(self, request, obj=None):
		if obj and not request.user.is_superuser:
			return self.readonly_fields + tuple(['document', 'payment_file', 'user'])
		return self.readonly_fields

	def get_form(self, request, obj=None, **kwargs):
		self.fields = ('document', 'payment_file', 'application_date', 'status', 'user')
		form = super(ApostilleRequestAdmin, self).get_form(request, obj, **kwargs)

		#form.base_fields['user'].initial = DepartmentUser.objects.get(user = request.user)

		if not request.user.is_superuser:
			self.fields = ('document', 'payment_file', 'user')
			
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