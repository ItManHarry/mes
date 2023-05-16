from django.urls import path
from . import views
app_name = 'org_com'
urlpatterns = [
    path('company/index/', views.company_index, name='company_index'),
    path('company/add/', views.company_add, name='company_add'),
    path('company/edit/<id>', views.company_edit, name='company_edit'),
]