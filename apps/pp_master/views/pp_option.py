from django.shortcuts import redirect, render, reverse
from django.views import View
from django.utils import timezone
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from mes.sys.decorators import check_menu_used
from django.core.paginator import Paginator
from ..forms.pp_option import OptionBasicForm, OptionCodeForm
from ..models.pp_option import OptionBasic, OptionCode
class OptionBasicIndexView(View):
    template_name = 'pp_master/pp_option/basic/index.html'
    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP005'))
    def get(self, request):
        all = OptionBasic.objects.all().order_by('code')
        paginator = Paginator(all, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(options=page.object_list, page=page))

class OptionBasicAddView(View):
    template_name = 'pp_master/pp_option/basic/edit.html'
    form_class = OptionBasicForm
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        form = self.form_class(facility_id)
        return render(request, self.template_name, dict(form=form))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        form = self.form_class(facility_id, request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.code = option.code.upper().strip()
            user = request.user
            if user:
                option.created_by = user.id
            option.save()
            return redirect(reverse('pp_master:option_basics'))
        return render(request, self.template_name, dict(form=form))
class OptionBasicEditView(View):
    template_name = 'pp_master/pp_option/basic/edit.html'
    form_class = OptionBasicForm
    def get(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        option = OptionBasic.objects.get(pk=kwargs['option_id'])
        form = self.form_class(facility_id, instance=option)
        return render(request, self.template_name, dict(form=form))
    def post(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        option = OptionBasic.objects.get(pk=kwargs['option_id'])
        form = self.form_class(facility_id, request.POST, instance=option)
        if form.is_valid():
            option = form.save(commit=False)
            option.code = option.code.upper().strip()
            user = request.user
            if user:
                option.updated_by = user.id
            option.updated_on = timezone.now()
            option.save()
            return redirect(reverse('pp_master:option_basics'))
        return render(request, self.template_name, dict(form=form))
class OptionCodeIndexView(View):
    template_name = ''
class OptionCodeAddView(View):
    pass
class OptionCodeEditView(View):
    pass