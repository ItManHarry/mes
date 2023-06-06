from django.urls import path
from . import views
app_name = 'sys_dict'
urlpatterns = [
    path('dict/index/', views.dict_index, name='dict_index'),
    path('dict/add/', views.dict_add, name='dict_add'),
    path('dict/edit/<id>', views.dict_edit, name='dict_edit'),
    path('enum/add/<dict_id>', views.enum_add, name='enum_add'),
    path('enum/edit/<dict_id>/<enum_id>', views.enum_edit, name='enum_edit'),
]