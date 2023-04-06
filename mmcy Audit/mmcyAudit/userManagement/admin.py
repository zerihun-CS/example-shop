from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Employee,Account,UserRole,Position


@admin.register(Position)
class EmployeeAdmin(ImportExportModelAdmin):
    pass

 
@admin.register(Employee)
class PersonAdmin(ImportExportModelAdmin):
    pass

class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login',
	                 'is_auditee', 'is_auditor', 'is_manager', 'is_other')
	search_fields = ('email','username',)
	icon_name = 'account_circle'
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()



admin.site.register(Account, AccountAdmin)


# @admin.register(Account)
# class PersonAdmin(ImportExportModelAdmin):
#     pass

@admin.register(UserRole)
class PersonAdmin(ImportExportModelAdmin):
    pass