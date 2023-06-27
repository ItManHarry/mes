import jwt
from jwt import exceptions
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate
@csrf_exempt
def test(request):
    print('Test the api , method is : ', request.method)
    payload = {'username': '20112004'}
    token = gen_token(payload)
    response = JsonResponse({
        'code': 200,
        'message': 'OK',
        'token': token
    })
    # 支持跨域访问
    response['Access-Control-Allow-Origin'] = '*'  # 允许所有IP访问
    return response
@csrf_exempt
def get_token(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print('User name {}, password {}.'.format(username, password))
    user = authenticate(request, username=username, password=password)
    if user:
        payload = {'username': username}
        token = gen_token(payload, 10)
        response = JsonResponse({'code': 1, 'message': '令牌获取成功！', 'token': token})
    else:
        response = JsonResponse({'code': 0, 'message': '用户名或密码错误！'})
    # 支持跨域访问
    response['Access-Control-Allow-Origin'] = '*'  # 允许所有IP访问
    return response
@csrf_exempt
def validate_token(request):
    token = request.POST.get('token')
    print('Token is : ', token)
    secret_key = settings.SECRET_KEY
    try:
        # 解码时也要指定加密算法
        result = jwt.decode(token, key=secret_key, algorithms=['HS256'])
        print('Result is : ', result)
        response = JsonResponse({'code': 200, 'message': '令牌验证通过!'})
    except exceptions.ExpiredSignatureError:
        response = JsonResponse({'code': 1001, 'message': "令牌失效!"})
    except exceptions.DecodeError:
        response = JsonResponse({'code': 1002, 'message': '令牌认证失败!'})
    except exceptions.InvalidTokenError:
        response = JsonResponse({'code': 1003, 'message': '非法令牌!'})
    # 支持跨域访问
    response['Access-Control-Allow-Origin'] = '*'  # 允许所有IP访问
    return response
def gen_token(payload, timeout=1):
    secret_key = settings.SECRET_KEY
    # headers = {
    #     'type': 'jwt',
    #     'alg': 'HS256',
    # }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)  # 设置到期时间(默认1分钟)
    token = jwt.encode(payload=payload, key=secret_key, algorithm='HS256')
    print('Token type is : ', type(token))
    return token