from django.urls import path
from .views import ProductLineIndexView, ProductLineAddView, ProductLineEditView
app_name = 'pp_master'
urlpatterns = [
    path('lines/', ProductLineIndexView.as_view(), name='lines'),
    path('line/add/', ProductLineAddView.as_view(), name='line_add'),
]