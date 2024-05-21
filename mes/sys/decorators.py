from functools import wraps
from sys_auth.models import RecentUsedMenu, Role, Menu
from django.utils import timezone
'''
检查菜单是否使用过，使用过更新时间，否则新增到最近使用的菜单中
'''
def check_menu_used(menu_code):
    def do_check(function):
        @wraps(function)
        def decorated_function(request, *args, **kwargs):
            user = request.user
            if user:
                menu = Menu.objects.filter(code=menu_code).first()
                if menu:
                    role_id = request.session.get('role_id', None)
                    if role_id:
                        role = Role.objects.get(pk=role_id)
                        rum = RecentUsedMenu.objects.filter(menu=menu, user=user, role=role).first()
                        if not rum:
                            RecentUsedMenu.objects.create(menu=menu, user=user, role=role)
                        else:
                            rum.updated_on = timezone.now()
                            rum.save()
            return function(request, *args, **kwargs)
        return decorated_function
    return do_check