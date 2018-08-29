from django.urls import path
from . import views
from .views import ProjectMonthArchiveView, ProjectArchiveIndexView, ProjectWIPArchiveView
from .models import Project

app_name = 'project'

urlpatterns = [
    path('admin/expense/<int:expense_id>/', views.admin_expense_detail,
         name='admin_expense_detail'),
    path('admin/purchase/<int:purchaseorder_id>/', views.admin_purchase_detail,
         name='admin_purchase_detail'),
    path('admin/expense/<int:expense_id>/pdf/', views.admin_expense_pdf, name='admin_expense_pdf'),
    path('admin/purchase/<int:purchaseorder_id>/pdf/', views.admin_purchase_pdf, name='admin_purchase_pdf'),
    path('booked/', views.ProjectBookedListView.as_view(), name='booked'),
    path('wip/<int:year>/<str:month>/', ProjectWIPArchiveView.as_view(), name="project_month"),
    path('pipeline/<int:year>/<str:month>/', ProjectMonthArchiveView.as_view(), name="project_month"),
    path('pipeline/', ProjectArchiveIndexView.as_view(), name="pipeline"),
    path('all/', views.ProjectListView.as_view(), name='booked'),
    path('<pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
]