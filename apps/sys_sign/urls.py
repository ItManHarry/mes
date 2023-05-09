from django.urls import path
from . import views
app_name = 'sys_sign'
urlpatterns = [
    path('login/', views.do_login, name='login'),
    path('logout/', views.do_logout, name='logout'),
    path('json/', views.json_req, name='json'),
]