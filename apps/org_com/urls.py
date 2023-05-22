from django.urls import path
from . import views
app_name = 'org_com'
urlpatterns = [
    path('company/index/', views.index, name='index'),
    path('company/add/', views.add, name='add'),
    path('company/edit/<id>', views.edit, name='edit'),
    path('company/department/<id>', views.get_departments, name='departments'),
]