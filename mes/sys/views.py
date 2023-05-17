from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
def root(request):
    return redirect(reverse('sys_sign:login'))
def index(request):
    return render(request, 'index.html', context=dict(login_message=''))
def home(request):
    return render(request, 'home.html')