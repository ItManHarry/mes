from django.urls import path
from . import views
app_name = 'org_dep'
urlpatterns = [
    path('department/index/', views.index, name='index'),
    path('department/add/', views.add, name='add'),
    path('department/edit/<id>', views.edit, name='edit'),
    path('department/import/', views.exe_import, name='import'),
]