from django import forms
from .models import Employee
from django.db.models import Q
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):
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