from django import forms
from ..models import OptionBasic, OptionCode
from org_com.models import Company
from django.db.models import Q
class OptionBasicForm(forms.ModelForm):
    def __init__(self, facility_id, *args, **kwargs):
        self.facility_id = facility_id
        super(OptionBasicForm, self).__init__(*args, **kwargs)
        if self.facility_id:
            self.fields['facility'].queryset = Company.objects.filter(id=self.facility_id).order_by('name')
        else:
            self.fields['facility'].queryset = Company.objects.all().order_by('name')
    class Meta:
        model = OptionBasic
        fields = ['id', 'code', 'name', 'sequence', 'use', 'facility']
        labels = {
            'code': 'Option代码',
            'name': 'Option名称',
            'sequence': '顺序号',
            'use': '使用与否',
            'facility': '工厂'
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sequence': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
            'use': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'facility': forms.Select(attrs={'class': 'form-control'})
        }
    def clean(self):
        data = super().clean()
        id = data['id']
        code = data['code']
        facility = data['facility']
        sequence = data['sequence']
        if not facility:
            self.add_error('facility', '请选择工厂！')
        option = OptionBasic.objects.filter(id=id).first()
        if option:
            if OptionBasic.objects.filter(~Q(id=id) & Q(code=code.strip().upper()) & Q(facility=facility)).first():
                self.add_error('code', 'Option代码已存在！')
            if OptionBasic.objects.filter(~Q(id=id) & Q(sequence=sequence) & Q(facility=facility)).first():
                self.add_error('sequence', '顺序号已存在！')
        else:
            if OptionBasic.objects.filter(Q(code=code.strip().upper()) & Q(facility=facility)).first():
                self.add_error('code', 'Option代码已存在！')
            if OptionBasic.objects.filter(Q(sequence=sequence) & Q(facility=facility)).first():
                self.add_error('sequence', '顺序号已存在！')

class OptionCodeForm(forms.ModelForm):
    def __init__(self, facility_id, *args, **kwargs):
        self.facility_id = facility_id
        super(OptionCodeForm, self).__init__(*args, **kwargs)
        if self.facility_id:
            self.fields['option'].queryset = OptionBasic.objects.filter(facility_id=facility_id).order_by('code')
        else:
            self.fields['option'] = OptionBasic.objects.none()
    class Meta:
        model = OptionCode
        fields = ['id', 'code', 'style_code', 'o_sap', 's_sap', 'o_mes', 's_mes', 'basic', 'erp_if', 'sign', 'option']
        labels = {
            'code': 'Option代码',
            'style_code': '式样代码',
            'o_sap': 'Option说明(SAP)',
            's_sap': '式样说明(SAP)',
            'o_mes': 'Option说明(MES)',
            's_mes': '式样说明(MES)',
            'basic': '基本Option',
            'erp_if': 'ERP接口',
            'sign': '详细标识',
            'option': 'Option基本',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'style_code': forms.TextInput(attrs={'class': 'form-control'}),
            'o_sap': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            's_sap': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'o_mes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            's_mes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'basic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'erp_if': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sign': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'option': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        data = super().clean()
        id = data['id']
        code = data['code']
        style_code = data['style_code']
        oc = OptionCode.objects.filter(id=id).first()
        if oc:
            if OptionCode.objects.filter(~Q(id=id) & Q(code=code.strip().upper()) & Q(style_code=style_code.strip().upper())).first():
                self.add_error('style_code', '式样代码已存在！')
        else:
            if OptionCode.objects.filter(Q(code=code.strip().upper()) & Q(style_code=style_code.strip().upper())).first():
                self.add_error('style_code', '式样代码已存在！')