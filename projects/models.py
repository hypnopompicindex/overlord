from django.db import models
from people.models import Profile
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from . import fields
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


SHOW_TYPE = (
    ('TRADESHOW', 'Tradeshow'),
    ('MUSEUM', 'Museum'),
    ('EVENT', 'Event'),
    ('RETAIL ENVIRONMENT', 'Retail Environment'),
    ('SOFTWARE ONLY RELEASE', 'Software Only Release'),
)

PAYMENT_TYPE = (
    ('WIRE TRANSFER', 'Wire Transfer'),
    ('PAYPAL', 'PayPal'),
    ('MASTERCARD', 'Mastercard'),
    ('CHEQUE', 'Cheque'),
    ('CASH', 'Cash'),
)


class Client(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)
    contact_name = models.CharField(max_length=200, blank=True, null=True)
    contact_email = models.EmailField(max_length=200, blank=True, null=True)
    contact_phone = models.CharField(max_length=200, blank=True, null=True)
    taylor_client = models.BooleanField(default=False)
    notes = models.TextField(max_length=200, blank=True, null=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TravelDates(models.Model):
    dates = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.dates)


class Project(models.Model):
    PROJECT_STATUS = (
        ('BOOKED', 'Booked'),
        ('BID', 'Bid'),
        ('PROPOSAL', 'Proposal'),
        ('EPWS', 'EPWS'),
        ('CLOSED', 'Closed'),
        ('LOST', 'Lost'),
        ('INTERNAL', 'Internal'),
        ('SUPPORT', 'Support'),
    )
    id = models.AutoField(primary_key=True, verbose_name='Job #')
    name = models.CharField(max_length=200, blank=True, null=True)
    project_status = models.CharField(choices=PROJECT_STATUS, max_length=200)
#    job_number_assignment = models.PositiveIntegerField(null=True, blank=True, verbose_name='Job #')
    product_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='product_owner', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client', blank=True, null=True)
    go_live_date = models.DateField(blank=True, null=True)
    event_start_date = models.DateField(blank=True, null=True)
    billing_date = models.DateField(blank=True, null=True)
    permanent_installation = models.BooleanField(default=False)
    team_selection = models.ManyToManyField(Profile)
    billable = models.BooleanField()
    estimate = models.BooleanField()
    production_budget = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    expenses_budget = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    hardware_purchase = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    hardware_rental = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    testing = models.DateField(blank=True, null=True)
    ship = models.DateField(blank=True, null=True)
    event_load_in = models.DateField(blank=True, null=True)
    dismantle = models.DateField(blank=True, null=True)
#    purchase_order = models.ManyToManyField('PurchaseOrder',
#                                            related_name='project_purchase_order',
#                                            blank=True)
    purchase_order = models.FileField(upload_to='project/purchase_order/%Y/%m/%d', blank=True, null=True)
    estimate_back_up = models.FileField(upload_to='expense_backup/%Y/%m/%d', blank=True, null=True)
    labour = models.DecimalField('Labour (Internal)', null=True, blank=True, decimal_places=2, max_digits=10)
    travel_dates = models.ManyToManyField(TravelDates, related_name='travel_dates_project', blank=True)
    timesheets_closed = models.BooleanField(default=False)
    falls_into_project_year = models.BooleanField(default=False)
    archive_by_year = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def total_budget(self):
        return self.production_budget + self.expenses_budget + self.hardware_purchase + self.hardware_rental

    @property
    def Purchase_order(self):
        if self.purchase_order:
            return mark_safe('<a href="/media/%s" target="_blank">'
                             '<img src="/static/admin/img/icon-yes.svg" alt="True" /></a>'
                             % self.purchase_order)
        else:
            return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="True" />')


class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self):
        return self.name


class Expense(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='expense number')
    person = models.ForeignKey('people.Profile', on_delete=models.CASCADE, related_name='person_expense', blank=True, null=True)
    expense_number_assignment = models.PositiveIntegerField(null=True, blank=True)
    cheque_processed = models.BooleanField()
    backup = models.FileField(upload_to='expense_backup/%Y/%m/%d', blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
#    date = models.DateField(blank=True, null=True)
    cheque_number = models.CharField(max_length=20, blank=True, null=True)
    reference_number = models.CharField(max_length=20, blank=True, null=True)
    by_whom = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.expense_number_assignment)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.expense_receipt.all())


class Receipt(models.Model):
    receipt_number = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_receipt', blank=True, null=True)
    net = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    hst = models.DecimalField('HST', default=0.13, null=True, blank=True, decimal_places=2, max_digits=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_receipt', blank=True, null=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='expense_receipt', blank=True, null=True)

    def __str__(self):
        return 'Receipt Number {0}'.format(self.receipt_number)

    class Meta:
        verbose_name_plural = "Expense Receipts"
        verbose_name = "Expense Receipts"

    @property
    def total(self):
        return round(self.net * (1 + self.hst), 2)

    def get_cost(self):
        return round(self.net * (1 + self.hst), 2)


class PurchaseOrderReceipt(models.Model):
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE, related_name='purchase_order_receipt', blank=True, null=True)
    row_number = models.PositiveIntegerField(null=True, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    hst = models.DecimalField('HST', default=0.13, null=True, blank=True, decimal_places=2, max_digits=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_purchase_order_receipt', blank=True, null=True)

    def __str__(self):
        return str(self.description)

    @property
    def amount(self):
        return round(self.quantity * self.rate * (1 + self.hst), 2)


class Supplier(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)
    contact_name = models.CharField(max_length=200, blank=True, null=True)
    contact_email = models.EmailField(max_length=200, blank=True, null=True)
    contact_phone = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(max_length=200, blank=True, null=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Purchase Order Number')
    requester = models.ForeignKey('people.Profile', on_delete=models.CASCADE, related_name='person_requester', blank=True, null=True)
#    purchase_order_number = models.PositiveIntegerField(null=True, blank=True)
    purchase_order_request_date = models.DateField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_order_supplier', blank=True, null=True)
    supplier_address = models.TextField(blank=True)
    backup = models.FileField(upload_to='purchase_backup/%Y/%m/%d', blank=True, null=True)
    method_of_payment = models.CharField(choices=PAYMENT_TYPE, max_length=200)
    processed = models.BooleanField()
    shipping = models.DecimalField(default=0, null=True, blank=True, decimal_places=2, max_digits=10)
    void = models.BooleanField(default=False)
    cheque_processed = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True, null=True)
    cheque_number = models.PositiveIntegerField(null=True, blank=True)
    by_whom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='by_whom_purchase_order', blank=True, null=True)

    def __str__(self):
        return 'Purchase Order Number {0}'.format(self.id)

    def get_total_cost(self):
        return sum(item.amount() for item in self.purchase_order_receipt.all())
