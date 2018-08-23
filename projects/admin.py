from django.contrib import admin
from .models import Project, Client, Category, Receipt, Expense, Supplier, PurchaseOrder, PurchaseOrderReceipt, TravelDates, User
from django.utils.safestring import mark_safe
from datetime import datetime


def print_expense(obj):
    return mark_safe('<a href="/project/admin/expense/%s" target="_blank">View</a>' % obj.id)


print_expense.short_description = 'Print'


def print_purchase(obj):
    return mark_safe('<a href="/project/admin/purchase/%s">View</a>' % obj.id)


print_purchase.short_description = 'Print'


def expense_pdf(obj):
    return mark_safe('<a href="/project/admin/expense/%s/pdf">PDF</a>' % obj.id)


expense_pdf.short_description = 'PDF'


def purchase_pdf(obj):
    return mark_safe('<a href="/project/admin/purchase/%s/pdf" target="_blank">PDF</a>' % obj.id)


purchase_pdf.short_description = 'PDF'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact_name', 'contact_email', 'taylor_client', 'projects']
    ordering = ['name']
#    readonly_fields = ['projects']
    search_fields = ['name', 'contact_name', 'contact_email']
    list_filter = ['taylor_client']

    def projects(self, obj):
        return ", ".join([k.name for k in obj.client.all()])


class ReceiptInline(admin.TabularInline):
    model = Receipt
    readonly_fields = ['receipt_number', 'total']
    fields = ['receipt_number', 'description', 'category', 'net', 'hst', 'fx', 'total', 'project']
    extra = 0


class PurchaseOrderReceiptInline(admin.TabularInline):
    model = PurchaseOrderReceipt
    readonly_fields = ['amount', 'id']
    fields = ['id', 'description', 'category', 'quantity', 'rate', 'hst', 'amount', 'project']
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['job_number', 'name', 'client', 'total_budget', 'project_status',
                    'estimate', 'Purchase_order', 'project_start', 'billing_date']
    filter_horizontal = ('team_selection',)
    list_filter = ('project_status', 'timesheets_closed', 'billing_date')
    search_fields = ['name', 'product_owner', 'client']
    readonly_fields = ['total_budget', 'id', 'Purchase_order']
    inlines = [ReceiptInline, PurchaseOrderReceiptInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('name', 'job_number', 'client', 'project_status', 'product_owner',
                       'timesheets_closed', 'falls_into_project_year',
                       'archive_by_year', 'purchase_order', 'purchase_order_number',
                       'estimate', 'estimate_back_up',)
        }),
        ('Financials', {
            'fields': ('internal', 'production_budget', 'expenses_budget',
                       'hardware_purchase', 'hardware_rental', 'total_budget')
        }),
        ('Key Dates', {
            'fields': ('project_start', 'billing_date',
                       'testing', 'ship', 'event_load_in', 'go_live_date', 'dismantle',
                       'travel_dates')
        }),
        ('Team Members', {
            'fields': ('team_selection',)
        }),
        ('Warranty & Support', {
            'fields': ('permanent_installation',)
        }),
    )

#    def save_model(self, request, obj, form, change):
#        if obj.job_number == 0:
#            obj.job_number = obj.id + 1300
#        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product_owner':
            kwargs["queryset"] = User.objects.filter(groups__name='Product Owner')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'person', 'cheque_processed', 'backup', print_expense]
    inlines = [ReceiptInline]
    list_filter = ['person', 'cheque_processed', 'date']
    search_fields = ['person']
    readonly_fields = ['id', 'date', 'by_whom']
    fields = ['id', 'person',
              'backup', 'cheque_number', 'reference_number',
              'cheque_processed', 'date', 'by_whom']

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = ['id', 'person', 'expense_number_assignment',
                           'backup', 'cheque_number', 'reference_number', 'cheque_processed',
                           'date', 'by_whom']
        else:
            self.fields = ['id', 'person', 'expense_number_assignment',
                           'backup', 'cheque_number', 'reference_number', 'cheque_processed',
                           'date', 'by_whom']
        form = super(ExpenseAdmin,self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        if obj.cheque_processed and 'cheque_processed' in form.changed_data:
            obj.date = datetime.now()
            if getattr(obj, 'by_whom', None) is None:
                obj.by_whom = request.user
        obj.save()


class PurchaseOrderSupplierInline(admin.TabularInline):
    model = PurchaseOrder
    fields = ['id', 'requester', 'processed', 'backup', 'date', 'by_whom']
    extra = 0


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_name', 'contact_email', 'contact_phone']
    inlines = [PurchaseOrderSupplierInline, ]
    search_fields = ['name', 'contact_name', 'contact_email', 'contact_phone']
    ordering = ['name']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'requester', 'backup',
                    'purchase_order_request_date', print_purchase]
    fields = ['requester', 'id',
              'purchase_order_request_date', 'supplier',
              'backup', 'method_of_payment', 'shipping',
              'cheque_number', 'processed', 'date', 'by_whom']
    inlines = [PurchaseOrderReceiptInline]
    list_filter = ['requester', 'supplier', 'processed']
    search_fields = ['requester', 'supplier', ]
    readonly_fields = ['id', 'date', 'by_whom']

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = ['id', 'requester',
                           'purchase_order_request_date', 'supplier',
                           'backup', 'method_of_payment', 'shipping',
                           'cheque_number', 'processed', 'date', 'by_whom']
        else:
            self.fields = ['requester', 'id',
                           'purchase_order_request_date', 'supplier',
                           'backup', 'method_of_payment', 'shipping',
                           'cheque_number', 'processed', 'date', 'by_whom']
        form = super(PurchaseOrderAdmin,self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        if obj.cheque_processed and 'processed' in form.changed_data:
            obj.date = datetime.now()
            if getattr(obj, 'by_whom', None) is None:
                obj.by_whom = request.user
        obj.save()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(TravelDates)
class TravelDatesAdmin(admin.ModelAdmin):
    list_display = ['dates']
