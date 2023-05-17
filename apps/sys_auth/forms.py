from django.forms import ModelForm
from django.db.models import Q
from django import forms
from .models import Role, Menu
from org_com.models import Company
class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'company']
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
            if Role.objects.filter(Q(code=code.upper()) & Q(company_id=company.id)):
                code_exist = True
        if code_exist:
            self.add_error('code', '角色代码已存在!')
class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['id', 'code', 'name', 'url', 'icon', 'remark']
        labels = {
            'code': '菜单代码',
            'name': '菜单名称',
            'url': '菜单URL',
            'icon': '菜单图标',
            'remark': '备注',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        code_exist = False      # 菜单代码是否存在
        try:
            menu = Menu.objects.get(pk=id)
        except:
            menu = None
        if menu:
            if Menu.objects.filter(~Q(id=id) & Q(code=code.upper())):
                code_exist = True
        else:
            if Menu.objects.filter(code=code.upper()):
                code_exist = True
        if code_exist:
            self.add_error('code', '菜单代码已存在!')