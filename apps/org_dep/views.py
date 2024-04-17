from django.shortcuts import render, redirect, reverse
from .models import Department
from org_com.models import Company
from .forms import DepartmentForm, DepartmentImportForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from mes.sys.decorators import check_menu_used
from mes.sys.upload import handle_uploaded_file
import xlrd3
from collections import namedtuple
import os
@login_required
@check_menu_used('OR002')
def index(request):
    form = DepartmentImportForm()
    user = request.user
    if user.is_superuser:
        departments = Department.objects.all().order_by('code')
    else:
        departments = Department.objects.filter(company_id=request.session['company_id']).order_by('code')
    paginator = Paginator(departments, settings.PAGE_ITEMS)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)
    return render(request, 'department/index.html', context=dict(departments=page.object_list, page=page, form=form))
@login_required
def add(request):
    company_id = request.session['company_id']
    if request.method == 'POST':
        # form = DepartmentForm(request.POST)
        form = DepartmentForm(company_id, request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.code = department.code.upper()
            user = request.user
            if user:
                department.created_by = user.id
            department.save()
            return redirect(reverse('org_dep:index'))
    else:
        # form = DepartmentForm()
        form = DepartmentForm(company_id)
    return render(request, 'department/edit.html', context=dict(form=form, nav='新增部门信息'))
@login_required
def edit(request, id):
    department = Department.objects.get(pk=id)
    company_id = request.session['company_id']
    if request.method == 'POST':
        # form = DepartmentForm(request.POST, instance=department)
        form = DepartmentForm(company_id, request.POST, instance=department)
        if form.is_valid():
            department = form.save(commit=False)
            department.code = department.code.upper()
            department.updated_on = timezone.now()
            user = request.user
            if user:
                department.updated_by = user.id
            department.save()
            return redirect(reverse('org_dep:index'))
    else:
        # form = DepartmentForm(instance=department)
        form = DepartmentForm(company_id, instance=department)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'department/edit.html', context=dict(form=form, nav='编辑部门信息'))

def exe_import(request):
    file = request.FILES['file']
    file_path = handle_uploaded_file(file, 'department')
    file_path = os.path.join(settings.UPLOAD_FILE_PATH, file_path)
    work_book = xlrd3.open_workbook(file_path)
    data_sheet = work_book.sheet_by_index(0)
    rows = data_sheet.nrows
    items = []
    Data = namedtuple('Data', ['code', 'name', 'parent_code'])
    for i in range(1, rows):
        values = data_sheet.row_values(i)
        items.append(Data(*values))
    company = Company.objects.first()
    for item in items:
        print(f'Department : {item.code} - {item.name} - {item.parent_code}')
        # 执行导入
        department = Department(name=item.name, code=item.code, company=company)
        department.save()
    # 更新上级部门
    departments = Department.objects.all()
    parent_map = {}
    for department in departments:
        parent_map[department.code] = department
    for item in items:
        department = Department.objects.filter(code=item.code).first()
        if item.parent_code and item.parent_code != '99999999':
            department.parent = parent_map[item.parent_code]
            department.save()
    return redirect(reverse('org_dep:index'))