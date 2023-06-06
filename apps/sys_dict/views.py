from django.shortcuts import render, redirect, reverse
from .models import SysEnum, SysDict
from .forms import SysDictForm, SysEnumForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def dict_index(request):
    dicts = SysDict.objects.all()
    return render(request, 'sys_dict/index.html', context=dict(dicts=dicts))
@login_required
def dict_add(request):
    if request.method == 'POST':
        form = SysDictForm(request.POST)
        if form.is_valid():
            sys_dict = form.save(commit=False)
            sys_dict.code = sys_dict.code.upper()
            user = request.user
            if user:
                sys_dict.created_by = user.id
            sys_dict.save()
            return redirect(reverse('sys_dict:dict_index'))
    else:
        form = SysDictForm()
    return render(request, 'sys_dict/edit.html', context=dict(form=form, title='新增字典'))
@login_required
def dict_edit(request, id):
    sys_dict = SysDict.objects.get(pk=id)
    if request.method == 'POST':
        form = SysDictForm(request.POST, instance=sys_dict)
        if form.is_valid():
            sys_dict = form.save(commit=False)
            sys_dict.code = sys_dict.code.upper()
            sys_dict.updated_on = timezone.now()
            user = request.user
            if user:
                sys_dict.updated_by = user.id
            sys_dict.save()
            return redirect(reverse('sys_dict:dict_index'))
    else:
        form = SysDictForm(instance=sys_dict)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'sys_dict/edit.html', context=dict(form=form, title='编辑字典'))
@login_required
def enum_add(request, dict_id):
    sys_dict = SysDict.objects.get(pk=dict_id)
    enums = sys_dict.sysenum_set.order_by('code').all()
    if request.method == 'POST':
        form = SysEnumForm(request.POST)
        if form.is_valid():
            enum = form.save(commit=False)
            enum.sys_dict = sys_dict
            enum.save()
            return redirect(reverse('sys_dict:enum_add', args=(dict_id, )))
    else:
        form = SysEnumForm()
    return render(request, 'sys_dict/enums.html', context=dict(enums=enums, form=form, sys_dict=sys_dict))
@login_required
def enum_edit(request, dict_id, enum_id):
    sys_dict = SysDict.objects.get(pk=dict_id)
    enums = sys_dict.sysenum_set.order_by('code').all()
    enum = SysEnum.objects.get(pk=enum_id)
    if request.method == 'POST':
        form = SysEnumForm(request.POST, instance=enum)
        if form.is_valid():
            enum = form.save(commit=False)
            enum.updated_on = timezone.now()
            enum.save()
            return redirect(reverse('sys_dict:enum_edit', args=(dict_id, enum_id, )))
    else:
        form = SysEnumForm(instance=enum)
    return render(request, 'sys_dict/enums.html', context=dict(enums=enums, form=form, sys_dict=sys_dict))