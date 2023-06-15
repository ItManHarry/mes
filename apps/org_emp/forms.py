from django import forms
from .models import Employee
from org_com.models import Company
from org_dep.models import Department
from django.db.models import Q
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):
    def __init__(self, company_id, *args, **kwargs):
        self.company_id = company_id
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # 设置法人
        if self.company_id:
            self.fields['company'].choices = [('000000000', '---------')]+[(company.id, company.name) for company in Company.objects.filter(id=self.company_id).order_by('name')]
        else:
            self.fields['company'].choices = [('000000000', '---------')]+[(company.id, company.name) for company in Company.objects.all().order_by('name')]
        employee_id = self.instance.pk
        try:
            employee = Employee.objects.get(pk=employee_id)
        except:
            employee = None
        if employee:    # 编辑
            self.fields['company'].initial = employee.department.company.id
            company = employee.department.company
            # print('Company is : ', company)
            self.fields['department'].queryset = company.department_set.all()
        else:           # 新增
            self.fields['department'].queryset = Department.objects.none()
        # 前端选择公司Ajax变更上级部门提交时，将对应的上级部门赋值,提交保存时使用
        if 'company' in self.data:
            # print('Selected company is : ', self.data['company'])
            self.fields['department'].queryset = Department.objects.filter(company_id=self.data['company'])
    class Meta:
        model = Employee
        fields = ['id', 'name', 'code', 'email', 'phone', 'department']
        labels = {
            'code': '职号',
            'name': '姓名',
            'email': '电子邮箱',
            'phone': '电话',
            'department': '所属部门',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
    company = forms.ChoiceField(label='所属公司', widget=forms.Select(attrs={'class': 'form-control'}))
    photo = forms.FileField(label='照片', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    def clean_code(self):
        id = self.cleaned_data['id']
        code = self.cleaned_data['code']
        # print('Id is {}, code is {}.'.format(id, code))
        try:
            employee = Employee.objects.get(pk=id)
        except:
            employee = None
        if employee:
            if Employee.objects.filter(~Q(id=id) & Q(code=code.upper())):
                raise ValidationError('职号已存在!')
        else:
            if Employee.objects.filter(code=code.upper()):
                raise ValidationError('职号已存在!')
        return code
    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            print('Photo is : ', photo.name)
            file_extend = photo.name.split('.')[1]
            if file_extend not in ['jpg', 'png', 'gif', 'jpeg']:
                raise ValidationError('文件扩展名必须是(jpg,png,gif,jpeg)')
        return photo