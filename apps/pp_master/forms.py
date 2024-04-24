from django import forms
from .models import ProductLine
from org_com.models import Company
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
    pass