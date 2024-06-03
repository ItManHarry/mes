from django import forms
from ..models import Warehouse, Location
from org_com.models import Company
from django.db.models import Q
class WarehouseForm(forms.ModelForm):
    def __init__(self, facility_id, *args, **kwargs):
        self.facility_id = facility_id
        super(WarehouseForm, self).__init__(*args, **kwargs)
        if self.facility_id:
            self.fields['facility'].queryset = Company.objects.filter(id=self.facility_id).order_by('name')
        else:
            self.fields['facility'].queryset = Company.objects.all().order_by('name')
    class Meta:
        model = Warehouse
        fields = ['id', 'code', 'name', 'address', 'facility']
        labels = {
            'code': '仓库代码',
            'name': '仓库名称',
            'address': '仓库地点',
            'facility': '所属工厂',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'facility': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        data = super().clean()
        id = data['id']
        code = data['code']
        facility = data['facility']
        warehouse = Warehouse.objects.filter(id=id).first()
        if warehouse:   # 编辑
            if Warehouse.objects.filter(~Q(id=id) & Q(code=code.strip().upper()) & Q(facility=facility)).first():
                self.add_error('code', '仓库代码已存在！')
        else:           # 新增
            if Warehouse.objects.filter(Q(code=code.strip().upper()) & Q(facility=facility)).first():
                self.add_error('code', '仓库代码已存在！')