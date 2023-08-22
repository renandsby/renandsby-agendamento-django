from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from core.forms.widgets import CustomSplitDateTimeWidget
from core.validators import require
from django import forms
from django.utils import timezone
from livro.models import Livro
from servidores.models import Servidor
from unidades.models import Modulo, Unidade

from .models import Acompanhamento, Livro

class LivroImprimeDataForm(forms.Form):
    data = forms.DateField(required=True, label='Selecione a Data do Livro')

class LivroForm(forms.ModelForm):
    data_abertura = forms.SplitDateTimeField(initial = timezone.now, show_hidden_initial = True, widget = CustomSplitDateTimeWidget(time_format="%H:%M", date_format="%Y-%m-%d"))
    def __init__(self, *args, **kwargs):
        self.modulo = kwargs.pop("modulo", None)
        self.unidade = kwargs.pop("unidade", None)
        super().__init__(*args, **kwargs)

        self.fields["servidor_recebimento"].disabled = True
        self.fields["servidor_passagem_anterior"].disabled = True
        self.fields["data_abertura"].disabled = True

        self.fields['ausencias'].widget.attrs['rows'] = \
            len(self.instance.ausencias.split('\n')) + 1 if self.instance.ausencias else 2

        self.fields['expediente'].widget.attrs['rows'] = \
            len(self.instance.expediente.split('\n')) + 1 if self.instance.expediente else 2

        self.fields['observacoes'].widget.attrs['rows'] = \
            len(self.instance.observacoes.split('\n')) + 1 if self.instance.observacoes else 2

        self.fields['informacoes_servidores'].widget.attrs['rows'] = \
            len(self.instance.informacoes_servidores.split('\n')) + 1 if self.instance.informacoes_servidores else 2

        self.fields['outras_informacoes'].widget.attrs['rows'] = \
            len(self.instance.outras_informacoes.split('\n')) + 1 if self.instance.outras_informacoes else 2


        
        if self.modulo:
            self.fields["plantonistas"].queryset = self.modulo.unidade.agentes

        elif self.unidade:
            self.fields["plantonistas"].queryset = self.unidade.agentes

    class Meta:
        model = Livro
        exclude = (
            "modulo",
            "unidade",
            "estrutura_copia_adolescentes_quartos",
        )
        


class NovoPlantaoForm(forms.ModelForm):
    data_abertura = forms.SplitDateTimeField(initial = timezone.now, show_hidden_initial = True, widget = CustomSplitDateTimeWidget(time_format="%H:%M", date_format="%Y-%m-%d"))
    def __init__(self, *args, **kwargs):
        self.modulo = kwargs.pop("modulo", None)
        self.unidade = kwargs.pop("unidade", None)

        super().__init__(*args, **kwargs)
        
        self.fields["modulo"].widget = forms.HiddenInput()
        self.fields["unidade"].widget = forms.HiddenInput()

        if self.modulo:
            self.fields[
                "servidor_passagem_anterior"
            ].queryset = self.modulo.unidade.agentes.order_by("nome")
            self.fields[
                "servidor_recebimento"
            ].queryset = self.modulo.unidade.agentes.order_by("nome")

            self.initial["modulo"] = self.modulo
            self.fields["modulo"].queryset = Modulo.objects.filter(id=self.modulo.id)

        elif self.unidade:
            self.fields[
                "servidor_passagem_anterior"
            ].queryset = self.unidade.agentes.order_by("nome")
            self.fields[
                "servidor_recebimento"
            ].queryset = self.unidade.agentes.order_by("nome")
            self.initial["unidade"] = self.unidade
            self.fields["unidade"].queryset = Unidade.objects.filter(id=self.unidade.id)

    class Meta:
        model = Livro
        fields = [
            "unidade",
            "modulo",
            "data_abertura",
            "servidor_passagem_anterior",
            "servidor_recebimento",
        ]

class AcompanhamentoForm(forms.ModelForm):
    data_hora = forms.SplitDateTimeField(
        show_hidden_initial=True,
        # initial=timezone.now,
        widget=CustomSplitDateTimeWidget(time_format="%H:%M", date_format="%Y-%m-%d"),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.fields['descricao'].widget.attrs['rows'] = len(self.instance.descricao.split('\n')) + 1 if self.instance.pk else 2
        
        
    class Meta:
        model = Acompanhamento
        exclude = ("modulo", "unidade")

AcompanhamentoLivroFormeSet = forms.inlineformset_factory(
    Livro,
    Acompanhamento,
    form = AcompanhamentoForm,
    fk_name="livro",
    extra=1,
    can_delete=True,
)


