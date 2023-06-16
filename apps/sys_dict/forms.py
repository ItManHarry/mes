from django.forms import ModelForm
from django.db.models import Q
from django import forms
from .models import SysDict, SysEnum
from django.core.exceptions import ValidationError
class SysDictForm(ModelForm):
    class Meta:
        model = SysDict
        fields = ['name', 'code', 'id']
        labels = {
            'code': '字典代码',
            'name': '字典名称',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'id': forms.HiddenInput(),
        }
    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        code_exist = False      # 字典代码是否存在
        try:
            work_book = SysDict.objects.get(pk=id)
        except:
            work_book = None
        if work_book:
            if SysDict.objects.filter(~Q(id=id) & Q(code=code.upper())):
                code_exist = True
        else:
            if SysDict.objects.filter(code=code.upper()):
                code_exist = True
        if code_exist:
            self.add_error('code', '字典代码已存在!')

class SysEnumForm(ModelForm):

    def __init__(self, dict_id, *args, **kwargs):
        self.dict_id = dict_id
        super(SysEnumForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SysEnum
        fields = ['id', 'name', 'code']
        labels = {
            'code': '枚举代码',
            'name': '枚举名称',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_code(self):
        id = self.cleaned_data['id']
        code = self.cleaned_data['code']
        # print('Dict id is : ', self.dict_id, ', enum code is : ', code)
        try:
            enum = SysEnum.objects.get(pk=id)
        except:
            enum = None
        code_exist = False
        if enum:
            if SysEnum.objects.filter(~Q(id=id) & Q(sys_dict_id=self.dict_id) & Q(code=code.lower())):
                code_exist = True
        else:
            if SysEnum.objects.filter(Q(sys_dict_id=self.dict_id) & Q(code=code.lower())):
                code_exist = True
        if code_exist:
            raise ValidationError('枚举代码已存在！')
        return code