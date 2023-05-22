from django.shortcuts import render, redirect, reverse
from .models import Employee
from .forms import EmployeeForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
@login_required
def index(request):
    employees = Employee.objects.all().order_by('code')
    return render(request, 'employee/index.html', context=dict(employees=employees))
@login_required
def add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        # form = EmployeeForm(None, request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.code = employee.code.upper()
            user = request.user
            if user:
                employee.created_by = user.id
            employee.save()
            return redirect(reverse('org_emp:index'))
    else:
        form = EmployeeForm()
        # form = EmployeeForm(None)
    return render(request, 'employee/edit.html', context=dict(form=form, nav='新增雇员信息'))
@login_required
def edit(request, id):
    employee = Employee.objects.get(pk=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        # form = EmployeeForm(request.POST, p_id=id, instance=employee)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.code = employee.code.upper()
            employee.updated_on = timezone.now()
            user = request.user
            if user:
                employee.updated_by = user.id
            employee.save()
            return redirect(reverse('org_emp:index'))
    else:
        form = EmployeeForm(instance=employee)
        # form = EmployeeForm(p_id=id, instance=employee)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'employee/edit.html', context=dict(form=form, nav='编辑雇员信息'))