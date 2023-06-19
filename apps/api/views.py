from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
@csrf_exempt
def test(request):
    print('Test the api , method is : ', request.method)
    return JsonResponse({
        'code': 200,
        'message': 'OK'
    })