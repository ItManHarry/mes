from django.urls import path
from .views import ProductLineIndexView
app_name = 'pp_master'
urlpatterns = [
    path('lines/', ProductLineIndexView.as_view(), name='lines'),
]