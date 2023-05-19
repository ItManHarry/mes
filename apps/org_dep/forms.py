from django.forms import ModelForm
from django.db.models import Q
from django import forms
from .models import Department
from org_com.models import Company
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
            'company': forms.Select(attrs={'class': 'form-control'}, choices=[(company.id, company.name) for company in Company.objects.all()]),
            'parent': forms.Select(attrs={'class': 'form-control'}, choices=[(department.id, department.name) for department in Department.objects.all().order_by('code')]),
        }

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        company = cleaned_data['company']
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