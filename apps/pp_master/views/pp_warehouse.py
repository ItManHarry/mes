from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import Paginator
from mes.sys.decorators import check_menu_used
from ..forms.pp_warehouse import WarehouseForm, LocationForm
from ..models import Warehouse, Location
from django.db.models import Q
class WarehousrIndexView(View):
    template_name = 'pp_master/pp_warehouse/index.html'
    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP007'))
    def get(self, request):
        facility_id = request.session['company_id']
        all = Warehouse.objects.filter(facility=facility_id).all().order_by('code')
        paginator = Paginator(all, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(warehouses=page.object_list, page=page))
def set_default_warehouse(facility_id):
    # 如果没有设定默认仓库,系统自动默认最先创建的仓库为默认仓库
    set_default = False
    for warehouse in Warehouse.objects.filter(facility=facility_id).all():
        if warehouse.default:
            set_default = True
    if not set_default:
        warehouse = Warehouse.objects.filter(facility=facility_id).order_by('created_on').first()
        warehouse.default = True
        warehouse.save()
class WarehouseAddView(View):
    template_name = 'pp_master/pp_warehouse/edit.html'
    form_class = WarehouseForm
    @method_decorator(login_required)
    def get(self, request):
        facility_id = request.session['company_id']
        form = self.form_class(facility_id)
        return render(request, self.template_name, dict(form=form))

    @method_decorator(login_required)
    def post(self, request):
        facility_id = request.session['company_id']
        form = self.form_class(facility_id, request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.code = warehouse.code.strip().upper()
            if warehouse.default:
                for w in Warehouse.objects.filter(facility=facility_id).all():
                    w.default = False
                    w.save()
            user = request.user
            if user:
                warehouse.created_by = user.id
            warehouse.save()
            set_default_warehouse(facility_id)
            return redirect(reverse('pp_master:warehouses'))
        return render(request, self.template_name, dict(form=form))

class WarehouseEditView(View):
    template_name = 'pp_master/pp_warehouse/edit.html'
    form_class = WarehouseForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        warehouse = Warehouse.objects.get(pk=kwargs['warehouse_id'])
        facility_id = request.session['company_id']
        form = self.form_class(facility_id, instance=warehouse)
        return render(request, self.template_name, dict(form=form))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        warehouse = Warehouse.objects.get(pk=kwargs['warehouse_id'])
        facility_id = request.session['company_id']
        form = self.form_class(facility_id, request.POST, instance=warehouse)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.code = warehouse.code.strip().upper()
            if warehouse.default:
                for w in Warehouse.objects.filter(Q(facility=facility_id) & ~Q(id=warehouse.id)).all():
                    w.default = False
                    w.save()
            user = request.user
            if user:
                warehouse.updated_by = user.id
            warehouse.updated_on = timezone.now()
            warehouse.save()
            set_default_warehouse(facility_id)
            return redirect(reverse('pp_master:warehouses'))
        return render(request, self.template_name, dict(form=form))
def set_location_default(warehouse):
    set_default = False
    for location in warehouse.locations.all():
        if location.default:
            set_default = True
    if not set_default:
        location = warehouse.locations.order_by('created_on').first()
        location.default = True
        location.save()
class LocationAddView(View):
    template_name = 'pp_master/pp_warehouse/locations.html'
    form_class = LocationForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        warehouse_id = kwargs['warehouse_id']
        form = self.form_class(warehouse_id)
        warehouse = Warehouse.objects.get(pk=warehouse_id)
        return render(request, self.template_name, dict(form=form, warehouse=warehouse, locations=warehouse.locations.all()))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        warehouse_id = kwargs['warehouse_id']
        form = self.form_class(warehouse_id, request.POST)
        warehouse = Warehouse.objects.get(pk=warehouse_id)
        if form.is_valid():
            location = form.save(commit=False)
            location.code = location.code.strip().upper()
            location.warehouse = warehouse
            if location.default:
                for lt in warehouse.locations.all():
                    lt.default = False
                    lt.save()
            user = request.user
            if user:
                location.created_by = user.id
            location.save()
            set_location_default(warehouse)
            return redirect(reverse('pp_master:location_add', args=(warehouse_id,)))
        else:
            print('Form validation failed ...')
        return render(request, self.template_name, dict(form=form, warehouse=warehouse, locations=warehouse.locations.all()))

class LocationEditView(View):
    template_name = 'pp_master/pp_warehouse/locations.html'
    form_class = LocationForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        warehouse_id = kwargs['warehouse_id']
        location = Location.objects.get(pk=kwargs['location_id'])
        form = self.form_class(warehouse_id, instance=location)
        warehouse = Warehouse.objects.get(pk=warehouse_id)
        return render(request, self.template_name, dict(form=form, warehouse=warehouse, locations=warehouse.locations.all()))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        warehouse_id = kwargs['warehouse_id']
        location_id = kwargs['location_id']
        location = Location.objects.get(pk=location_id)
        form = self.form_class(warehouse_id, request.POST, instance=location)
        warehouse = Warehouse.objects.get(pk=warehouse_id)
        if form.is_valid():
            location = form.save(commit=False)
            location.code = location.code.strip().upper()
            user = request.user
            if location.default:
                for lt in warehouse.locations.all():
                    lt.default = False
                    lt.save()
            if user:
                location.updated_by = user.id
            location.updated_on = timezone.now()
            location.save()
            set_location_default(warehouse)
            return redirect(reverse('pp_master:location_edit', args=(warehouse_id, location_id, )))
        else:
            print('Form validation failed ...')
        return render(request, self.template_name, dict(form=form, warehouse=warehouse, locations=warehouse.locations.all()))

@login_required
def get_locations(request, warehouse_id):
    warehouse = Warehouse.objects.get(pk=warehouse_id)
    locations = warehouse.locations.all()
    return render(request, 'pp_master/pp_warehouse/_location_items.html', dict(locations=locations))
