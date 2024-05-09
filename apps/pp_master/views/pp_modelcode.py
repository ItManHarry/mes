from django.views import View
from django.shortcuts import redirect, reverse, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator
from ..forms.pp_machinecode import ModelCodeForm
from ..models import ModelCode
from mes.sys.decorators import check_menu_used
class ModelCodeIndexView(View):
    template_name = 'pp_master/pp_modelcode/index.html'
    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP004'))
    def get(self, request):
        mcs = ModelCode.objects.all().order_by('code')
        paginator = Paginator(mcs, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(modelcodes=page.object_list, page=page))
class ModelCodeAddView(View):
    template_name = 'pp_master/pp_modelcode/edit.html'
    form_class = ModelCodeForm
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
            modelcode = form.save(commit=False)
            modelcode.code = modelcode.code.upper().strip()
            user = request.user
            if user:
                modelcode.created_by = user.id
            modelcode.save()
            return redirect(reverse('pp_master:modelcodes'))
        return render(request, self.template_name, dict(form=form))
class ModelCodeEditView(View):
    template_name = 'pp_master/pp_modelcode/edit.html'
    form_class = ModelCodeForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        modelcode = ModelCode.objects.get(pk=kwargs['modelcode_id'])
        form = self.form_class(company_id, instance=modelcode)
        return render(request, self.template_name, dict(form=form))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        modelcode = ModelCode.objects.get(pk=kwargs['modelcode_id'])
        form = self.form_class(company_id, request.POST, instance=modelcode)
        if form.is_valid():
            modelcode = form.save(commit=False)
            modelcode.code = modelcode.code.upper().strip()
            user = request.user
            if user:
                modelcode.updated_by = user.id
            modelcode.updated_on = timezone.now()
            modelcode.save()
            return redirect(reverse('pp_master:modelcodes'))
        return render(request, self.template_name, dict(form=form))
# @login_required
# def get_workcenters_by_facility(request, facility_id):
#     if facility_id == '000000000':
#         workcenters = MachineCode.objects.none()
#     else:
#         workcenters = MachineCode.objects.filter(facility_id=facility_id).order_by('code')
#     return render(request, 'pp_master/pp_modelcode/_workcenters.html', context=dict(workcenters=workcenters))