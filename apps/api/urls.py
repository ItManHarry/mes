from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
app_name = 'api'
urlpatterns = [
    path('test', views.test, name='test')
]