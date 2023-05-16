from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from mes.sys.email import send_mail
from django.http import JsonResponse
from .models import SysLogin
from datetime import timedelta
def json_req(request):
    name = request.POST['name']
    age = request.POST['age']
    print('I am {}, {} years old.'.format(name, age))
    return JsonResponse(
        {'items': [1, 2, 3], 'status': 1, 'message': 'Succeeded!!!'}
    )
def do_login(request):
    login_message = ''
    # try:
    #     next = request.GET['next']
    # except:
    #     next = ''
    # print('Next page is : ', next)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # next = request.POST['next']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session['username'] = username
            # 设置session过期时间-> 30分钟
            request.session.set_expiry(timedelta(minutes=30))
            # 登录IP地址
            ip = request.META.get('REMOTE_ADDR')
            # 记录登录日志
            login_log = SysLogin(user=user, ip=ip, created_by=user.id, updated_by=user.id)
            login_log.save()
            print('{} authenticate succeeded!!!'.format(username))
            # wordbooks = WordBook.objects.all().order_by('-name')
            # context = {'wordbooks': []}
            # send_mail('Send mail by Thread',
            #           ['guoqian.cheng@hyundai-di.com'],
            #           'mails/test.html', context,
            #           ['guoqian.cheng@hyundai-di.com'],
            #           'Email text body.', 'd:/data.xls')
            # if next:
            #     return redirect(next)
            return redirect(reverse('index'))
        else:
            print('Authenticate failed!!!')
            login_message = 'User name or password is not correct!'
    # return render(request, 'sys_sign/login.html', context=dict(login_message=login_message, next=next))
    return render(request, 'sys_sign/login.html', context=dict(login_message=login_message))
def do_logout(request):
    logout(request)
    return redirect(reverse('sys_sign:login'))
def re_login(request):
    return render(request, 'sys_sign/relogin.html', context={})