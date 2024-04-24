from django.urls import path
from .views import ProductLineIndexView, ProductLineAddView, ProductLineEditView, ProductWorkCenterAddView, ProductWorkCenterEditView, ProductWorkCenterIndexView
app_name = 'pp_master'
urlpatterns = [
    path('line/index/', ProductLineIndexView.as_view(), name='lines'),
    path('line/add/', ProductLineAddView.as_view(), name='line_add'),
    path('line/edit/<line_id>/', ProductLineEditView.as_view(), name='line_edit'),
    path('work_center/index/', ProductWorkCenterIndexView.as_view(), name='workcenters'),
    path('work_center/add/', ProductWorkCenterAddView.as_view(), name='workcenter_add'),
    path('work_center/edit/<work_center_id>/', ProductWorkCenterEditView.as_view(), name='workcenter_edit'),
]