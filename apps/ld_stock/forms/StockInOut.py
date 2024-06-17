from django import forms
from ..models import StockBill
from org_com.models import Company
class StockInOutForm(forms.ModelForm):
    def __init__(self, facility_id, stock_type,  *args, **kwargs):
        self.facility_id = facility_id  # 出入库单工厂所属
        self.stock_type = stock_type    # 订单区分1：入库单 0： 出库单
        super(StockInOutForm, self).__init__(*args, **kwargs)
    class Meta:
        model = StockBill
        fields = ['id', 'bill_no', 'bill_type', 'bill_date', 'in_out_type', 'in_out_by', 'facility',]
        labels = {
            'bill_no': '单号',
            'bill_type': '类型',
            'bill_date': '日期',
            'in_out_type': '出入库类型',
            'in_out_by': '操作人员',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'bill_no': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'bill_type': forms.Select(attrs={'class': 'form-control'}),
            'bill_date': forms.TextInput(attrs={'class': 'form-control'}),
            'in_out_type': forms.Select(attrs={'class': 'form-control'}),
            'in_out_by': forms.TextInput(attrs={'class': 'form-control'}),
            'facility': forms.HiddenInput(),
        }
    def clean(self):
        data = super().clean()