from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.utils import timezone
from core.forms.widgets import CustomSplitDateTimeWidget
from unidades.models import Modulo
from adolescentes.models import Adolescente, Familiar
from .models import Visita, PertenceVisita


class VisitaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.modulo = kwargs.pop("modulo", None)
        super().__init__(*args, **kwargs)
        self.initial['data_entrada'] = timezone.now
        
        self.fields["modulo"].widget = forms.HiddenInput()
        self.fields["modulo"].queryset = Modulo.objects.none()
        self.fields["adolescente"].queryset = Adolescente.objects.none()
        self.fields["visitante"].queryset = Familiar.objects.none()
        
        if self.modulo is not None:
            self.fields["modulo"].queryset = Modulo.objects.filter(id=self.modulo.id)
            self.initial["modulo"] = self.modulo
            self.fields["adolescente"].queryset = self.modulo.adolescentes

        if hasattr(self.instance, 'adolescente'):
            if self.instance.adolescente is not None:
                self.fields['visitante'].queryset = self.instance.adolescente.familiares_autorizados_visita

        if self.instance.pk and self.instance.data_entrada is not None:
            self.initial['data_saida'] = timezone.now
        
        if 'adolescente' in self.data and self.data.get('adolescente') != "":
            self.fields['visitante'].queryset = Familiar.objects.filter(adolescente__id=self.data.get('adolescente'))
    
    class Meta:
        model = Visita
        fields = "__all__"
        widgets = {
            'observacoes' : forms.widgets.Textarea( attrs={'rows':2})
        }

class PertenceVisitaForm(forms.ModelForm):
    data_recebimento = forms.SplitDateTimeField(
        required=False,
        widget=CustomSplitDateTimeWidget(time_format="%H:%M", date_format="%Y-%m-%d"),
    )
    data_entrega = forms.SplitDateTimeField(
        required=False,
        widget=CustomSplitDateTimeWidget(time_format="%H:%M", date_format="%Y-%m-%d"),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = PertenceVisita
        exclude = ("visita",)
        widgets = {
            'observacoes' : forms.widgets.Textarea( attrs={'rows':1})
        }
