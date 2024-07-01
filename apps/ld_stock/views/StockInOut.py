from django.views import View
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from mes.sys.decorators import check_menu_used
from ..models import StockBill, StockItems
from sys_dict.models import SysEnum
from django.db.models import Q
from ..forms.stock import StockForm
from pp_master.models.pp_component import Component, ComponentAmount

def get_items(request, stock_type):
    if stock_type == 1:     # 入库
        pass
    else:                   # 出库
        pass
    items = [
        {'name': 'C1', 'code': '001', 'amount': 2},
        {'name': 'C2', 'code': '002', 'amount': 5},
        {'name': 'C3', 'code': '003', 'amount': 3},
        {'name': 'C4', 'code': '004', 'amount': 8},
        {'name': 'C5', 'code': '005', 'amount': 9},
    ]
    return render(request, 'ld_stock/_items.html', dict(items=items))
class StockIndexView(View):
    template_name = 'ld_stock/index.html'
    @method_decorator(check_menu_used('LD001'))
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        print('Today is : ', timezone.now().strftime('%Y%m%d%H%M%S'))
        facility_id = request.session['company_id']
        bill_type_code = int(request.GET.get('bill_type', 1))
        bill_type = SysEnum.objects.filter(Q(sys_dict__code='D009') & Q(code=str(bill_type_code))).first()
        bills = StockBill.objects.filter(Q(bill_type=bill_type.id) & Q(facility=facility_id)).all().order_by('bill_no')
        paginator = Paginator(bills, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(bills=page.object_list, page=page, bill_type_code=bill_type_code))
class StockAddView(View):
    template_name = 'ld_stock/edit.html'
    form_class = StockForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        stock_type = kwargs['stock_type']
        print(f'Stock type is {stock_type}')
        form = self.form_class(facility_id, stock_type)
        items = [
            {'name': 'C1', 'code': '001', 'amount': 2},
            {'name': 'C2', 'code': '002', 'amount': 5},
            {'name': 'C3', 'code': '003', 'amount': 3},
            {'name': 'C4', 'code': '004', 'amount': 8},
            {'name': 'C5', 'code': '005', 'amount': 9},
        ]
        print(f'Facility id is {form.facility_id} , stock type is {form.stock_type}')
        return render(request, self.template_name, dict(form=form, stock_type=stock_type, items=items))
class StockEditView(View):
    pass