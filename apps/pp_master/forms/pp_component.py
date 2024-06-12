from django import forms
from ..models import Component
from django.db.models import Q
class ComponentForm(forms.ModelForm):
    def __init__(self, facility_id, *args, **kwargs):
        self.facility_id = facility_id
        super(ComponentForm, self).__init__(*args, **kwargs)
        self.facility_id['facility'].initial = facility_id
    class Meta:
        model = Component
        fields = ['id', 'code', 'name', 'safe_storage', 'facility']
        labels = {
            'code': '品号',
            'name': '品名',
            'safe_storage': '安全库存',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'facility': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'safe_storage': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        data = super().clean()
        id = data['id']
        code = data['code']
        component = Component.objects.filter(id=id).first()
        if component:
            if Component.objects.filter(~Q(id=id) & Q(code=code.strip().upper()) & Q(facility=self.facility_id)).first():
                self.add_error('code', '品号已存在！')
        else:
            if Component.objects.filter(Q(code=code.strip().upper()) & Q(facility=self.facility_id)).first():
                self.add_error('code', '品号已存在！')