from django.urls import path
from . import views
app_name = 'sys_auth'
urlpatterns = [
    path('role/index/', views.role_index, name='role_index'),
    path('role/add/', views.role_add, name='role_add'),
    path('role/edit/<id>', views.role_edit, name='role_edit'),
    path('role/menus/<id>', views.get_role_menus, name='get_role_menus'),
    path('role/auth/<id>', views.auth_role_menus, name='auth_role_menus'),
    path('menu/index/', views.menu_index, name='menu_index'),
    path('menu/add/', views.menu_add, name='menu_add'),
    path('menu/edit/<id>', views.menu_edit, name='menu_edit'),
    path('user/index/', views.user_index, name='user_index'),
    path('user/add/', views.user_add, name='user_add'),
    path('user/edit/<int:id>', views.user_edit, name='user_edit'),
]