from django.views import View
from django.shortcuts import render, reverse, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import ProductLine
from mes.sys.decorators import check_menu_used
from ..forms import ProductLineForm
class ProductLineIndexView(View):
    template_name = 'pp_master/pp_line/index.html'
    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP001'))
    def get(self, request):
        lines = ProductLine.objects.all()
        return render(request, self.template_name, dict(lines=lines))

class ProductLineAddView(View):
    form_class = ProductLineForm
    template_name = 'pp_master/pp_line/edit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, dict(form=form))

class ProductLineEditView(View):
    pass