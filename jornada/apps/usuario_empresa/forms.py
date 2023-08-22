from typing import Any, Dict
from django import forms
from django.utils import timezone
from .models import UsuarioEmpresa
from core.forms.widgets import CustomAttachmentInput, CustomSplitDateTimeWidget


class UsuarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = UsuarioEmpresa
        fields = "__all__"



