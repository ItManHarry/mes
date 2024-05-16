from django.shortcuts import redirect, render, reverse
from django.views import View
from django.utils import timezone
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from mes.sys.decorators import check_menu_used
from django.core.paginator import Paginator
from ..forms.pp_option import OptionBasicForm, OptionCodeForm
class OptionBasicIndexView(View):
    pass
class OptionBasicAddView(View):
    pass
class OptionBasicEditView(View):
    pass
class OptionCodeIndexView(View):
    pass
class OptionCodeAddView(View):
    pass
class OptionCodeEditView(View):
    pass