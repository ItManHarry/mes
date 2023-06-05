from django.forms import ModelForm
from django.db.models import Q
from django import forms
from .models import Department
from org_com.models import Company
from django.core.exceptions import ValidationError
'''
递归获取子部门
'''
def get_sub_departments(parent_id, sub_departments):
    departments = Department.objects.filter(parent_id=parent_id)
    if departments:
        for department in departments:
            sub_departments.append(department.id)
            # 递归
            get_sub_departments(department.id, sub_departments)
    else:
        return sub_departments
class DepartmentForm(ModelForm):
    def __init__(self, company_id, *args, **kwargs):
        self.company_id = company_id
        super(DepartmentForm, self).__init__(*args, **kwargs)
        # 设置法人
        if self.company_id:
            self.fields['company'].queryset = Company.objects.filter(id=self.company_id).order_by('name')
        else:
            self.fields['company'].queryset = Company.objects.all().order_by('name')
        # 设置上级部门
        department_id = self.instance.pk
        try:
            department = Department.objects.get(pk=department_id)
        except:
            department = None
        if department:
            # 编辑时剔除自身及子部门(递归)
            sub_ids = [department_id]
            get_sub_departments(department_id, sub_ids)
            self.fields['parent'].queryset = self.instance.company.department_set.filter(
                ~Q(id=department_id) & ~Q(parent_id__in=sub_ids)).order_by('code')
        else:
            self.fields['parent'].queryset = Department.objects.none()
        # 前端选择公司Ajax变更上级部门提交时，将对应的上级部门赋值,提交保存时使用
        if 'company' in self.data:
            # print('Selected company is : ', self.data['company'])
            self.fields['parent'].queryset = Department.objects.filter(company_id=self.data['company'])
    # def __init__(self, p_id, *args, **kwargs):
    #     self.p_id = p_id
    #     super(DepartmentForm, self).__init__(*args, **kwargs)
    #     if self.p_id:
    #         # 上级部门剔除自身及所有下级部门-递归获取子子部门
    #         sub_ids = [self.p_id]
    #         self.get_sub_ids(self.p_id, sub_ids)
    #         # print('Sub ids are >>>>>>>>>>>>', sub_ids)
    #         self.fields['parent'].queryset = Department.objects.filter(~Q(id=self.p_id) & ~Q(parent_id__in=sub_ids))
    # def get_sub_ids(self, parent_id, sub_ids):
    #     # print('ID is >>>>>>>>>>>>>>>>>>>>>>>', parent_id)
    #     departments = Department.objects.filter(parent_id=parent_id)
    #     if departments:
    #         for department in departments:
    #             sub_ids.append(department.id)
    #             # 递归
    #             self.get_sub_ids(department.id, sub_ids)
    #     else:
    #         return sub_ids
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
        if parent and parent.id == id:
            raise ValidationError('上级部门不能选择自身!')
        return parent