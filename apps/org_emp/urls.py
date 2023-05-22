from django.urls import path
from . import views
app_name = 'org_emp'
urlpatterns = [
    path('employee/index/', views.index, name='index'),
    path('employee/add/', views.add, name='add'),
    path('employee/edit/<id>', views.edit, name='edit'),
]