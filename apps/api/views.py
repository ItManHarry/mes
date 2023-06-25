from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
@csrf_exempt
def test(request):
    print('Test the api , method is : ', request.method)
    response = JsonResponse({
        'code': 200,
        'message': 'OK'
    })
    # 支持跨域访问
    response['Access-Control-Allow-Origin'] = '*'  # 允许所有IP访问
    return response