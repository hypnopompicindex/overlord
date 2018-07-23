from django.urls import path, re_path
from django.contrib.auth.views import *
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),

    # login / logout urls
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),

    # change password urls
    path('password-change/', password_change, name='password_change'),
    path('password-change/done/', password_change_done, name='password_change_done'),

    # restore password urls
    path('password-reset/', password_reset, name='password_reset'),
    path('password-reset/done/', password_reset_done, name='password_reset_done'),
    re_path('password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/',
         password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/complete/', password_reset_complete, name='password_reset_complete'),
    path('timesheet/create/', views.TimeSheetCreate.as_view(), name='people_create'),
    path('timesheet/<pk>/', views.TimeSheetUpdate.as_view(), name='timesheet-update'),
    path('timesheet/', views.TimeSheetListView.as_view(), name='timesheets'),
    path('user/', views.UserList.as_view(), name='user-list'),
    path('user/add/', views.UserTimeSheetCreate.as_view(), name='user-add'),
    path('user/<pk>/', views.UserTimeSheetUpdate.as_view(), name='user-update'),
    path('user/<pk>/delete/', views.UserDelete.as_view(), name='user-delete'),
]
