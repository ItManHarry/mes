from django.forms import ModelForm
from django.db.models import Q
from django import forms
from .models import Role, Menu
from org_com.models import Company
class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'code', 'id', 'company']
        labels = {
            'code': '角色代码',
            'name': '角色名称',
            'company': '法人所属',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}, choices=[(company.id, company.name) for company in Company.objects.all()]),
        }

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        company = cleaned_data['company']
        code_exist = False      # 角色代码是否存在
        try:
            role = Role.objects.get(pk=id)
        except:
            role = None
        if role:
            print('Role is : ', role, ', company id is : ', company.id)
            if Role.objects.filter(~Q(id=id) & Q(code=code.upper()) & Q(company_id=company.id)):
                code_exist = True
        else:
            if Role.objects.filter(code=code.upper()):
                code_exist = True
        if code_exist:
            self.add_error('code', '角色代码已存在!')