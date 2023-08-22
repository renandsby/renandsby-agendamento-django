from django import forms
from .models import UnidadeDeApoio
from core.forms.mixins import (
    UfCidadeBairroMixin
)


       
class UnidadeDeApoioForm(UfCidadeBairroMixin, forms.ModelForm):
    class Meta:
        model = UnidadeDeApoio
        fields = "__all__"
