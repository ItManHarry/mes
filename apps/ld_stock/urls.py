from django.urls import path
from .views.ld_stock_in_out import StockIndexView,  StockEditView, StockAddView, get_io_select_items
from .views.ld_stock_bar_code import StockBarcodeIndexView, barcode_add, barcode_edit, get_items, execute_save_barcode, \
    barcode_item_remove
app_name = 'ld_stock'
urlpatterns = [
    path('stock/index/', StockIndexView.as_view(), name='stocks'),
    path('stock/add/<int:stock_type>/', StockAddView.as_view(), name='stock_add'),
    path('stock/edit/<bill_id>/', StockEditView.as_view(), name='stock_edit'),
    path('stock/barcode/index/', StockBarcodeIndexView.as_view(), name='barcodes'),
    path('stock/barcode/add/', barcode_add, name='stock_barcode_add'),
    path('stock/barcode/save/execute/', execute_save_barcode, name='execute_add_barcode'),
    path('stock/barcode/edit/<barcode_id>/', barcode_edit, name='stock_barcode_edit'),
    path('stock/barcode/get_items/', get_items, name='stock_barcode_get_items'),
    path('stock/barcode/items/remove/<item_id>', barcode_item_remove, name='barcode_item_remove'),
    path('stock/io/get_io_select_items/<int:stock_type>/', get_io_select_items, name='stock_io_get_items'),
]