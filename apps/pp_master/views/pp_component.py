from django.views import View
from django.shortcuts import render, reverse, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import Component
from mes.sys.decorators import check_menu_used
from ..forms import ComponentForm
from django.core.paginator import Paginator
from django.conf import settings
from django.utils import timezone
class ComponentIndexView(View):
    template_name = 'pp_master/pp_component/index.html'
    @method_decorator(login_required)
    @method_decorator(check_menu_used('PP008'))
    def get(self, request):
        components = Component.objects.all().order_by('code')
        paginator = Paginator(components, settings.PAGE_ITEMS)
        page_num = request.GET.get('page', 1)
        page = paginator.page(page_num)
        return render(request, self.template_name, dict(components=page.object_list, page=page))
class ComponentAddView(View):
    form_class = ComponentForm
    template_name = 'pp_master/pp_component/edit.html'
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
            component = form.save(commit=False)
            component.code = component.code.upper().strip()
            user = request.user
            if user:
                component.created_by = user.id
            component.save()
            return redirect(reverse('pp_master:components'))
        return render(request, self.template_name, dict(form=form))
class ComponentEditView(View):
    form_class = ComponentForm
    template_name = 'pp_master/pp_component/edit.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        component = Component.objects.get(pk=kwargs['component_id'])
        form = self.form_class(facility_id, instance=component)
        return render(request, self.template_name, dict(form=form))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        facility_id = request.session['company_id']
        component = Component.objects.get(pk=kwargs['component_id'])
        form = self.form_class(facility_id, request.POST, instance=component)
        if form.is_valid():
            component = form.save(commit=False)
            component.code = component.code.upper().strip()
            component.updated_on = timezone.now()
            user = request.user
            if user:
                component.updated_by = user.id
            component.save()
            return redirect(reverse('pp_master:components'))
        return render(request, self.template_name, dict(form=form))