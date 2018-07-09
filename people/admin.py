from django.contrib import admin
from .models import Profile, OutOfOffice
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class UserProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False


class OutOfOfficeInline(admin.StackedInline):
    model = OutOfOffice
    extra = 0
    fields = ['start_date', 'end_date', 'person', 'leave_type', 'project', 'notes', 'approved']


class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline, OutOfOfficeInline]

    fieldsets = (
        ('Personal Info',{
            'fields': ('username', 'password', 'first_name', 'last_name', 'email',)
        }),

        ('Permissions',{
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'avatar']


@admin.register(OutOfOffice)
class OutOfOfficeAdmin(admin.ModelAdmin):
    readonly_fields = ['number_of_days']
    list_display = ['start_date', 'end_date', 'number_of_days', 'person', 'leave_type',  'approved', 'number_of_days', 'project',]
    fields = ['start_date', 'end_date', 'number_of_days', 'person', 'leave_type', 'project', 'notes', 'approved']
