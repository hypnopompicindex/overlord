from django.urls import path
from . import views

urlpatterns = [
    path('admin/expense/<int:expense_id>/', views.admin_expense_detail,
         name='admin_expense_detail'),
    path('admin/purchase/<int:purchaseorder_id>/', views.admin_purchase_detail,
         name='admin_purchase_detail'),
    path('admin/expense/<int:expense_id>/pdf/', views.admin_expense_pdf, name='admin_expense_pdf'),
    path('admin/purchase/<int:purchaseorder_id>/pdf/', views.admin_purchase_pdf, name='admin_purchase_pdf'),
]