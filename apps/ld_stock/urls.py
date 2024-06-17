from django.urls import path
from .views.StockInOut import StockIndexView,  StockEditView, StockAddView
app_name = 'ld_stock'
urlpatterns = [
    path('stock/index/', StockIndexView.as_view(), name='stocks'),
    path('stock/add/', StockAddView.as_view(), name='stock_add'),
    path('stock/edit/<bill_id>/', StockEditView.as_view(), name='stock_edit'),
]