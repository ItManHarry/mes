from django.urls import path
from . import views
app_name = 'sys_auth'
urlpatterns = [
    path('role/index/', views.role_index, name='role_index'),
    path('role/add/', views.role_add, name='role_add'),
    path('role/edit/<id>', views.role_edit, name='role_edit'),
]