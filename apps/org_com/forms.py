from django.forms import ModelForm
from django.db.models import Q
from django import forms
from .models import Company
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['id', 'name', 'code']
        labels = {
            'code': '公司代码',
            'name': '公司名称',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        code_exist = False      # 公司代码是否存在
        try:
            company = Company.objects.get(pk=id)
        except:
            company = None
        if company:
            if Company.objects.filter(~Q(id=id) & Q(code=code.upper())):
                code_exist = True
        else:
            if Company.objects.filter(code=code.upper()):
                code_exist = True
        if code_exist:
            self.add_error('code', '公司代码已存在!')