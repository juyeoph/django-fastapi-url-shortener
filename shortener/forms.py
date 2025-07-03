from django import forms
from .models import URL

class URLCreationForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ['original_url']