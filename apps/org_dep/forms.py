from django.forms import ModelForm
from django.db.models import Q
from django import forms
from .models import Department
from django.core.exceptions import ValidationError
class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'company', 'parent']
        labels = {
            'code': '部门代码',
            'name': '部门名称',
            'company': '公司所属',
            'parent': '上级部门',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        company = cleaned_data['company']
        print('ID : {}, code : {} company : {}.'.format(id, code, company))
        code_exist = False  # 部门代码是否存在
        try:
            department = Department.objects.get(pk=id)
        except:
            department = None
        if department:
            print('Department is : ', department, ', company id is : ', company.id)
            if Department.objects.filter(~Q(id=id) & Q(code=code.upper()) & Q(company_id=company.id)):
                code_exist = True
        else:
            if Department.objects.filter(Q(code=code.upper()) & Q(company_id=company.id)):
                code_exist = True
        if code_exist:
            self.add_error('code', '部门代码已存在!')
    def clean_parent(self):
        id = self.cleaned_data['id']
        parent = self.cleaned_data['parent']
        company = self.cleaned_data['company']
        print('Parent id is : ', parent.id, ', self id is : ', id, ', company is :', company.id)
        if parent.id == id:
            raise ValidationError('上级部门不能选择自身!')
        return parent