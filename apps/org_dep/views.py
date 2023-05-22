from django.shortcuts import render, redirect, reverse
from .models import Department
from .forms import DepartmentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
@login_required
def index(request):
    departments = Department.objects.all().order_by('code')
    return render(request, 'department/index.html', context=dict(departments=departments))
@login_required
def add(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        # form = DepartmentForm(None, request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.code = department.code.upper()
            user = request.user
            if user:
                department.created_by = user.id
            department.save()
            return redirect(reverse('org_dep:index'))
    else:
        form = DepartmentForm()
        # form = DepartmentForm(None)
    return render(request, 'department/edit.html', context=dict(form=form, nav='新增部门信息'))
@login_required
def edit(request, id):
    department = Department.objects.get(pk=id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        # form = DepartmentForm(request.POST, p_id=id, instance=department)
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
        form = DepartmentForm(instance=department)
        # form = DepartmentForm(p_id=id, instance=department)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'department/edit.html', context=dict(form=form, nav='编辑部门信息'))