from django.forms import ModelForm, FileInput
from django import forms
from .models import File


FILE_NAME = 'path'


class FileUploadForm(ModelForm):
    class Meta:
        model = File
        fields = [FILE_NAME]

        widgets = {
            FILE_NAME: forms.FileInput(attrs={
                'class': "file-input",
                'accept': '.txt',
                'id': FILE_NAME,
                'name': FILE_NAME,
                'hidden': True  # This makes the input hidden
            })
        }