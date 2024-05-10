from django.urls import path
from .views import ProductLineIndexView, ProductLineAddView, ProductLineEditView, ProductWorkCenterAddView, ProductWorkCenterEditView, ProductWorkCenterIndexView, get_lines_by_facility, get_workcenters_by_facility
from .views.pp_machinecode import MachineCodeIndexView, MachineCodeAddView, MachineCodeEditView, get_machinecodes_by_facility
from .views.pp_modelcode import ModelCodeIndexView, ModelCodeAddView, ModelCodeEditView
app_name = 'pp_master'
urlpatterns = [
    path('line/index/', ProductLineIndexView.as_view(), name='lines'),
    path('line/add/', ProductLineAddView.as_view(), name='line_add'),
    path('line/edit/<line_id>/', ProductLineEditView.as_view(), name='line_edit'),
    path('line/get/<facility_id>', get_lines_by_facility, name='get_lines_by_facility'),
    path('work_center/index/', ProductWorkCenterIndexView.as_view(), name='workcenters'),
    path('work_center/add/', ProductWorkCenterAddView.as_view(), name='workcenter_add'),
    path('work_center/edit/<workcenter_id>/', ProductWorkCenterEditView.as_view(), name='workcenter_edit'),
    path('work_center/get/<facility_id>', get_workcenters_by_facility, name='get_workcenters_by_facility'),
    path('machine_code/index/', MachineCodeIndexView.as_view(), name='machinecodes'),
    path('machine_code/add/', MachineCodeAddView.as_view(), name='machinecode_add'),
    path('machine_code/edit/<machinecode_id>/', MachineCodeEditView.as_view(), name='machinecode_edit'),
    path('machine_code/get/<facility_id>', get_machinecodes_by_facility, name='get_machinecodes_by_facility'),
    path('model_code/index/', ModelCodeIndexView.as_view(), name='modelcodes'),
    path('model_code/add/', ModelCodeAddView.as_view(), name='modelcode_add'),
    path('model_code/edit/<modelcode_id>/', ModelCodeEditView.as_view(), name='modelcode_edit'),
]