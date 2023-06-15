"""
URL configuration for mes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .sys import views

urlpatterns = [
    path('', views.root, name='root'),
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('func/', views.func, name='func'),
    path('sys_sign/', include('sys_sign.urls')),
    path('org_com/', include('org_com.urls')),
    path('org_dep/', include('org_dep.urls')),
    path('org_emp/', include('org_emp.urls')),
    path('sys_auth/', include('sys_auth.urls')),
    path('sys_dict/', include('sys_dict.urls')),
]