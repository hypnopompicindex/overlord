from django.contrib import admin
from .models import Project, Client, Category, Receipt, Expense, Supplier, PurchaseOrder, PurchaseOrderReceipt, TravelDates
from django.utils.safestring import mark_safe


def print_expense(obj):
    return mark_safe('<a href="/project/admin/expense/%s">View</a>' % obj.id)


print_expense.short_description = 'Print'


def print_purchase(obj):
    return mark_safe('<a href="/project/admin/purchase/%s">View</a>' % obj.id)


print_purchase.short_description = 'Print'


def expense_pdf(obj):
    return mark_safe('<a href="/project/admin/expense/%s/pdf">PDF</a>' % obj.id)


expense_pdf.short_description = 'PDF'


def purchase_pdf(obj):
    return mark_safe('<a href="/project/admin/purchase/%s/pdf">PDF</a>' % obj.id)


purchase_pdf.short_description = 'PDF'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'sub_customer_of', 'address', 'contact_name', 'contact_email']
    ordering = ['name']
    search_fields = ['name', 'sub_customer_of', 'contact_name', 'contact_email']
    list_filter = ['sub_customer_of']


class ReceiptInline(admin.TabularInline):
    model = Receipt
    readonly_fields = ['receipt_number', 'total']
    fields = ['receipt_number', 'description', 'category', 'net', 'hst', 'total', 'project']
    extra = 0


class PurchaseOrderReceiptInline(admin.TabularInline):
    model = PurchaseOrderReceipt
    readonly_fields = ['amount']
    fields = ['row_number', 'description', 'quantity', 'rate', 'hst', 'amount', 'project']
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['job_number_assignment', 'name', 'client', 'total_budget', 'project_status', 'estimate', 'purchase_order', 'event_start_date', 'event_end_date']
    filter_horizontal = ('team_selection',)
    list_filter = ('project_status', 'timesheets_closed', 'event_end_date')
    search_fields = ['name', 'product_owner', 'client']
    readonly_fields = ['total_budget']
    inlines = [ReceiptInline, PurchaseOrderReceiptInline]
    fieldsets = (
        ('General',{
            'fields': ('name', 'project_status', 'product_owner', 'client')
        }),
        ('EPWS',{
            'fields': ('job_number_assignment', 'event_start_date', 'event_end_date', 'team_selection', 'billable')
        }),
        ('Proposal', {
            'fields': ('estimate', 'production_budget', 'expenses_budget', 'hardware_budget', 'total_budget')
        }),
        ('Bid', {
            'fields': ('testing', 'ship', 'event_load_in', 'production_date', 'dismantle')
        }),
        ('Booked', {
            'fields': ('purchase_order', 'labour', 'travel_dates')
        }),
        ('Closed', {
            'fields': ('timesheets_closed', 'falls_into_project_year', 'archive_by_year')
        }),

    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number_assignment', 'person', 'processed', 'backup', print_expense, expense_pdf]
    inlines = [ReceiptInline]
    list_filter = ['person', 'processed', 'cheque_processed']
    search_fields = ['person']
    fields = ['person', 'expense_number_assignment', 'processed', 'backup',
              'cheque_processed', 'date', 'cheque_number', 'by_whom']

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = ['person', 'expense_number_assignment', 'processed', 'backup',
              'cheque_processed', 'date', 'cheque_number', 'by_whom', ]
        else:
            self.fields = ['person', 'expense_number_assignment', 'processed', 'backup']
        form = super(ExpenseAdmin,self).get_form(request, obj, **kwargs)
        return form


class PurchaseOrderSupplierInline(admin.TabularInline):
    model = PurchaseOrder
    fields = ['purchase_order_number', 'requester', 'processed', 'backup', 'date', 'by_whom']
    extra = 0


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_name', 'contact_email', 'contact_phone']
    inlines = [PurchaseOrderSupplierInline, ]
    search_fields = ['name', 'contact_name', 'contact_email', 'contact_phone']
    ordering = ['name']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['purchase_order_number', 'supplier', 'requester', 'processed', 'backup',
                    'purchase_order_request_date', print_purchase, purchase_pdf]
    fields = ['requester', 'purchase_order_number', 'purchase_order_request_date',
              'supplier', 'supplier_address', 'backup', 'method_of_payment', 'processed',
              'shipping', 'void', 'cheque_processed', 'date', 'cheque_number', 'by_whom']
    inlines = [PurchaseOrderReceiptInline]
    list_filter = ['requester', 'supplier', 'processed']
    search_fields = ['requester', 'supplier', ]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = ['requester', 'purchase_order_number', 'purchase_order_request_date',
              'supplier', 'supplier_address', 'backup', 'method_of_payment', 'processed',
              'shipping', 'void', 'cheque_processed', 'date', 'cheque_number', 'by_whom']
        else:
            self.fields = ['requester', 'purchase_order_number', 'purchase_order_request_date',
              'supplier', 'supplier_address', 'backup', 'method_of_payment', 'processed',
              'shipping', 'void']
        form = super(PurchaseOrderAdmin,self).get_form(request, obj, **kwargs)
        return form


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(TravelDates)
class TravelDatesAdmin(admin.ModelAdmin):
    list_display = ['dates']