from django.contrib import admin

from .models import Person, Department, Organ, Signet, Document, Apostille, ApostilleRequest, DepartmentUser

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from django.conf import settings
import django.utils

# Register your models here.

admin.site.disable_action('delete_selected')
admin.site.site_header = settings.ADMIN_SITE_HEADER


class ApostilleRequestAdmin(admin.ModelAdmin):
	list_display = ('document', 'status')
	search_fields = ['document__name', 'user__user__username']

	def get_readonly_fields(self, request, obj=None):
		if obj and not request.user.is_superuser:
			return self.readonly_fields + tuple(['document', 'payment_file'])
		return self.readonly_fields

	def get_form(self, request, obj=None, **kwargs):
		self.fields = ('document', 'payment_file', 'application_date', 'status', 'user')
		form = super(ApostilleRequestAdmin, self).get_form(request, obj, **kwargs)

		if not request.user.is_superuser:
			self.fields = ('document', 'payment_file')
			
		return form

	def get_queryset(self, request):
		qs = super(ApostilleRequestAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(user__user=request.user)

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:
			obj.user = DepartmentUser.objects.get(user=request.user)
			obj.status = 'p'
			obj.application_date = django.utils.timezone.now()

		obj.save()


class ApostilleAdmin(admin.ModelAdmin):
	search_fields = ['request__document__name', 'validator__name', 'validator__surname']
	list_display = ('get_name', 'validator', 'id')

	def get_name(self, obj):
		return obj.request

	def get_readonly_fields(self, request, obj=None):
		if obj and not request.user.is_superuser:
			return self.readonly_fields + tuple(['placing_date', 'request', 'validator'])
		return self.readonly_fields


	def get_queryset(self, request):
		qs = super(ApostilleAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(request__user__user=request.user)

	get_name.short_description = 'Document'
	get_name.admin_order_field = 'request__document__name'


class DocumentAdmin(admin.ModelAdmin):
	search_fields = ['name', 'signer_name', 'signer_surname']


class PersonAdmin(admin.ModelAdmin):
	search_fields = ['name', 'surname', 'position']


class OrganAdmin(admin.ModelAdmin):
	search_fields = ['name', 'location']


class DepartmentAdmin(admin.ModelAdmin):
	search_fields = ['organ__name', 'organ__location']


class DepartmentUserInline(admin.StackedInline):
	model = DepartmentUser
	can_delete = False
	verbose_name_plural = 'Department User'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
	inlines = (DepartmentUserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Organ, OrganAdmin)
admin.site.register(Signet)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Apostille, ApostilleAdmin)
admin.site.register(ApostilleRequest, ApostilleRequestAdmin)