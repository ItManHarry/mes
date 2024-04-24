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
    pass
class ProductWorkCenterEditView(View):
    pass