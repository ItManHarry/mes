from django.shortcuts import render, redirect, reverse
from .models import Company
from .forms import CompanyForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
@login_required
def company_index(request):
    companies = Company.objects.all()
    return render(request, 'company/index.html', context=dict(companies=companies))
@login_required
def company_add(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            user = request.user
            if user:
                company.created_by = user.id
            company.save()
            return redirect(reverse('org_com:company_index'))
    else:
        form = CompanyForm()
    return render(request, 'company/edit.html', context=dict(form=form, nav='新增公司信息'))
@login_required
def company_edit(request, id):
    company = Company.objects.get(pk=id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.updated_on = timezone.now()
            user = request.user
            if user:
                company.updated_by = user.id
            company.save()
            return redirect(reverse('org_com:company_index'))
    else:
        form = CompanyForm(instance=company)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'company/edit.html', context=dict(form=form, nav='编辑公司信息'))