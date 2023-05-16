from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html', context=dict(login_message=''))
def home(request):
    return render(request, 'home.html')