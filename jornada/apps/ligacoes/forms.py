from django import forms
from django.utils import timezone
from unidades.models import Modulo
from adolescentes.models import Adolescente, Telefone
from .models import Ligacao


class LigacaoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.modulo = kwargs.pop("modulo", None)
        super().__init__(*args, **kwargs)
        if self.instance.adding:
            self.initial['data_ligacao'] = timezone.now
        
        self.fields["modulo"].widget = forms.HiddenInput()
        self.fields["modulo"].queryset = Modulo.objects.none()
        self.fields["adolescente"].queryset = Adolescente.objects.none()
        self.fields["telefone"].queryset = Telefone.objects.none()
        
        cols = 2
        if self.instance.pk is not None:
            cols += len(self.instance.observacoes.split('\n')) - 1
        self.fields['observacoes'].widget.attrs['rows'] = cols
        
        if self.modulo is not None:
            self.fields["modulo"].queryset = Modulo.objects.filter(id=self.modulo.id)
            self.initial["modulo"] = self.modulo
            self.fields["adolescente"].queryset = self.modulo.adolescentes

        if hasattr(self.instance, 'adolescente'):
            if self.instance.adolescente is not None:
                self.fields['telefone'].queryset = self.instance.adolescente.telefones_autorizados
        
        if 'adolescente' in self.data and self.data.get('adolescente') != "":
            self.fields['telefone'].queryset = Telefone.objects.filter(adolescente__id=self.data.get('adolescente'))
    
    class Meta:
        model = Ligacao
        fields = "__all__"
        widgets = {
            'observacoes' : forms.widgets.Textarea( attrs={'rows':2})
        }
