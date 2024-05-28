from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "drivesafe"
urlpatterns = [
    path("", views.home, name="index"),
    path('login_view/', views.login_view, name='login'),
    path('accounts/', include('allauth.urls')),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('regular_user_home/', views.regular_user, name='regular_user_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('user_report/', views.report, name='report'),
    path('form_submitted/', views.form_submitted, name='form_submitted'),
    path('submissions/', views.view_submissions, name='submissions'),
    path('user_submissions/', views.view_user_submissions, name='user_submissions'),
    path('anonymous_report/', views.anonymous_report, name='anonymous_report'),
    path('update_status/<int:submission_id>/', views.update_status, name='update_status'),
    path('update_response/<int:submission_id>/', views.update_response, name='update_response'),
    path('common_words/', views.common_words, name='common_words'),
    path('submission/<int:submission_id>/delete/', views.delete_submission, name='delete_submission'),
    path('update_status_and_response/<int:submission_id>/', views.update_status_and_response, name='update_status_and_response'),
    path('anon_form_submitted/', views.anon_form_submitted, name='anon_form_submitted')
]
