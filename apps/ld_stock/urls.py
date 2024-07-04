from django.urls import path
from .views.StockInOut import StockIndexView,  StockEditView, StockAddView
from .views.StockBarcode import StockBarcodeIndexView, StockBarcodeAddView, StockBarcodeEditView, get_items
app_name = 'ld_stock'
urlpatterns = [
    path('stock/index/', StockIndexView.as_view(), name='stocks'),
    path('stock/add/<int:stock_type>/', StockAddView.as_view(), name='stock_add'),
    path('stock/edit/<bill_id>/', StockEditView.as_view(), name='stock_edit'),
    path('stock/barcode/index/', StockBarcodeIndexView.as_view(), name='barcodes'),
    path('stock/barcode/get_items/', get_items, name='stock_barcode_get_items'),
    path('stock/barcode/add/', StockBarcodeAddView.as_view(), name='stock_barcode_add'),
    path('stock/barcode/edit/<barcode_id>/', StockBarcodeEditView.as_view(), name='stock_barcode_edit'),
]