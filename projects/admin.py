from django.contrib import admin
from .models import Project, Client, Category, Receipt, Expense, Supplier, PurchaseOrder, PurchaseOrderReceipt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'sub_customer_of', 'address', 'contact_name', 'contact_email']
    ordering = ['name']
    search_fields = ['name', 'sub_customer_of', 'contact_name', 'contact_email']


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
    list_display = ['name', 'project_status']
    filter_horizontal = ('team_selection',)
    list_filter = ('project_status',)
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
            'fields': ('estimate', 'expenses_budget', 'hardware_budget', 'total_budget')
        }),
        ('Bid', {
            'fields': ('testing', 'ship', 'event_load_in', 'dismantle')
        }),
        ('Booked', {
            'fields': ('purchase_order', 'labour')
        }),
        ('Closed', {
            'fields': ('timesheets_closed', 'falls_into_project_year', 'archive_by_year')
        }),

    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number_assignment', 'person', 'processed', 'backup', ]
    inlines = [ReceiptInline]


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
    list_display = ['purchase_order_number', 'supplier', 'requester', 'processed', 'backup', 'purchase_order_request_date']
    fields = ['requester', 'purchase_order_number', 'purchase_order_request_date', 'supplier', 'supplier_address', 'backup', 'method_of_payment', 'processed', 'shipping', 'void', 'cheque_processed', 'date', 'cheque_number', 'by_whom']
    inlines = [PurchaseOrderReceiptInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
