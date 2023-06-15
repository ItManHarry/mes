from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from . import views
app_name = 'org_emp'
urlpatterns = [
    path('employee/index/', views.index, name='index'),
    path('employee/add/', views.add, name='add'),
    path('employee/edit/<id>', views.edit, name='edit'),
    path('employee/search/', views.search_employee, name='search'),
    # https://blog.csdn.net/xingxingmingyue/article/details/89678916
    re_path(r'^(?P<path>.*)$', serve, {'document_root': settings.UPLOAD_FILE_PATH}),
]