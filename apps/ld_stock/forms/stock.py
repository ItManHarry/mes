from django import forms
from ..models import StockBill
from org_com.models import Company
from sys_dict.models import SysEnum
from django.db.models import Q
import uuid
class StockForm(forms.ModelForm):
    def __init__(self, facility_id, stock_type,  *args, **kwargs):
        self.facility_id = facility_id  # 出入库单工厂所属
        self.stock_type = stock_type    # 订单区分1：入库单 2： 出库单
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['in_out_type'].queryset = SysEnum.objects.filter(~Q(code='000') & Q(sys_dict__code='D007')).order_by('code') if self.stock_type == 1 else SysEnum.objects.filter(~Q(code='000') & Q(sys_dict__code='D008')).order_by('code')
    class Meta:
        model = StockBill
        fields = ['id', 'bill_no', 'bill_date', 'in_out_type', 'facility']
        labels = {
            'bill_no': '单号',
            'bill_date': '日期',
            'in_out_type': '出入库类型',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'bill_no': forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'placeholder': '系统自动生成......'}),
            'bill_date': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'in_out_type': forms.Select(attrs={'class': 'form-select'}),
            'facility': forms.HiddenInput(),
        }
    tmp_bill_id = forms.UUIDField(initial=uuid.uuid4, widget=forms.HiddenInput())
    def clean(self):
        data = super().clean()