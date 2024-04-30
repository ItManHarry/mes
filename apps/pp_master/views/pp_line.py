from django.views import View
from django.shortcuts import render, reverse, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import ProductLine
from mes.sys.decorators import check_menu_used
from ..forms import ProductLineForm
from django.core.paginator import Paginator
from django.conf import settings
from django.utils import timezone
class ProductLineIndexView(View):
    template_name = 'pp_master/pp_line/index.html'
    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP001'))
    def get(self, request):
        lines = ProductLine.objects.all().order_by('code')
        paginator = Paginator(lines, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(lines=page.object_list, page=page))

class ProductLineAddView(View):
    form_class = ProductLineForm
    template_name = 'pp_master/pp_line/edit.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        form = self.form_class(company_id)
        return render(request, self.template_name, dict(form=form))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        form = self.form_class(company_id, request.POST)
        if form.is_valid():
            line = form.save(commit=False)
            line.code = line.code.upper().strip()
            user = request.user
            if user:
                line.created_by = user.id
            line.save()
            return redirect(reverse('pp_master:lines'))
        return render(request, self.template_name, dict(form=form))
class ProductLineEditView(View):
    form_class = ProductLineForm
    template_name = 'pp_master/pp_line/edit.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        line = ProductLine.objects.get(pk=kwargs['line_id'])
        form = self.form_class(company_id, instance=line)
        return render(request, self.template_name, dict(form=form))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        line = ProductLine.objects.get(pk=kwargs['line_id'])
        form = self.form_class(company_id, request.POST, instance=line)
        if form.is_valid():
            line = form.save(commit=False)
            line.code = line.code.upper().strip()
            line.updated_on = timezone.now()
            user = request.user
            if user:
                line.updated_by = user.id
            line.save()
            return redirect(reverse('pp_master:lines'))
        return render(request, self.template_name, dict(form=form))
@login_required
def get_lines_by_facility(request, facility_id):
    if facility_id == '000000000':
        lines = ProductLine.objects.none()
    else:
        lines = ProductLine.objects.filter(company_id=facility_id).order_by('code')
    return render(request, 'pp_master/pp_line/_lines.html', context=dict(lines=lines))