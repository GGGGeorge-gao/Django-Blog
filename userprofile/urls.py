from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete/<int:id>', views.user_delete, name='delete'),
    path('edit/<int:id>', views.profile_edit, name='edit'),
    path('register/', views.user_register, name='register'),
    path('edit_password/<int:id>', views.edit_password, name='edit_password'),
]

