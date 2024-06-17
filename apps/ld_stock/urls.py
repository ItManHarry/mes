from django.urls import path
from .views.StockInOut import StockInIndexView, StockOutIndexView, StockOutEditView, StockOutAddView, StockInEditView, StockInAddView
app_name = 'ld_stock'
urlpatterns = [
    path('in_out/index/', StockInIndexView.as_view(),name='in_outs')
]