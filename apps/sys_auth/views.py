from django.shortcuts import render, redirect, reverse
from .models import Role, Menu
from .forms import RoleForm, MenuForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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

@login_required
def menu_index(request):
    menus = Menu.objects.all().order_by('code')
    return render(request, 'menu/index.html', context=dict(menus=menus))
@login_required
def menu_add(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.code = menu.code.upper()
            user = request.user
            if user:
                menu.created_by = user.id
            menu.save()
            return redirect(reverse('sys_auth:menu_index'))
    else:
        form = MenuForm()
    return render(request, 'menu/edit.html', context=dict(form=form, nav='新增菜单信息'))
@login_required
def menu_edit(request, id):
    menu = Menu.objects.get(pk=id)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.code = menu.code.upper()
            menu.updated_on = timezone.now()
            user = request.user
            if user:
                menu.updated_by = user.id
            menu.save()
            return redirect(reverse('sys_auth:menu_index'))
    else:
        form = MenuForm(instance=menu)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'menu/edit.html', context=dict(form=form, nav='编辑菜单信息'))
@login_required
def get_role_menus(request, id):
    role = Role.objects.get(pk=id)
    all_menus = [(menu.id, '({})-{}'.format(menu.code, menu.name)) for menu in Menu.objects.all().order_by('code')]
    # print('Type is : ', type(role.menus))
    authed_menus = [menu.id for menu in role.menus.all()]
    return JsonResponse({
        'code': '1',
        'message': 'Success',
        'all_menus': all_menus,
        'authed_menus': authed_menus
    })
@login_required
def auth_role_menus(request, id):
    # 接收参数
    params = request.POST
    # print(params)
    # for k, v in params.items():
    #     print('key is : ', k, ', value is : ', v)
    menu_ids = params.get('menu_ids')
    end = len(menu_ids) - 1
    # 剔除'[]'及引号'"'
    menu_ids = menu_ids[1:end].replace('"', '')
    menu_ids = menu_ids.split(',')
    # 选择的菜单清单
    menus = Menu.objects.filter(id__in=menu_ids)
    role = Role.objects.get(pk=id)
    print(role)
    # 清空已授权菜单
    role.menus.clear()
    # 重新授权菜单
    for menu in menus:
        role.menus.add(menu)
    return JsonResponse({
        'code': '1',
        'message': '菜单授权成功！',
    })