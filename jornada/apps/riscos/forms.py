from django import forms
from .models import Risco
from django.utils import timezone

class RiscoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['data_registro'] = timezone.now
        

    class Meta:
        model = Risco
        exclude = ("adolescente",)
        