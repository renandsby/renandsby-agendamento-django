from django import forms
from .models import RedeDeLocalizacao
from core.forms.mixins import (
    UfCidadeBairroMixin
)


       
class RedeDeLocalizacaoForm(UfCidadeBairroMixin, forms.ModelForm):
    class Meta:
        model = RedeDeLocalizacao
        fields = "__all__"
