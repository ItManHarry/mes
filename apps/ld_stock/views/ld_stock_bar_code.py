from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from mes.sys.decorators import check_menu_used
from django.conf import settings
from django.core.paginator import Paginator
from ..models.ld_stock_barcode import StockBarCode, StockBarCodeList
from django.http import JsonResponse
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
        all_bars = StockBarCode.objects.filter(facility=facility_id).all().order_by('-created_on')
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
    search_str = params.get('search_str')
    page_num = int(params.get('page'))
    if search_str:
        components = Component.objects.filter(Q(facility=facility_id) & (Q(code__icontains=search_str) | Q(name__icontains=search_str))).order_by('name')
    else:
        components = Component.objects.filter(facility=facility_id).order_by('code')
    paginator = Paginator(components, settings.PAGE_ITEMS)
    page = paginator.page(page_num)
    return render(request, 'ld_barcode/_components.html', dict(components=page.object_list, page=page))
@login_required
def execute_save_barcode(request):
    user = request.user
    facility_id = request.session['company_id']
    barcode_val = request.POST.get('barcode')
    components = json.loads(request.POST.get('components'))
    if barcode_val:     # 编辑
        barcode = StockBarCode.objects.filter(code=barcode_val).first()
        if user:
            barcode.updated_by = user.id
        barcode.updated_on = timezone.now()
        barcode.save()
        for component in components:
            barcode_item = StockBarCodeList.objects.filter(Q(barcode=barcode) & Q(component_id=component.get('id'))).first()
            if barcode_item:
                barcode_item.amount = int(component.get('amount'))
                if user:
                    barcode_item.updated_by = user.id
                barcode_item.updated_on = timezone.now()
                barcode_item.save()
            else:
                barcode_item = StockBarCodeList(barcode=barcode, component_id=component.get('id'), amount=int(component.get('amount')))
                if user:
                    barcode_item.created_by = user.id
                barcode_item.save()
    else:       # 新增
        barcode = StockBarCode(code='BC'+datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(10, 99)), facility_id=facility_id)
        if user:
            barcode.created_by = user.id
        barcode.save()
        for component in components:
            barcode_item = StockBarCodeList(barcode=barcode, component_id=component.get('id'), amount=int(component.get('amount')))
            if user:
                barcode_item.created_by = user.id
            barcode_item.save()
    return JsonResponse({
        'code': 1,
        'message': 'Add successfully!'
    })
@login_required
def barcode_edit(request, barcode_id):
    barcode = StockBarCode.objects.get(pk=barcode_id)
    return render(request, 'ld_barcode/edit.html', dict(barcode=barcode, items=barcode.items.filter(active=True).all()))
@login_required
def barcode_item_remove(request, item_id):
    item = StockBarCodeList.objects.get(pk=item_id)
    item.active = False
    user = request.user
    if user:
        item.updated_by = user.id
    item.updated_on = timezone.now()
    item.save()
    return JsonResponse({'code': 1, 'message': 'Barcode item remove successfully.'})