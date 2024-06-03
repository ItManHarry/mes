from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import Paginator
from mes.sys.decorators import check_menu_used
from django.http import JsonResponse
from ..forms.pp_warehouse import WarehouseForm
from ..models import Warehouse, Location
class WarehousrIndexView(View):
    template_name = 'pp_master/pp_warehouse/index.html'

    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP007'))
    def get(self, request):
        all = Warehouse.objects.all().order_by('code')
        paginator = Paginator(all, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(warehouses=page.object_list, page=page))

class WarehouseAddView(View):
    template_name = 'pp_master/pp_warehouse/edit.html'
    form_class = WarehouseForm

    def get(self, request):
        facility_id = request.session['company_id']
        form = self.form_class(facility_id)
        return render(request, self.template_name, dict(form=form))

class WarehouseEditView(View):
    pass