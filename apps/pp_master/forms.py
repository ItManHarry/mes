from django import forms
from .models import ProductLine
class ProductLineForm(forms.ModelForm):
    class Meta:
        model = ProductLine
        fields = ['id', 'name', 'code', 'version', 'company']
        labels = {
            'code': '线号',
            'name': '名称',
            'version': '版本',
            'company': '工厂',
        }
        widgets = {
            'id': forms.HiddenInput(),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
        }