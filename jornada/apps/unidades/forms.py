from typing import Any, Dict
from django import forms
from django.utils import timezone
from .models import Unidade, Modulo, Quarto
from core.forms.widgets import CustomAttachmentInput, CustomSplitDateTimeWidget


class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        exclude = ("vagas",)


class ModuloLabelMixin:
    @staticmethod
    def modulo_label_from_instance(self):
        return str(self.descricao)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'modulo' in self.fields:
            self.fields['modulo'].label_from_instance = self.modulo_label_from_instance


class QuartoLabelMixin:
    @staticmethod
    def quarto_label_from_instance(self):
        label = str(self.numero)
        if self.nome is not None:
            label += str(self.nome)
        return label

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'quarto' in self.fields:
            self.fields['quarto'].label_from_instance = self.quarto_label_from_instance
