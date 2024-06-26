from django import forms
from ..models import ProductLine, ProductWorkCenter
from org_com.models import Company
from sys_dict.models import SysEnum
from django.db.models import Q

class ProductWorkCenterForm(forms.ModelForm):
    def __init__(self, company_id, *args, **kwargs):
        self.company_id = company_id
        super(ProductWorkCenterForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = SysEnum.objects.filter(Q(sys_dict__code='D002') & ~Q(code='000')).all().order_by('code')
        if self.company_id:
            self.fields['facility'].queryset = Company.objects.filter(id=self.company_id).order_by('name')
        else:
            self.fields['facility'].queryset = Company.objects.all().order_by('name')
        instance = ProductWorkCenter.objects.filter(id=self.instance.pk).first()
        if instance:    # 编辑
            self.fields['line'].queryset = self.instance.facility.product_lines.order_by('code')
            self.fields['start_wc'].queryset = self.instance.line.work_centers.order_by('code') if self.instance.line else ProductWorkCenter.objects.none()
            self.fields['end_wc'].queryset = self.instance.line.work_centers.order_by('code') if self.instance.line else ProductWorkCenter.objects.none()
        else:           # 新增
            self.fields['line'].queryset = ProductLine.objects.none()
            self.fields['start_wc'].queryset = ProductWorkCenter.objects.none()
            self.fields['end_wc'].queryset = ProductWorkCenter.objects.none()
        # Ajax切换工厂后保存产线时使用,否则报错
        if 'facility' in self.data:
            self.fields['line'].queryset = ProductLine.objects.filter(company_id=self.data['facility']).order_by('code')
        if 'line' in self.data:
            self.fields['start_wc'].queryset = ProductWorkCenter.objects.filter(line_id=self.data['line']).order_by('code')
            self.fields['end_wc'].queryset = ProductWorkCenter.objects.filter(line_id=self.data['line']).order_by('code')
    class Meta:
        model = ProductWorkCenter
        fields = ['id', 'name', 'code', 'category', 'facility', 'line', 'to_track', 'to_sap', 'start_wc', 'end_wc']
        labels = {
            'code': '作业场代码',
            'name': '作业场名称',
            'category': '区分',
            'facility': '工厂',
            'line': '产线',
            'to_track': '追溯性传送',
            'to_sap': 'SAP实绩传送',
            'start_wc': '开始作业场',
            'end_wc': '结束作业场',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'facility': forms.Select(attrs={'class': 'form-select'}),
            'line': forms.Select(attrs={'class': 'form-select'}),
            'to_track': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'to_sap': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'start_wc': forms.Select(attrs={'class': 'form-select'}),
            'end_wc': forms.Select(attrs={'class': 'form-select'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        facility = cleaned_data['facility']
        if not facility:
            self.add_error('facility', '请选择工厂！')
        workcenter = ProductWorkCenter.objects.filter(id=id).first()
        if workcenter:    # 编辑
            if ProductWorkCenter.objects.filter(~Q(id=id) & Q(code=code.upper().strip()) & Q(facility=facility)).all():
                self.add_error('code', '作业场代码已存在！')
        else:       # 新增
            if ProductWorkCenter.objects.filter(Q(code=code.upper().strip()) & Q(facility=facility)).all():
                self.add_error('code', '作业场代码已存在！')