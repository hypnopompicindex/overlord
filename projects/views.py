from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView
import weasyprint
from .models import Expense, PurchaseOrder, Project


@staff_member_required
def admin_expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    return render(request,
                  'admin/expenses/expense/detail.html',
                  {'expense': expense})


@staff_member_required
def admin_purchase_detail(request, purchaseorder_id):
    purchase = get_object_or_404(PurchaseOrder, id=purchaseorder_id)
    return render(request,
                  'admin/purchases/purchase/detail.html',
                  {'purchase': purchase})


@staff_member_required
def admin_expense_pdf(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    html = render_to_string('admin/expenses/expense/pdf.html',
                            {'expense': expense})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(expense.id)
    weasyprint.HTML(string=html).write_pdf(response,)
    return response


@staff_member_required
def admin_purchase_pdf(request, purchaseorder_id):
    purchase = get_object_or_404(PurchaseOrder, id=purchaseorder_id)
    html = render_to_string('admin/purchases/purchase/pdf.html',
                            {'purchase': purchase})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(purchaseorder_id)
    weasyprint.HTML(string=html).write_pdf(response,)
    return response


class ProjectBookedListView(ListView):
    model = Project
    queryset = Project.objects.filter(project_status='Booked')
    template_name = 'projects/booked_list.html'


class ProjectMonthArchiveView(MonthArchiveView):
    queryset = Project.objects.exclude(project_status='Closed')
    date_field = "billing_date"
    allow_future = True
    ordering = ['billing_date']
    allow_empty = True

    def get_month(self):
        try:
            month = super(ProjectMonthArchiveView, self).get_month()
        except Http404:
            month = now().strftime(self.get_month_format())

        return month

    def get_year(self):
        try:
            year = super(ProjectMonthArchiveView, self).get_year()
        except Http404:
            year = now().strftime(self.get_year_format())

        return year


class ProjectArchiveIndexView(ArchiveIndexView):
    queryset = Project.objects.exclude(project_status='Closed')
    date_field = "billing_date"
    allow_future = True
    ordering = ['billing_date']
    date_list_period = 'month'
