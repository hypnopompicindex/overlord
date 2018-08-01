from django.contrib import admin
from .models import Profile, OutOfOffice, TimeSheet, TimeSheetWeek, Hours
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from projects.models import Project


@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ['person', 'project', 'week', 'end_of_week', 'hours', 'approved']
    search_fields = ['person', 'project', 'week', 'monday']
    readonly_fields = ['hours', 'end_of_week']
    list_filter = ('person', 'project', 'week')
    fields = ['project', 'week', 'end_of_week', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'hours', 'approved', 'changes_required']

    class Media:
        js = ('people/js/weekPicker.js',)

    def save_model(self, request, obj, form, change):
        obj.person = request.user
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(TimeSheetAdmin, self).get_queryset(request)
        else:
            qs = super(TimeSheetAdmin, self).get_queryset(request)
            return qs.filter(person=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'project':
            kwargs["queryset"] = Project.objects.filter(timesheets_closed=False, team_selection__exact=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = ['project', 'week', 'end_of_week', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'hours', 'approved', 'changes_required']
        else:
            self.fields = ['project', 'week', 'end_of_week', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'hours']
        form = super(TimeSheetAdmin,self).get_form(request, obj, **kwargs)
        return form


class TimeSheetInline(admin.StackedInline):
    model = TimeSheet
    extra = 0
    readonly_fields = ['hours']
    search_fields = ['project', 'week']


class UserProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False


class OutOfOfficeInline(admin.StackedInline):
    model = OutOfOffice
    extra = 0
    fields = ['start_date', 'end_date', 'person', 'leave_type', 'project', 'notes', 'approved']


class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']

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
    list_display = ['user', 'date_of_birth']


@admin.register(OutOfOffice)
class OutOfOfficeAdmin(admin.ModelAdmin):
    readonly_fields = ['number_of_days']
    list_display = ['person', 'start_date', 'end_date', 'number_of_days',  'leave_type', 'project', 'approved']
    fields = ['start_date', 'end_date', 'number_of_days', 'person', 'leave_type', 'project', 'notes', 'approved', 'time_approved']
    list_filter = ('person', 'start_date', 'leave_type', 'project')
    search_fields = ['person', 'project']

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = ['start_date', 'end_date', 'number_of_days', 'person', 'leave_type', 'project', 'notes', 'approved', 'time_approved']
        else:
            self.fields = ['start_date', 'end_date', 'number_of_days', 'person', 'leave_type', 'project', 'notes']
        form = super(OutOfOfficeAdmin,self).get_form(request, obj, **kwargs)
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(OutOfOfficeAdmin, self).get_queryset(request)
        else:
            qs = super(OutOfOfficeAdmin, self).get_queryset(request)
            return qs.filter(person=request.user)


class HoursInline(admin.TabularInline):
    model = Hours
    extra = 0
    readonly_fields = ['hours']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'project':
            kwargs["queryset"] = Project.objects.filter(timesheets_closed=False, team_selection__exact=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TimeSheetWeek)
class TimeSheetWeekAdmin(admin.ModelAdmin):
    readonly_fields = ['end_of_week']
    list_display = ['week', 'end_of_week', 'person', 'approved', 'changes_required']
    search_fields = ['week', 'end_of_week', 'person']
    list_filter = ['person', 'week', 'approved']
    inlines = [HoursInline]
    fields = ['person', 'week', 'end_of_week', 'approved', 'changes_required']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person':
            kwargs["queryset"] = User.objects.filter(username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)