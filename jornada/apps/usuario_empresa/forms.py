from typing import Any, Dict
from django import forms
from django.utils import timezone
from .models import UsuarioEmpresa
from dominios.models import TipoSaidaUnidade
from core.forms.widgets import CustomAttachmentInput, CustomSplitDateTimeWidget
from core.forms.mixins import PreencheProcessoPorAdolescenteMixin, LabelProcessoSemNomeMixin
from adolescentes.models import Adolescente

class UsuarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = UsuarioEmpresa



