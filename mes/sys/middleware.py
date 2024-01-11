# middlewares
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from common.models import SysLog
from django.contrib.auth.models import User
from datetime import timedelta
def session_check(get_response):
    def check(request):
        # 是否是Ajax请求
        ajax_request = True if request.headers.get('x-requested-with') is not None and request.headers.get(
            'x-requested-with') == 'XMLHttpRequest' else False
        # 登录是否超时
        time_out = False
        try:
            request.session['username']
        except:
            time_out = True
        exclude_urls = [
            '/sys_sign/login/',
            '/sys_sign/logout/',
            '/sys_sign/relogin/',
            '/sys_sign/roles/',
            '/',
            '/test/',
            '/api/test/',
            '/api/test',
            '/api/token/get/',
            '/api/token/get',
            '/api/token/validate/',
            '/api/token/validate',
        ]
        exclude = False
        if request.path in exclude_urls or 'static' in request.path:
            exclude = True
        if exclude:
            print('<', request.path, '>不执行session超时检查!')
        else:
            print('<', request.path, '>检查session是否超时!')
            if time_out:
                '''
                    已超时：
                        1. Ajax请求返回Response，并标识session已超时
                        2. 非Ajax请求跳转至登录页
                '''
                if ajax_request:
                    response = HttpResponse()
                    response.headers['login_timeout'] = 'Y'
                    return response
                else:
                    return redirect(reverse('sys_sign:relogin'))
            else:
                '''
                若未超时，session续时间
                '''
                request.session.set_expiry(timedelta(minutes=30))
        print('Do the session check before the request ...')
        response = get_response(request)
        print('Do the session check after the request ...')
        if not exclude:
            # 记录登录日志
            ip = request.META.get('REMOTE_ADDR')
            log = SysLog(url=request.path, ip=ip)
            # log.url =
            user = request.user
            if isinstance(user, User):
                log.user = user
                log.created_by = user.id
                log.updated_by = user.id
            log.save()
        return response
    return check