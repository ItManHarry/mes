from django import forms
from .models import ProductLine, ProductWorkCenter
from org_com.models import Company
from sys_dict.models import SysEnum
from django.db.models import Q
class ProductLineForm(forms.ModelForm):
    def __init__(self, company_id, *args, **kwargs):
        self.company_id = company_id
        super(ProductLineForm, self).__init__(*args, **kwargs)
        if self.company_id:
            self.fields['company'].query_set = Company.objects.filter(id=self.company_id).order_by('name')
        else:
            self.fields['company'].query_set = Company.objects.all().order_by('name')
    class Meta:
        model = ProductLine
        fields = ['id', 'name', 'code', 'version', 'company']
        labels = {
            'code': '线号',
            'name': '名称',
            'version': '版本',
            'company': '工厂',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        company = cleaned_data['company']
        if not company:
            self.add_error('company', '请选择工厂！')
        line = ProductLine.objects.filter(id=id).first()
        if line:    # 编辑
            if ProductLine.objects.filter(~Q(id=id) & Q(code=code.upper()) & Q(company=company)).all():
                self.add_error('code', '线号已存在！')
        else:       # 新增
            if ProductLine.objects.filter(Q(code=code.upper()) & Q(company=company)).all():
                self.add_error('code', '线号已存在！')
class ProductWorkCenterForm(forms.ModelForm):
    def __init__(self, company_id, *args, **kwargs):
        self.company_id = company_id
        super(ProductWorkCenterForm, self).__init__(*args, **kwargs)
        self.fields['category'].query_set = SysEnum.objects.filter(Q(sys_dict__code='D002') & ~Q(code='000')).all().order_by('code')
        if self.company_id:
            self.fields['facility'].query_set = Company.objects.filter(id=self.company_id).order_by('name')
        else:
            self.fields['facility'].query_set = Company.objects.all().order_by('name')
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
            'category': forms.Select(attrs={'class': 'form-control'}),
            'facility': forms.Select(attrs={'class': 'form-control'}),
            'line': forms.Select(attrs={'class': 'form-control'}),
            'to_track': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'to_sap': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'start_wc': forms.Select(attrs={'class': 'form-control'}),
            'end_wc': forms.Select(attrs={'class': 'form-control'}),
        }