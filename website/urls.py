# This code snippet is from a Django project's urls.py file. It defines URL patterns for different
# views in the application. Here's a breakdown of what each part does:
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("super-admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("delete-feedback/<int:id>/", views.delete_feedback, name="delete_feedback"),
    path("edit-feedback/<int:id>/", views.edit_feedback, name="edit_feedback"),
    path("change-password/", views.change_password, name="change_password"),
    path("submit-feedback/", views.submit_feedback, name="submit_feedback"),
]