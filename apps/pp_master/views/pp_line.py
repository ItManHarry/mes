from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, reverse, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import ProductLine
class ProductLineIndexView(LoginRequiredMixin, ListView):
    model = ProductLine
    template_name = 'pp_master/pp_line/index.html'
    context_object_name = 'lines'