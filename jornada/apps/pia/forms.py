from django import forms
from .models import Pia, AnexoPia
from servidores.models import Servidor
from unidades.models import Unidade
from core.forms.widgets import CustomAttachmentInput

class PiaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.unidade = kwargs.pop('unidade',None)
        super().__init__(*args, **kwargs)
        self.fields["servidor_referencia"].queryset = Servidor.objects.none()
        self.fields["tecnico_1"].queryset = Servidor.objects.none()
        self.fields["tecnico_2"].queryset = Servidor.objects.none()
        self.fields["tecnico_3"].queryset = Servidor.objects.none()
        self.fields["unidade"].widget = forms.HiddenInput()
        if self.unidade is not None and not self.instance.pk:
            self.fields["servidor_referencia"].queryset = self.unidade.servidores
            self.fields["tecnico_1"].queryset = self.unidade.especialistas
            self.fields["tecnico_2"].queryset = self.unidade.especialistas
            self.fields["tecnico_3"].queryset = self.unidade.especialistas
            self.initial["unidade"] = self.unidade
            self.fields["unidade"].queryset = Unidade.objects.filter(id = self.unidade.id)
        
        if self.instance.pk and self.instance.unidade is not None:
            self.fields["servidor_referencia"].queryset = self.instance.unidade.servidores
            self.fields["tecnico_1"].queryset = self.instance.unidade.especialistas
            self.fields["tecnico_2"].queryset = self.instance.unidade.especialistas
            self.fields["tecnico_3"].queryset = self.instance.unidade.especialistas
            self.initial["unidade"] = self.instance.unidade
            self.fields["unidade"].queryset = Unidade.objects.filter(id = self.instance.unidade.id)


    class Meta:
        model = Pia
        fields= '__all__'
        exclude = ("adolescente",)

AnexoPiaFormSet = forms.inlineformset_factory(
    Pia,
    AnexoPia,
    fk_name="anexo_pia",
    fields="__all__",
    extra=1,
    can_delete=True,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)