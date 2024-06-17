from django.views import View
from django.shortcuts import redirect, reverse, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator
from ..forms import ProductWorkCenterForm
from ..models import ProductWorkCenter
from mes.sys.decorators import check_menu_used
from org_emp.models import Employee, EmployeeWorkCenterChangeList
from django.http import JsonResponse
class ProductWorkCenterIndexView(View):
    template_name = 'pp_master/pp_workcenter/index.html'
    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP002'))
    def get(self, request):
        facility_id = request.session['company_id']
        wcs = ProductWorkCenter.objects.filter(facility=facility_id).all().order_by('code')
        paginator = Paginator(wcs, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(workcenters=page.object_list, page=page))
class ProductWorkCenterAddView(View):
    template_name = 'pp_master/pp_workcenter/edit.html'
    form_class = ProductWorkCenterForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        form = self.form_class(company_id)
        return render(request, self.template_name, dict(form=form))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        form = self.form_class(company_id, request.POST)
        if form.is_valid():
            workcenter = form.save(commit=False)
            workcenter.code = workcenter.code.upper().strip()
            user = request.user
            if user:
                workcenter.created_by = user.id
            workcenter.save()
            return redirect(reverse('pp_master:workcenters'))
        return render(request, self.template_name, dict(form=form))
class ProductWorkCenterEditView(View):
    template_name = 'pp_master/pp_workcenter/edit.html'
    form_class = ProductWorkCenterForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        workcenter = ProductWorkCenter.objects.get(pk=kwargs['workcenter_id'])
        form = self.form_class(company_id, instance=workcenter)
        return render(request, self.template_name, dict(form=form))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        workcenter = ProductWorkCenter.objects.get(pk=kwargs['workcenter_id'])
        form = self.form_class(company_id, request.POST, instance=workcenter)
        if form.is_valid():
            workcenter = form.save(commit=False)
            workcenter.code = workcenter.code.upper().strip()
            user = request.user
            if user:
                workcenter.updated_by = user.id
            workcenter.updated_on = timezone.now()
            workcenter.save()
            return redirect(reverse('pp_master:workcenters'))
        return render(request, self.template_name, dict(form=form))
@login_required
def get_workcenters_by_facility(request, facility_id):
    if facility_id == '000000000':
        workcenters = ProductWorkCenter.objects.none()
    else:
        workcenters = ProductWorkCenter.objects.filter(facility_id=facility_id).order_by('code')
    return render(request, 'pp_master/pp_workcenter/_workcenters.html', context=dict(workcenters=workcenters))
@login_required
def get_workcenters_by_line(request, line_id):
    if line_id == '000000000':
        workcenters = ProductWorkCenter.objects.none()
    else:
        workcenters = ProductWorkCenter.objects.filter(line_id=line_id).order_by('code')
    return render(request, 'pp_master/pp_workcenter/_workcenters.html', context=dict(workcenters=workcenters))
@login_required
def get_employees(request, wc_id):
    employees = []
    if wc_id:
        workcenter = ProductWorkCenter.objects.get(pk=wc_id)
        # print('Work center is : ', wc.employees.all(), type(wc.employees))
        if workcenter.employees.all():
            employees = workcenter.employees.all()
    # print('Employee list', employees)
    return render(request, 'pp_master/pp_workcenter/_employee_items.html', dict(employees=employees))
@login_required
def add_employee(request, wc_id, emp_id):
    workcenter = ProductWorkCenter.objects.get(pk=wc_id)
    employee = Employee.objects.get(pk=emp_id)
    # 已添加过的不重复添加
    if employee not in workcenter.employees.all():
        workcenter.employees.add(employee)
        user = request.user
        item = EmployeeWorkCenterChangeList(employee=employee, department=employee.department.name, work_center=workcenter)
        if user:
            item.created_by = user.id
        item.save()
        return JsonResponse({'code': 1, 'message': '添加成功！'})
    return JsonResponse({'code': 0, 'message': '工人已存在！'})
@login_required
def remove_employee(request, wc_id, emp_id):
    workcenter = ProductWorkCenter.objects.get(pk=wc_id)
    employee = Employee.objects.get(pk=emp_id)
    workcenter.employees.remove(employee)
    return JsonResponse({'code': 1, 'message': '工人已移除！'})