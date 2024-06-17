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
class StockIndexView(View):
    template_name = 'ld_stock/index.html'
    @method_decorator(check_menu_used('PP009'))
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        print('Facility id is : ', facility_id)
        bill_type_code = int(request.GET.get('bill_type', 1))
        print('Bill type code is : ', bill_type_code, type(bill_type_code))
        bill_type = SysEnum.objects.filter(Q(sys_dict__code='D009') & Q(code=str(bill_type_code))).first()
        print('Bill type id is : ', bill_type.id)
        bills = StockBill.objects.filter(Q(bill_type=bill_type.id) & Q(facility=facility_id)).all().order_by('bill_no')
        paginator = Paginator(bills, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(bills=page.object_list, page=page, bill_type_code=bill_type_code))
class StockAddView(View):
    pass
class StockEditView(View):
    pass