from django.views import View
from django.shortcuts import redirect, reverse, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator
from ..forms import MachineCodeForm
from ..models import MachineCode
from mes.sys.decorators import check_menu_used
class MachineCodeIndexView(View):
    template_name = 'pp_master/pp_machinecode/index.html'
    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP003'))
    def get(self, request):
        mcs = MachineCode.objects.all().order_by('code')
        paginator = Paginator(mcs, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(machinecodes=page.object_list, page=page))
class MachineCodeAddView(View):
    template_name = 'pp_master/pp_machinecode/edit.html'
    form_class = MachineCodeForm
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
            machinecode = form.save(commit=False)
            machinecode.code = machinecode.code.upper()
            user = request.user
            if user:
                machinecode.created_by = user.id
            machinecode.save()
            return redirect(reverse('pp_master:machinecodes'))
        return render(request, self.template_name, dict(form=form))
class MachineCodeEditView(View):
    template_name = 'pp_master/pp_machinecode/edit.html'
    form_class = MachineCodeForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        machinecode = MachineCode.objects.get(pk=kwargs['machinecode_id'])
        form = self.form_class(company_id, instance=machinecode)
        return render(request, self.template_name, dict(form=form))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        company_id = request.session['company_id']
        machinecode = MachineCode.objects.get(pk=kwargs['machinecode_id'])
        form = self.form_class(company_id, request.POST, instance=machinecode)
        if form.is_valid():
            machinecode = form.save(commit=False)
            machinecode.code = machinecode.code.upper()
            user = request.user
            if user:
                machinecode.updated_by = user.id
            machinecode.updated_on = timezone.now()
            machinecode.save()
            return redirect(reverse('pp_master:machinecodes'))
        return render(request, self.template_name, dict(form=form))
# @login_required
# def get_workcenters_by_facility(request, facility_id):
#     if facility_id == '000000000':
#         workcenters = MachineCode.objects.none()
#     else:
#         workcenters = MachineCode.objects.filter(facility_id=facility_id).order_by('code')
#     return render(request, 'pp_master/pp_machinecode/_workcenters.html', context=dict(workcenters=workcenters))