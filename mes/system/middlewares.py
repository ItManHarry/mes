# middlewares
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
def session_check(get_response):
    def check(request):
        print(request.path)
        print(request.path_info)
        print(request.headers.get('x-requested-with'))
        ajax_request = True if request.headers.get('x-requested-with') is not None and request.headers.get(
            'x-requested-with') == 'XMLHttpRequest' else False
        # 判断登录是否超时
        time_out = False
        try:
            request.session['username']
        except:
            time_out = True
        if time_out:
            print('Session timeout, please login system again.')
        print('Do the session check before the the view are called .........')
        exclude_urls = ['/sys_sign/login/', '/sys_sign/logout/']
        exclude = False
        if request.path in exclude_urls or 'static' in request.path:
            exclude = True
        if not exclude:
            print('<', request.path, '>检查session是否超时!')
            if time_out:
                if ajax_request:
                    response = HttpResponse()
                    response.headers['login_timeout'] = 'Y'
                    return response
                else:
                    return redirect(reverse('sys_sign:login'))
        else:
            print('<', request.path, '>不执行session超时检查!')
        response = get_response(request)
        print('Do the session check after the view are called ............')
        return response
    return check