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
from django.db.models import Q
import random
import json
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
@login_required
def barcode_add(request):
    return render(request, 'ld_barcode/edit.html')
@login_required
def get_items(request):
    facility_id = request.session['company_id']
    params = json.loads(request.POST.get('params'))
    print(type(params), params)
    search_str = params.get('search_str')
    page_num = int(params.get('page'))
    if search_str:
        components = Component.objects.filter(Q(facility=facility_id) & (Q(code__icontains=search_str) | Q(name__icontains=search_str))).order_by('code')
    else:
        components = Component.objects.filter(facility=facility_id).order_by('code')
    paginator = Paginator(components, settings.PAGE_ITEMS)
    page = paginator.page(page_num)
    return render(request, 'ld_barcode/_components.html', dict(components=page.object_list, page=page))
class StockBarcodeEditView(View):
    pass