from django.urls import path
from .views import ProductLineIndexView, ProductLineAddView, ProductLineEditView, ProductWorkCenterAddView, ProductWorkCenterEditView, ProductWorkCenterIndexView, get_lines_by_facility, get_workcenters_by_facility
from .views.pp_machinecode import MachineCodeIndexView, MachineCodeAddView, MachineCodeEditView, get_machinecodes_by_facility
from .views.pp_modelcode import ModelCodeIndexView, ModelCodeAddView, ModelCodeEditView
from .views.pp_option import OptionBasicAddView, OptionBasicIndexView, OptionBasicEditView, OptionCodeIndexView, OptionCodeAddView, OptionCodeEditView
from .views.pp_workcenter import get_workcenters_by_line, get_employees, add_employee, remove_employee
from .views.pp_warehouse import WarehousrIndexView, WarehouseAddView, WarehouseEditView
app_name = 'pp_master'
urlpatterns = [
    path('line/index/', ProductLineIndexView.as_view(), name='lines'),
    path('line/add/', ProductLineAddView.as_view(), name='line_add'),
    path('line/edit/<line_id>/', ProductLineEditView.as_view(), name='line_edit'),
    path('line/get/<facility_id>', get_lines_by_facility, name='get_lines_by_facility'),
    path('work_center/index/', ProductWorkCenterIndexView.as_view(), name='workcenters'),
    path('work_center/add/', ProductWorkCenterAddView.as_view(), name='workcenter_add'),
    path('work_center/edit/<workcenter_id>/', ProductWorkCenterEditView.as_view(), name='workcenter_edit'),
    path('work_center/get/facility/<facility_id>', get_workcenters_by_facility, name='get_workcenters_by_facility'),
    path('work_center/get/line/<line_id>', get_workcenters_by_line, name='get_workcenters_by_line'),
    path('work_center/get/employees/<wc_id>', get_employees, name='get_employees'),
    path('work_center/add/employee/<wc_id>/<emp_id>', add_employee, name='add_employee'),
    path('work_center/remove/employee/<wc_id>/<emp_id>', remove_employee, name='remove_employee'),
    path('machine_code/index/', MachineCodeIndexView.as_view(), name='machinecodes'),
    path('machine_code/add/', MachineCodeAddView.as_view(), name='machinecode_add'),
    path('machine_code/edit/<machinecode_id>/', MachineCodeEditView.as_view(), name='machinecode_edit'),
    path('machine_code/get/<facility_id>', get_machinecodes_by_facility, name='get_machinecodes_by_facility'),
    path('model_code/index/', ModelCodeIndexView.as_view(), name='modelcodes'),
    path('model_code/add/', ModelCodeAddView.as_view(), name='modelcode_add'),
    path('model_code/edit/<modelcode_id>/', ModelCodeEditView.as_view(), name='modelcode_edit'),
    path('option/basic/index/', OptionBasicIndexView.as_view(), name='option_basics'),
    path('option/basic/add/', OptionBasicAddView.as_view(), name='option_basic_add'),
    path('option/basic/edit/<option_id>/', OptionBasicEditView.as_view(), name='option_basic_edit'),
    path('option/code/index/', OptionCodeIndexView.as_view(), name='option_codes'),
    path('option/code/add/', OptionCodeAddView.as_view(), name='option_code_add'),
    path('option/code/edit/<option_id>/', OptionCodeEditView.as_view(), name='option_code_edit'),
    path('warehouse/index/', WarehousrIndexView.as_view(), name='warehouses'),
    path('warehouse/add/', WarehouseAddView.as_view(), name='warehouse_add'),
    path('warehouse/edit/<warehouse_id>', WarehouseEditView.as_view(), name='warehouse_edit'),
]