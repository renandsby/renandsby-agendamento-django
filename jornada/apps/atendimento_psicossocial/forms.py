from django import forms
from .models import AtendimentoPsicossocial, AnexoAtendimento
from core.forms.widgets import CustomAttachmentInput
from django.utils import timezone

class AtendimentoPsicossocialForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.fields['observacoes'].widget.attrs['placeholder'] = "Informações que apenas poderão ser visualizadas por outros Especialistas."
        self.fields['observacoes_publicas'].widget.attrs['placeholder'] = "Informações que poderão ser visualizadas por todos os servidores da Unidade."

        if self.instance.adding:
            self.initial['data_atendimento'] = timezone.now
      
        cols = 10
        tam = 0
        if self.instance.pk is not None:
            if self.observacoes is not None:
                tam = len(self.instance.observacoes.split('\n'))
        self.fields['observacoes'].widget.attrs['rows'] = cols if cols > tam else tam + 1
        
        cols = 4
        tam = 0
        if self.instance.pk is not None:
            if self.observacoes_publicas is not None:
                tam = len(self.instance.observacoes_publicas.split('\n'))
        self.fields['observacoes_publicas'].widget.attrs['rows'] = cols if cols > tam else tam + 1
        
        
    class Meta:
        model = AtendimentoPsicossocial
        exclude = ("adolescente",)
    

AnexoAtendimentoFormSet = forms.inlineformset_factory(
    AtendimentoPsicossocial,
    AnexoAtendimento,
    fk_name="atendimento_psicossocial",
    fields="__all__",
    extra=1,
    can_delete=True,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)
