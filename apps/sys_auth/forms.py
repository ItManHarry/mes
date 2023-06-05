from django.forms import ModelForm
from django.db.models import Q
from django import forms
from .models import Role, Menu
from sys_auth.models import Role
from org_com.models import Company
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class RoleForm(ModelForm):

    def __init__(self, company_id, *args, **kwargs):
        self.company_id = company_id
        super(RoleForm, self).__init__(*args, **kwargs)
        # 设置法人
        if self.company_id:
            self.fields['company'].queryset = Company.objects.filter(id=self.company_id).order_by('name')
        else:
            self.fields['company'].queryset = Company.objects.all().order_by('name')

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
            'company': forms.Select(attrs={'class': 'form-control'}),
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
class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields['roles'].choices = [(role.id, role.name) for role in Role.objects.all().order_by('code')]
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    is_staff = forms.BooleanField(label='全职雇员', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), initial=True, required=False)
    # is_superuser = forms.BooleanField(label='超级管理员', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), initial=False, required=False)
    username = forms.CharField(label='账号', max_length=24, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}), required=True)
    name = forms.CharField(label='姓名', max_length=24, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}), required=True)
    password = forms.CharField(label='密码', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    email = forms.EmailField(label='电子邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    employee = forms.CharField(label='雇员', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}), required=False)
    employee_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    # roles = forms.ChoiceField(label='角色', widget=forms.Select(attrs={'class': 'form-control'}), choices=[(role.id, role.name) for role in Role.objects.all().order_by('code')])

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.cleaned_data['id']:
            id = int(self.cleaned_data['id'])
            if User.objects.filter(~Q(id=id) & Q(username=username.upper())):
                raise ValidationError('用户已存在！')
        else:
            print('Add user')
            if User.objects.filter(username=username.upper()):
                raise ValidationError('用户已存在！')
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        # 新增时校验密码是否输入
        if not self.cleaned_data['id']:
            if not password.strip():
                raise ValidationError('请输入密码！')
        return password