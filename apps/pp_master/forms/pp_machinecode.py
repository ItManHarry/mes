from django import forms
from ..models import MachineCode
from org_com.models import Company
from sys_dict.models import SysEnum
from django.db.models import Q
class MachineCodeForm(forms.ModelForm):
    def __init__(self, company_id, *args, **kwargs):
        self.company_id = company_id
        super(MachineCodeForm, self).__init__(*args, **kwargs)
        self.fields['pro_quality'].queryset = SysEnum.objects.filter(Q(sys_dict__code='D003') & ~Q(code='000')).all().order_by('code')
        if self.company_id:
            self.fields['facility'].queryset = Company.objects.filter(id=self.company_id).order_by('name')
        else:
            self.fields['facility'].queryset = Company.objects.all().order_by('name')
    class Meta:
        model = MachineCode
        fields = ['id', 'code', 'facility', 'model_sap', 'model_mes', 'pro_group1', 'pro_group2', 'pro_quality', 'finished']
        labels = {
            'code': '机种代码',
            'facility': '工厂',
            'model_sap': '机型(SAP)',
            'model_mes': '机型(MES)',
            'pro_group1': '产品Group1',
            'pro_group2': '产品Group2',
            'pro_quality': '品质产品群',
            'finished': '已结束',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'facility': forms.Select(attrs={'class': 'form-control'}),
            'model_sap': forms.TextInput(attrs={'class': 'form-control'}),
            'model_mes': forms.TextInput(attrs={'class': 'form-control'}),
            'pro_group1': forms.TextInput(attrs={'class': 'form-control'}),
            'pro_group2': forms.TextInput(attrs={'class': 'form-control'}),
            'pro_quality': forms.Select(attrs={'class': 'form-control'}),
            'finished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        model_sap = cleaned_data['model_sap']
        model_mes = cleaned_data['model_mes']
        facility = cleaned_data['facility']
        if not facility:
            self.add_error('facility', '请选择工厂！')
        machinecode = MachineCode.objects.filter(id=id).first()
        if machinecode:    # 编辑
            if MachineCode.objects.filter(~Q(id=id) & Q(code=code.upper().strip()) & Q(facility=facility)).all():
                self.add_error('code', '机种代码已存在！')
            if model_sap:
                if MachineCode.objects.filter(~Q(id=id) & Q(model_sap=model_sap.upper().strip()) & Q(facility=facility)).all():
                    self.add_error('model_sap', '机型(SAP)代码已存在！')
            else:
                self.add_error('model_sap', '机型(SAP)代码不能为空！')
            if model_mes:
                if MachineCode.objects.filter(~Q(id=id) & Q(model_mes=model_mes.upper().strip()) & Q(facility=facility)).all():
                    self.add_error('model_mes', '机型(MES)代码已存在！')
            else:
                self.add_error('model_mes', '机型(MES)代码不能为空！')
        else:       # 新增
            if MachineCode.objects.filter(Q(code=code.upper().strip()) & Q(facility=facility)).all():
                self.add_error('code', '机种代码已存在！')
            if model_sap:
                if MachineCode.objects.filter(Q(model_sap=model_sap.upper().strip()) & Q(facility=facility)).all():
                    self.add_error('model_sap', '机型(SAP)代码已存在！')
            else:
                self.add_error('model_sap', '机型(SAP)代码不能为空！')
            if model_mes:
                if MachineCode.objects.filter(Q(model_mes=model_mes.upper().strip()) & Q(facility=facility)).all():
                    self.add_error('model_mes', '机型(MES)代码已存在！')
            else:
                self.add_error('model_mes', '机型(MES)代码不能为空！')