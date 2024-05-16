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
        fields = ['id', 'code', 'style_code', 'o_remark', 's_remark', 'facility']
        labels = {
            'code': 'Option代码',
            'style_code': '式样代码',
            'o_remark': 'Option说明(MES)',
            's_remark': '式样说明(MES)',
            'facility': '工厂'
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'style_code': forms.TextInput(attrs={'class': 'form-control'}),
            'o_remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            's_remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'facility': forms.Select(attrs={'class': 'form-control'})
        }
    def clean(self):
        data = super().clean()
        id = data['id']
        code = data['code']
        style_code = data['style_code']
        facility = data['facility']
        if not facility:
            self.add_error('facility', '请选择工厂！')
        option = OptionBasic.objects.filter(id=id).first()
        if option:
            if OptionBasic.objects.filter(~Q(id=id)
                                          & Q(code=code.strip().upper())
                                          & Q(style_code=style_code.strip().upper())
                                          & Q(facility=facility)).first():
                self.add_error('style_code', '式样代码已存在！')
        else:
            if OptionBasic.objects.filter(Q(code=code.strip().upper())
                                          & Q(style_code=style_code.strip().upper())
                                          & Q(facility=facility)).first():
                self.add_error('style_code', '式样代码已存在！')

class OptionCodeForm(forms.ModelForm):
    pass