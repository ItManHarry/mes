from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.utils import timezone
from sys_auth.models import RecentUsedMenu, Role, Menu
from django.db.models import Q
from django.contrib.auth.decorators import login_required
def root(request):
    return redirect(reverse('sys_sign:login'))
def index(request):
    return render(request, 'index.html', context={})
def home(request):
    user = request.user
    # 获取最近使用&所有的菜单权限清单
    if user.is_superuser:
        recent_used_menus = [rum.menu for rum in RecentUsedMenu.objects.filter(user=user)]
        all_menus = Menu.objects.all().order_by('code')
    else:
        role_id = request.session['role_id']
        role = Role.objects.get(pk=role_id)
        recent_used_menus = [rum.menu for rum in RecentUsedMenu.objects.filter(Q(user=user) & Q(role=role))]
        all_menus = role.menus.order_by('code')
    return render(request, 'home.html', context=dict(recent_used_menus=recent_used_menus, all_menus=all_menus))
@login_required
def func(request):
    user = request.user
    params = request.POST
    code = params['code']
    menus = Menu.objects.filter(code__iexact=code)
    if menus:
        menu = menus[0]
        authed = False
        if user.is_superuser:
            authed = True
            rums = RecentUsedMenu.objects.filter(menu=menu, user=user)
            if not rums:
                RecentUsedMenu.objects.create(menu=menu, user=user)
            else:
                rum = rums[0]
                rum.updated_on = timezone.now()
                rum.save()
        else:
            role_id = request.session['role_id']
            role = Role.objects.get(pk=role_id)
            if menu in role.menus.all():
                authed = True
                rums = RecentUsedMenu.objects.filter(menu=menu, user=user, role=role)
                if not rums:
                    RecentUsedMenu.objects.create(menu=menu, user=user, role=role)
                else:
                    rum = rums[0]
                    rum.updated_on = timezone.now()
                    rum.save()
        if authed:
            tab = {'id': menu.id, 'name': menu.name, 'url': reverse(menu.url)}
            return JsonResponse({
                'code': 1,
                'tab': tab
            })
        else:
            return JsonResponse({
                'code': 0,
                'message': '功能菜单未授权！'
            })
    else:
        return JsonResponse({
            'code': 0,
            'message': '功能菜单不存在！'
        })
def test(request):
    return render(request, 'common/test.html', context={})