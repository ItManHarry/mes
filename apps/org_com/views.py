from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from .models import Company
from org_dep.models import Department
from org_dep.forms import get_sub_departments
from .forms import CompanyForm
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
@login_required
def index(request):
    companies = Company.objects.all()
    return render(request, 'company/index.html', context=dict(companies=companies))
@login_required
def add(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.code = company.code.upper()
            user = request.user
            if user:
                company.created_by = user.id
            company.save()
            return redirect(reverse('org_com:index'))
    else:
        form = CompanyForm()
    return render(request, 'company/edit.html', context=dict(form=form, nav='新增公司信息'))
@login_required
def edit(request, id):
    company = Company.objects.get(pk=id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.code = company.code.upper()
            company.updated_on = timezone.now()
            user = request.user
            if user:
                company.updated_by = user.id
            company.save()
            return redirect(reverse('org_com:index'))
    else:
        form = CompanyForm(instance=company)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'company/edit.html', context=dict(form=form, nav='编辑公司信息'))
@login_required
def get_departments(request, id):
    try:
        company = Company.objects.get(pk=id)
    except:
        company = None
    if company:
        department_id = ''
        try:
            department_id = request.POST['department_id']
            print('Department id is : ', department_id)
            department = Department.objects.get(pk=department_id)
        except:
            department = None
        if department:
            # 编辑部门信息
            # print('Edit the department...')
            sub_ids = [department_id]
            get_sub_departments(department_id, sub_ids)
            # print('Sub Departments are : ', sub_ids)
            departments = company.department_set.filter(~Q(id=department_id) & ~Q(parent_id__in=sub_ids)).order_by('code')
        else:
            # 新增部门信息
            # print('Add the department...')
            departments = company.department_set.order_by('code')
    else:
        departments = Department.objects.none()
    return render(request, 'company/_departments.html', context=dict(departments=departments))
    # return JsonResponse({
    #     'departments': [(department.id, department.name) for department in company.department_set.all()]
    # })