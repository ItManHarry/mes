from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from sys_auth.models import RecentUsedMenu, Role, Menu
from django.db.models import Q
def root(request):
    return redirect(reverse('sys_sign:login'))
def index(request):
    return render(request, 'index.html', context={})
def home(request):
    user = request.user
    # 获取最近使用&所有的菜单权限清单
    if user.is_superuser:
        recent_used_menus = RecentUsedMenu.objects.filter(user=user)
        all_menus = Menu.objects.all().order_by('code')
    else:
        role_id = request.session['role_id']
        role = Role.objects.get(pk=role_id)
        recent_used_menus = RecentUsedMenu.objects.filter(Q(user=user) & Q(role=role))
        all_menus = role.menus.order_by('code')
    return render(request, 'home.html', context=dict(recent_used_menus=recent_used_menus, all_menus=all_menus))