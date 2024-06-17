from django.views import View
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from mes.sys.decorators import check_menu_used
class StockInIndexView(View):
    pass
class StockInAddView(View):
    pass
class StockInEditView(View):
    pass
class StockOutIndexView(View):
    pass
class StockOutAddView(View):
    pass
class StockOutEditView(View):
    pass