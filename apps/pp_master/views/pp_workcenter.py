from django.views import View
from django.shortcuts import redirect, reverse, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator
from ..forms import ProductWorkCenterForm
from ..models import ProductWorkCenter
from mes.sys.decorators import check_menu_used
class ProductWorkCenterIndexView(View):
    template_name = 'pp_master/pp_workcenter/index.html'
    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP002'))
    def get(self, request):
        wcs = ProductWorkCenter.objects.all().order_by('code')
        paginator = Paginator(wcs, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(workcenters=page.object_list, page=page))
class ProductWorkCenterAddView(View):
    template_name = 'pp_master/pp_workcenter/edit.html'
    form_class = ProductWorkCenterForm
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
            workcenter = form.save(commit=False)
            workcenter.code = workcenter.code.upper().strip()
            user = request.user
            if user:
                workcenter.created_by = user.id
            workcenter.save()
            return redirect(reverse('pp_master:workcenters'))
        return render(request, self.template_name, dict(form=form))
class ProductWorkCenterEditView(View):
    template_name = 'pp_master/pp_workcenter/edit.html'
    form_class = ProductWorkCenterForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        workcenter = ProductWorkCenter.objects.get(pk=kwargs['workcenter_id'])
        form = self.form_class(company_id, instance=workcenter)
        return render(request, self.template_name, dict(form=form))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        workcenter = ProductWorkCenter.objects.get(pk=kwargs['workcenter_id'])
        form = self.form_class(company_id, request.POST, instance=workcenter)
        if form.is_valid():
            workcenter = form.save(commit=False)
            workcenter.code = workcenter.code.upper().strip()
            user = request.user
            if user:
                workcenter.updated_by = user.id
            workcenter.updated_on = timezone.now()
            workcenter.save()
            return redirect(reverse('pp_master:workcenters'))
        return render(request, self.template_name, dict(form=form))
@login_required
def get_workcenters_by_facility(request, facility_id):
    if facility_id == '000000000':
        workcenters = ProductWorkCenter.objects.none()
    else:
        workcenters = ProductWorkCenter.objects.filter(facility_id=facility_id).order_by('code')
    return render(request, 'pp_master/pp_workcenter/_workcenters.html', context=dict(workcenters=workcenters))