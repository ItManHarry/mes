from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from mes.sys.decorators import check_menu_used
from django.conf import settings
from django.core.paginator import Paginator
from ..models.ld_stock_barcode import StockBarCode, StockBarCodeList
from django.http import HttpResponse
from pp_master.models.pp_component import Component
import random
import json
def get_items(request):
    print('Get items ...')
    items = json.loads(request.POST.get('items'))
    print(type(items), items)
    return HttpResponse('<h1>OK</h1>')
class StockBarcodeIndexView(View):
    template_name = 'ld_barcode/index.html'
    form_class = None
    @method_decorator(login_required)
    @method_decorator(check_menu_used('LD002'))
    def get(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        all_bars = StockBarCode.objects.filter(facility=facility_id).all().order_by('code')
        paginator = Paginator(all_bars, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(bars=page.object_list, page=page))

class StockBarcodeAddView(View):
    template_name = 'ld_barcode/edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # items = [{'name': 'C'+str(i), 'code': '00'+str(i), 'amount': random.randint(1, 20)} for i in range(100)]
        components = Component.objects.all().order_by('code')
        return render(request, self.template_name, dict(components=components))
class StockBarcodeEditView(View):
    pass