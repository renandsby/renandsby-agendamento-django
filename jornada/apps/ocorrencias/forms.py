from django import forms
from django.utils import timezone
from core.forms.widgets import CustomAttachmentInput
from ocorrencias.models import AnexoOcorrencia, Ocorrencia
from unidades.models import Unidade, Modulo

class OcorrenciaForm(forms.ModelForm):
    
    def clean(self):
        infracoes_leves = self.cleaned_data.get("infracoes_leves")
        infracoes_medias = self.cleaned_data.get("infracoes_medias")
        infracoes_graves = self.cleaned_data.get("infracoes_graves")
        infracoes_gravissimas = self.cleaned_data.get("infracoes_gravissimas")

        if not infracoes_medias and not infracoes_graves and not infracoes_leves:
            raise forms.ValidationError("Favor escolher pelo menos uma infração.")
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        self.modulo = kwargs.pop("modulo", None)
        super().__init__(*args, **kwargs)
        
        self.initial["data_hora"] = timezone.now
        self.fields["modulo"].widget = forms.HiddenInput()
        self.fields["modulo"].queryset = Modulo.objects.none()
        self.fields["unidade"].widget = forms.HiddenInput()
        self.fields["unidade"].queryset = Unidade.objects.none()

        if self.modulo is not None:
            self.fields["modulo"].queryset = Modulo.objects.filter(id=self.modulo.id)
            self.initial["modulo"] = self.modulo
            
            self.fields["unidade"].queryset = Unidade.objects.filter(id=self.modulo.unidade.id)
            
            self.fields["adolescentes_autores"].queryset = self.modulo.unidade.adolescentes_lotados
            self.fields["adolescentes_vitimas"].queryset = self.modulo.unidade.adolescentes_lotados


            self.regulamento_infracoes_id = self.modulo.unidade.regulamento_infracoes_id
            self.fields["servidores_relacionados"].queryset = self.modulo.unidade.servidores
            infracoes_unidade = self.modulo.unidade.regulamento_infracoes.infracoes.all()
            
            self.fields["infracoes_leves"].queryset = infracoes_unidade.filter(gravidade__descricao="Leve")
            self.fields["infracoes_graves"].queryset = infracoes_unidade.filter(gravidade__descricao="Grave")
            self.fields["infracoes_medias"].queryset = infracoes_unidade.filter(gravidade__descricao="Média")
            self.fields["infracoes_gravissimas"].queryset = infracoes_unidade.filter(gravidade__descricao="Gravíssimas")



    class Meta:
        model = Ocorrencia
        fields = "__all__"


AnexoOcorrenciaFormSet = forms.inlineformset_factory(
    Ocorrencia,
    AnexoOcorrencia,
    fk_name="ocorrencia",
    fields="__all__",
    labels={"descricao": "descrição"},
    extra=1,
    can_delete=True,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)
