from django.views import View
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from mes.sys.decorators import check_menu_used
from ..models.ld_stock import StockBill
from ..models.ld_stock_barcode import StockBarCode, StockBarCodeList
from sys_dict.models import SysEnum
from django.db.models import Q
from ..forms.stock import StockForm
import json
from pp_master.models.pp_component import ComponentInOutList, ComponentAmount
from pp_master.models.pp_warehouse import Warehouse
from datetime import datetime
import random
@login_required
def get_io_select_items(request, stock_type):
    facility_id = request.session['company_id']
    items = []
    print('Facility id is :', facility_id)
    if stock_type == 1:     # 入库
        bar_codes = StockBarCode.objects.filter(facility=facility_id).filter(active=True).order_by('-code')
        for bar_code in bar_codes:
            sum = 0
            for item in bar_code.items.all():
                if item.amount != item.amount_in:
                    sum += item.amount - item.amount_in     # 总数量和已入库数量差即为可入库数量
            if sum:
                items.append({'code': bar_code.code, 'amount': sum, 'id': bar_code.id})
    else:                   # 出库
        # 查询库存余额
        ids = json.loads(request.POST.get('ids'))   # 已选择的剔除掉
        com_amounts = ComponentAmount.objects.filter(~Q(id__in=ids) & Q(component__facility=facility_id)).all().order_by('component')
        components = {}
        for com_amount in com_amounts:
            if com_amount.component.id in components:
                components[com_amount.component.id].append(com_amount)
            else:
                components[com_amount.component.id] = [com_amount]
        for component, amounts in components.items():
            print(f'Component is {component}, amounts {amounts}')
            total = 0
            for amount in amounts:
                total += amount.quantity
            items.append({'code': amounts[0].component, 'amount': total, 'id': component})
    return render(request, 'ld_stock/_items_select_list.html', dict(items=items, stock_in=True if stock_type == 1 else False))
@login_required
def set_selected_items(request):
    facility_id = request.session['company_id']
    stock_type = int(request.POST.get('stock_type'))
    print(f'Stock type is : {stock_type}')
    ids = json.loads(request.POST.get('ids'))
    warehouses, locations = [], []
    if stock_type == 1:
        print('Barcode ids :\t', ids)
        barcodes = StockBarCode.objects.filter(id__in=ids).all().order_by('code')
        items = []
        for barcode in barcodes:
            for item in barcode.items.all():
                items.append(item)
        warehouses = Warehouse.objects.filter(facility=facility_id).order_by('code')
        default_warehouse = Warehouse.objects.filter(Q(facility=facility_id) & Q(default=True)).first()
        locations = default_warehouse.locations.all()
    else:
        print('Component ids :\t', ids)
        items = [amount for amount in ComponentAmount.objects.filter(component__id__in=ids).all().order_by('component')]
    return render(request, 'ld_stock/_items.html', dict(stock_type=stock_type, items=items, warehouses=warehouses, locations=locations))
class StockIndexView(View):
    template_name = 'ld_stock/index.html'
    @method_decorator(check_menu_used('LD001'))
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        print('Today is : ', timezone.now().strftime('%Y%m%d%H%M%S'))
        facility_id = request.session['company_id']
        bill_type_code = int(request.GET.get('bill_type', 1))
        bill_type = SysEnum.objects.filter(Q(sys_dict__code='D009') & Q(code=str(bill_type_code))).first()
        bills = StockBill.objects.filter(Q(bill_type=bill_type.id) & Q(facility=facility_id)).all().order_by('-bill_no')
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
        # print(f'Stock type is : {stock_type}')
        form = self.form_class(facility_id, stock_type)
        # print(f'Facility id is {form.facility_id} , stock type is {form.stock_type}')
        return render(request, self.template_name, dict(form=form, stock_type=stock_type))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        stock_type = kwargs['stock_type']
        form = self.form_class(facility_id, stock_type, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            component_ids, barcode_items, warehouses, locations, amounts = json.loads(data['items'])
            dict_warehouse = dict(zip(component_ids, warehouses))
            dict_barcode_items = dict(zip(component_ids, barcode_items))
            dict_locations = dict(zip(component_ids, locations))
            dict_amounts = dict(zip(component_ids, amounts))
            print('Component ids : ', component_ids)
            print('Barcode dictionary : ', dict_barcode_items)
            print('Warehouse dictionary : ', dict_warehouse)
            print('Location dictionary : ', dict_locations)
            print('Amount dictionary : ', dict_amounts)
            # 执行保存
            bill = form.save(commit=False)
            bill.bill_type = SysEnum.objects.filter(Q(sys_dict__code='D009') & Q(code='1')).first() if stock_type == 1 else SysEnum.objects.filter(Q(sys_dict__code='D009') & Q(code='2')).first()
            bill.bill_no = ('IN' if stock_type == 1 else 'OUT')+datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(10, 99))
            user = request.user
            bill.created_by = user.id
            bill.in_out_by_id = user.id
            bill.save()
            # 出入库明细&库存余额
            for component_id, warehouse_id in dict_warehouse.items():
                # 生成出入库明细
                print(f'Component id : {component_id}, warehouse is {warehouse_id}')
                item = ComponentInOutList(bill=bill,
                                          component_id=component_id,
                                          warehouse_id=warehouse_id,
                                          location_id=dict_locations[component_id],
                                          quantity=int(dict_amounts[component_id]),
                                          inout_type=data['in_out_type'],
                                          created_by=user.id)
                item.save()
                if stock_type == 1:
                    # 更新barcode item入库数量
                    barcode_item = StockBarCodeList.objects.get(pk=dict_barcode_items[component_id])
                    barcode_item.amount_in = int(dict_amounts[component_id])
                    barcode_item.updated_by = user.id
                    barcode_item.updated_on = timezone.now()
                    barcode_item.save()
                    # 入库计算库存余额
                    c_amount = ComponentAmount.objects.filter(Q(component_id=component_id) & Q(warehouse_id=warehouse_id) & Q(location_id=dict_locations[component_id])).first()
                    if c_amount:
                        # 存在则更新
                        c_amount.quantity += int(dict_amounts[component_id])
                        c_amount.updated_by = user.id
                        c_amount.updated_on = timezone.now()
                    else:
                        # 不存在则新增
                        c_amount = ComponentAmount(component_id=component_id,
                                                   warehouse_id=warehouse_id,
                                                   location_id=dict_locations[component_id],
                                                   quantity=int(dict_amounts[component_id]),
                                                   created_by=user.id)
                    c_amount.save()
                else:
                    # 出库计算库存余额
                    c_amount = ComponentAmount.objects.filter(
                        Q(component_id=component_id) & Q(warehouse_id=warehouse_id) & Q(
                            location_id=dict_locations[component_id])).first()
                    c_amount.quantity -= int(dict_amounts[component_id])
                    c_amount.updated_by = user.id
                    c_amount.updated_on = timezone.now()
                    c_amount.save()
            return redirect('/ld_stock/stock/index/?bill_type='+str(stock_type))
        return render(request, self.template_name, dict(form=form, stock_type=stock_type))
class StockEditView(View):
    pass