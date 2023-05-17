from django.shortcuts import render, redirect, reverse
from .models import Role, Menu
from .forms import RoleForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
@login_required
def role_index(request):
    roles = Role.objects.all().order_by('code')
    return render(request, 'role/index.html', context=dict(roles=roles))
@login_required
def role_add(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.code = role.code.upper()
            user = request.user
            if user:
                role.created_by = user.id
            role.save()
            return redirect(reverse('sys_auth:role_index'))
    else:
        form = RoleForm()
    return render(request, 'role/edit.html', context=dict(form=form, nav='新增角色信息'))
@login_required
def role_edit(request, id):
    role = Role.objects.get(pk=id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save(commit=False)
            role.code = role.code.upper()
            role.updated_on = timezone.now()
            user = request.user
            if user:
                role.updated_by = user.id
            role.save()
            return redirect(reverse('sys_auth:role_index'))
    else:
        form = RoleForm(instance=role)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'role/edit.html', context=dict(form=form, nav='编辑角色信息'))