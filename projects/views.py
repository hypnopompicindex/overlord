from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Expense, PurchaseOrder
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


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