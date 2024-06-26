from django.shortcuts import render, redirect, reverse
from .models import Employee
from .forms import EmployeeForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from mes.sys.upload import handle_uploaded_file
from django.conf import settings
from django.core.paginator import Paginator
from mes.sys.decorators import check_menu_used
import os, xlrd3
from collections import namedtuple
from common.forms import ExcelImportForm
@login_required
@check_menu_used('OR003')
def index(request):
    form = ExcelImportForm()
    user = request.user
    if user.is_superuser:
        employees = Employee.objects.all().order_by('code')
    else:
        employees = Employee.objects.filter(department__company_id=request.session['company_id']).order_by('code')
    paginator = Paginator(employees, settings.PAGE_ITEMS)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)
    return render(request, 'employee/index.html', context=dict(employees=page.object_list, page=page, form=form))
@login_required
def add(request):
    company_id = request.session['company_id']
    if request.method == 'POST':
        # form = EmployeeForm(request.POST)
        form = EmployeeForm(company_id, request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.code = employee.code.upper()
            if 'photo' in request.FILES:
                file = request.FILES['photo']
                photo_path = handle_uploaded_file(file, 'employee')
                if photo_path:
                    employee.photo_path = photo_path
            user = request.user
            if user:
                employee.created_by = user.id
            employee.save()
            return redirect(reverse('org_emp:index'))
    else:
        # form = EmployeeForm()
        form = EmployeeForm(company_id)
    return render(request, 'employee/edit.html', context=dict(form=form, nav='新增雇员信息'))
@login_required
def edit(request, id):
    company_id = request.session['company_id']
    employee = Employee.objects.get(pk=id)
    if request.method == 'POST':
        # form = EmployeeForm(request.POST, instance=employee)
        form = EmployeeForm(company_id, request.POST, request.FILES, instance=employee)
        # form.company_id = company_id
        if form.is_valid():
            employee = form.save(commit=False)
            employee.code = employee.code.upper()
            if 'photo' in request.FILES:
                file = request.FILES['photo']
                photo_path = handle_uploaded_file(file, 'employee')
                if photo_path:
                    employee.photo_path = photo_path
            employee.updated_on = timezone.now()
            user = request.user
            if user:
                employee.updated_by = user.id
            employee.save()
            return redirect(reverse('org_emp:index'))
    else:
        # form = EmployeeForm(instance=employee)
        form = EmployeeForm(company_id, instance=employee)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'employee/edit.html', context=dict(form=form, employee=employee, nav='编辑雇员信息'))
@login_required
def search_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
    else:
        name = request.GET['name']
    name = name.strip()
    # print('Search employee name is : ', name)
    if len(name) > 0:
        # print('Name is not empty...')
        employees = Employee.objects.filter(name__icontains=name).order_by('name')
    else:
        # print('Get all employees...')
        employees = Employee.objects.all().order_by('name')
    return render(request, 'employee/_search.html', context=dict(employees=employees))
def exe_import(request):
    file = request.FILES['file']
    file_path = handle_uploaded_file(file, 'employee')
    file_path = os.path.join(settings.UPLOAD_FILE_PATH, file_path)
    work_book = xlrd3.open_workbook(file_path)
    data_sheet = work_book.sheet_by_index(0)
    rows = data_sheet.nrows
    items = []
    Data = namedtuple('Data', ['code', 'name', 'department'])
    for i in range(1, rows):
        values = data_sheet.row_values(i)
        items.append(Data(*values))
    # 更新上级部门
    from org_dep.models import Department
    departments = Department.objects.all()
    parent_map = {}
    for department in departments:
        parent_map[department.code] = department
    for item in items:
        print(f'Employee : {item.code} - {item.name} - {item.department}')
        # 执行导入
        # 姓名为空或部门不存在则跳过
        if not item.name or not parent_map.get(item.department, None):
            continue
        employee = Employee(name=item.name, code=str(item.code).split('.')[0], department=parent_map.get(item.department))
        employee.save()
    return redirect(reverse('org_emp:index'))