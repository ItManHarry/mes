from django.shortcuts import render, redirect, reverse
from .models import Role, Menu
from django.db.models import Q
from org_emp.models import Employee
from .forms import RoleForm, MenuForm, UserForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.conf import settings
@login_required
def role_index(request):
    user = request.user
    if user.is_superuser:
        roles = Role.objects.all().order_by('code')
    else:
        roles = Role.objects.filter(company_id=request.session['company_id']).order_by('code')
    paginator = Paginator(roles, settings.PAGE_ITEMS)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)
    return render(request, 'role/index.html', context=dict(roles=page.object_list, page=page))
@login_required
def role_add(request):
    company_id = request.session['company_id']
    if request.method == 'POST':
        form = RoleForm(company_id, request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.code = role.code.upper()
            user = request.user
            if user:
                role.created_by = user.id
            role.save()
            return redirect(reverse('sys_auth:role_index'))
    else:
        form = RoleForm(company_id)
    return render(request, 'role/edit.html', context=dict(form=form, nav='新增角色信息'))
@login_required
def role_edit(request, id):
    role = Role.objects.get(pk=id)
    company_id = request.session['company_id']
    if request.method == 'POST':
        form = RoleForm(company_id, request.POST, instance=role)
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
        form = RoleForm(company_id, instance=role)
        # print('Code is {} name is {}'.format(form.code, form.name))
    return render(request, 'role/edit.html', context=dict(form=form, nav='编辑角色信息'))

@login_required
def menu_index(request):
    menus = Menu.objects.all().order_by('code')
    paginator = Paginator(menus, settings.PAGE_ITEMS)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)
    return render(request, 'menu/index.html', context=dict(menus=page.object_list, page=page))
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
    user = request.user
    if user.is_superuser:   # 超级管理员
        all_menus = [(menu.id, '({})-{}'.format(menu.code, menu.name)) for menu in Menu.objects.all().order_by('code')]
    else:                   # 当前登录角色具备的菜单权限进行下发
        current_role_id = request.session['role_id']
        current_role = Role.objects.get(pk=current_role_id)
        all_menus = [(menu.id, '({})-{}'.format(menu.code, menu.name)) for menu in current_role.menus.all().order_by('code')]
    # print('Type is : ', type(role.menus))
    authed_menus = [menu.id for menu in role.menus.all()]
    return JsonResponse({
        'code': '1',
        'message': 'Success',
        'all_menus': all_menus,
        'authed_menus': authed_menus
    })
@login_required
def get_role_users(request, id):
    role = Role.objects.get(pk=id)
    return JsonResponse({
        'code': '1',
        'message': 'Success',
        'users': [f'{user.employee.name}({user.username})' if user.is_staff else f'{user.last_name}{user.first_name}({user.username})' for user in role.users.all()],
    })
@login_required
def get_roles(request, user_id):
    # 待授权用户
    auth_user = User.objects.get(pk=user_id)
    auth_user_roles = auth_user.role_set.all()
    authed_roles = [role.id for role in auth_user_roles]
    print('Auth user is : ', auth_user, ', authed rules : ', auth_user_roles)
    # 当前用户
    current_user = request.user
    if current_user.is_superuser:
        current_user_roles = Role.objects.filter(~Q(id__in=authed_roles)).order_by('name')
    else:
        current_user_roles = current_user.role_set.filter(~Q(id__in=authed_roles)).order_by('name')
    print('Current user is : ', current_user, ', authed rules : ', current_user_roles)
    return JsonResponse({
        'code': 1,
        'message': 'OK',
        'for_select': [(role.id, role.company.name+'-'+role.name) for role in current_user_roles],    # 所有当前用户可授权角色清单
        'selected': [(role.id, role.company.name+'-'+role.name) for role in auth_user_roles],         # 待授权用户已授权角色清单
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
@login_required
def user_index(request):
    users = User.objects.all().order_by('username')
    paginator = Paginator(users, settings.PAGE_ITEMS)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)
    return render(request, 'user/index.html', context=dict(users=page.object_list, page=page))
@login_required
def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # 保存
            user = User(username=data['username'], first_name=data['name'][1:], last_name=data['name'][:1], email=data['email'], is_superuser=False, is_staff=data['is_staff'])
            user.set_password(data['password'])
            user.save()
            # 关联雇员
            if data['is_staff']:
                employee = Employee.objects.get(pk=data['employee_id'])
                employee.user = user
                employee.save()
            return redirect(reverse('sys_auth:user_index'))
    else:
        form = UserForm()
    return render(request, 'user/edit.html', context=dict(form=form))
@login_required
def user_edit(request, id):
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # 保存
            user.username = data['username']
            user.first_name = data['name'][1:]
            user.last_name = data['name'][:1]
            user.email = data['email']
            user.is_staff = data['is_staff']
            if data['password'].strip():
                user.set_password(data['password'])
            user.save()
            # 关联雇员
            if data['is_staff']:
                employee = Employee.objects.get(pk=data['employee_id'])
                employee.user = user
                employee.save()
            # 当前用户密码修改后，必须重新登录系统，否则系统报错
            if request.user == user and data['password'].strip():
                return redirect(reverse('sys_sign:relogin'))
            return redirect(reverse('sys_auth:user_index'))
    else:
        form = UserForm({
            'id': user.id,
            'is_staff': user.is_staff,
            'username': user.username,
            'name': user.last_name+user.first_name,
            'password': '',
            'email': user.email,
            'employee': user.employee.name if hasattr(user, 'employee') else '',
            'employee_id': user.employee.id if hasattr(user, 'employee') else '',
        })
    return render(request, 'user/edit.html', context=dict(form=form))
@login_required
def auth_user_roles(request, id):
    user = User.objects.get(pk=id)
    # 接收参数
    params = request.POST
    roles = params.get('roles')
    end = len(roles) - 1
    # 剔除'[]'及引号'"'
    roles = roles[1:end].replace('"', '')
    roles = roles.split(',')
    # 选择的角色清单
    roles = Role.objects.filter(id__in=roles)
    print('Selected roles are : ', roles)
    # 清空已授权角色
    user.role_set.clear()
    # 重新授权
    for role in roles:
        user.role_set.add(role)
    return JsonResponse({
        'code': '1',
        'message': '用户授权成功！',
    })
@login_required
def reset_password(request, id):
    user = User.objects.get(pk=id)
    pwd = request.POST['pwd']
    user.set_password(pwd)
    user.save()
    username = request.session['username']
    if username == user.username:
        return JsonResponse({
            'code': '2',
            'message': '当前账号密码重置成功,请重新登录！'
        })
    return JsonResponse({
        'code': '1',
        'message': '密码重置成功！'
    })
@login_required
def user_status(request, id, status):
    user = User.objects.get(pk=id)
    print('User id is : ', id, ', status is : ', status)
    user.is_active = True if status == 1 else False
    user.save()
    return JsonResponse({
        'code': '1',
        'message': '用户状态修改完成！'
    })