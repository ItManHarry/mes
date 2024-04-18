from django import forms
from django.forms import ValidationError
class ExcelImportForm(forms.Form):
    file = forms.FileField(label='Excel文件', required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            print('File name is : ', file.name)
            file_extend = file.name.split('.')[1]
            if file_extend not in ['xls', 'xlsx', 'csv']:
                raise ValidationError('文件扩展名必须是(xls,xlsx,csv)')
        return file