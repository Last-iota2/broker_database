from django import forms
from .models import ArrayData

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = ArrayData
        fields = ('array_data',)