from django import forms
from .models import UserData, Abiturientus


class ContactForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': "required"
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'required': "required"
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }