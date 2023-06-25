from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
app_name = 'api'
urlpatterns = [
    path('test', views.test, name='test'),
    path('token/get/', views.get_token, name='get_token'),
    path('token/validate/', views.validate_token, name='validate_token'),
]