from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from mes.sys.decorators import check_menu_used
from django.conf import settings
from django.core.paginator import Paginator
from ..models.ld_stock_barcode import StockBarCode, StockBarCodeList

class StockBarcodeIndexView(View):
    template_name = 'ld_barcode/index.html'
    form_class = None
    @method_decorator(login_required)
    @method_decorator(check_menu_used('LD002'))
    def get(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        all_bars = StockBarCode.objects.filter(facility=facility_id).all()
        paginator = Paginator(all_bars, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(bars=page.object_list, page=page))

class StockBarcodeAddView(View):
    template_name = 'ld_barcode/edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        items = [
            {'name': 'C1', 'code': '001', 'amount': 2},
            {'name': 'C2', 'code': '002', 'amount': 5},
            {'name': 'C3', 'code': '003', 'amount': 3},
            {'name': 'C4', 'code': '004', 'amount': 8},
            {'name': 'C5', 'code': '005', 'amount': 9},
        ]
        return render(request, self.template_name, dict(items=items))
class StockBarcodeEditView(View):
    pass