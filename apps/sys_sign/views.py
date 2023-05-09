from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from mail_tool import do_send_mail, send_mail_message, send_mail
from django.http import JsonResponse
from .models import SysLoginLog
def json_req(request):
    return JsonResponse(
        {'items': [1, 2, 3], 'status': 1, 'message': 'Succeeded!!!'}
    )
def do_login(request):
    login_message = ''
    try:
        next = request.GET['next']
    except:
        next = ''
    # print('Next page is : ', next)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next = request.POST['next']
        # if next:
        #     print('Next to ', next)
        # else:
        #     print('No next ...')
        # print('User name : {}, password {}.'.format(username, password))
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session['username'] = username
            # login_log = SysLoginLog(user=user, content='系统登录-'+username)
            # login_log.save()
            print('Authenticate succeeded!!!')
            # s = do_send_mail()
            # print('Send mail result is : ', s)
            # wordbooks = WordBook.objects.all().order_by('-name')
            # context = {'wordbooks': wordbooks}
            # send_mail_message(context)
            # send_mail('Send mail by Thread',
            #           ['guoqian.cheng@hyundai-di.com'],
            #           'mails/test.html', context,
            #           ['guoqian.cheng@hyundai-di.com'],
            #           'Email text body.', 'd:/data.xls')
            if next:
                return redirect(next)
            # return redirect(reverse('sys_sign:login'))
            login_message = 'User login successfully!'
            return render(request, 'index.html', context=dict(login_message=login_message))
        else:
            print('Authenticate failed!!!')
            login_message = 'User name or password is not correct!'
    return render(request, 'sys_sign/login.html', context=dict(login_message=login_message, next=next))
def do_logout(request):
    logout(request)
    return redirect(reverse('sys_sign:login'))