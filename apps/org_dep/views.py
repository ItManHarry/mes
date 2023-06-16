from django.shortcuts import render, redirect, reverse
from .models import Department
from .forms import DepartmentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        departments = Department.objects.all().order_by('code')
    else:
        departments = Department.objects.filter(company_id=request.session['company_id']).order_by('code')
    paginator = Paginator(departments, settings.PAGE_ITEMS)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)
    return render(request, 'department/index.html', context=dict(departments=page.object_list, page=page))
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