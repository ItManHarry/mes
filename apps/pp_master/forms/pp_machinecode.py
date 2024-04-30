from django import forms
from ..models import ProductLine, MachineCode
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
        # instance = MachineCode.objects.filter(id=self.instance.pk).first()
        # if instance:    # 编辑
        #     self.fields['line'].queryset = self.instance.facility.product_lines.order_by('code')
        #     self.fields['start_wc'].queryset = self.instance.facility.work_centers.order_by('code')
        #     self.fields['end_wc'].queryset = self.instance.facility.work_centers.order_by('code')
        # else:           # 新增
        #     self.fields['line'].queryset = ProductLine.objects.none()
        #     self.fields['start_wc'].queryset = MachineCode.objects.none()
        #     self.fields['end_wc'].queryset = MachineCode.objects.none()
        # # Ajax切换工厂后保存产线时使用,否则报错
        # if 'facility' in self.data:
        #     self.fields['line'].queryset = ProductLine.objects.filter(company_id=self.data['facility']).order_by('code')
        #     self.fields['start_wc'].queryset = MachineCode.objects.filter(facility_id=self.data['facility']).order_by('code')
        #     self.fields['end_wc'].queryset = MachineCode.objects.filter(facility_id=self.data['facility']).order_by('code')
    class Meta:
        model = MachineCode
        fields = ['id', 'code', 'facility', 'pro_group1', 'pro_group2', 'pro_quality', 'finished']
        labels = {
            'code': '机种代码',
            'facility': '工厂',
            'pro_group1': '产品Group1',
            'pro_group2': '产品Group2',
            'pro_quality': '品质产品群',
            'finished': '已结束',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'facility': forms.Select(attrs={'class': 'form-control'}),
            'pro_group1': forms.TextInput(attrs={'class': 'form-control'}),
            'pro_group2': forms.TextInput(attrs={'class': 'form-control'}),
            'pro_quality': forms.Select(attrs={'class': 'form-control'}),
            'finished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data['id']
        code = cleaned_data['code']
        facility = cleaned_data['facility']
        if not facility:
            self.add_error('facility', '请选择工厂！')
        machinecode = MachineCode.objects.filter(id=id).first()
        if machinecode:    # 编辑
            if MachineCode.objects.filter(~Q(id=id) & Q(code=code.upper()) & Q(facility=facility)).all():
                self.add_error('code', '机种代码已存在！')
        else:       # 新增
            if MachineCode.objects.filter(Q(code=code.upper()) & Q(facility=facility)).all():
                self.add_error('code', '机种代码已存在！')