from django import forms
from core.forms.widgets import CustomAttachmentInput
from core.forms.mixins import (
    PreencheProcessoPorAdolescenteMixin,
    LabelProcessoSemNomeMixin
)

from adolescentes.models import Adolescente

from .models import (
    Vinculacao, 
    AnexoVinculacao,
    Desvinculacao,
    AnexoDesvinculacao,
    Transferencia,
    AnexoTransferencia
)

def adolescente_label_from_instance(self):
        label = str(self.nome)
        if self.possui_entrada_ativa:
            label += f" ({self.entrada_em_unidade_atual.get_status_display()} em {str(self.unidade_atual.sigla)})"
            if self.entrada_em_unidade_atual.processo is not None:
                label += f" [{str(self.entrada_em_unidade_atual.processo.str_sem_nome())}]"
        return label


class VinculacaoForm(
    PreencheProcessoPorAdolescenteMixin,
    LabelProcessoSemNomeMixin,
    forms.ModelForm
):
    class Meta:
        model = Vinculacao
        exclude = ('unidade_origem', 'entrada_antiga', 'unidade_origem', 'entrada_criada')
        widgets = {
            'observacoes' : forms.widgets.Textarea(attrs={'rows':3}),
            'observacoes_entrada' : forms.widgets.Textarea(attrs={'rows':2}),
            'observacoes_saida' : forms.widgets.Textarea(attrs={'rows':2}),   
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['adolescente'].label_from_instance = adolescente_label_from_instance    



AnexoVinculacaoFormSet = forms.inlineformset_factory(
    Vinculacao, 
    AnexoVinculacao,
    fk_name="vinculacao", 
    fields="__all__", 
    extra=0,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)


class TransferenciaForm(
    PreencheProcessoPorAdolescenteMixin,
    LabelProcessoSemNomeMixin,
    forms.ModelForm
):

    class Meta:
        model = Transferencia
        exclude = ('unidade_origem', 'entrada_antiga', 'unidade_origem', 'entrada_criada')
        widgets = {
            'observacoes' : forms.widgets.Textarea(attrs={'rows':3}),
            'observacoes_entrada' : forms.widgets.Textarea(attrs={'rows':2}),
            'observacoes_saida' : forms.widgets.Textarea(attrs={'rows':2}),   
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['adolescente'].label_from_instance = adolescente_label_from_instance
        self.fields['adolescente'].queryset = Adolescente.vinculados_em_unidade()
                
AnexoTransferenciaFormSet = forms.inlineformset_factory(
    Transferencia, 
    AnexoTransferencia,
    fk_name="transferencia", 
    fields="__all__", 
    extra=0,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)




class DesvinculacaoForm( 
    PreencheProcessoPorAdolescenteMixin,
    forms.ModelForm
):
    class Meta:
        model = Desvinculacao
        exclude = ('unidade_origem', 'entrada_antiga', 'unidade_origem')
        widgets = {
            'observacoes' : forms.widgets.Textarea(attrs={'rows':3}),
            'observacoes_saida' : forms.widgets.Textarea(attrs={'rows':2}),  
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['adolescente'].label_from_instance = adolescente_label_from_instance
        self.fields['adolescente'].queryset = Adolescente.vinculados_em_unidade()
                
AnexoDesvinculacaoFormSet = forms.inlineformset_factory(
    Desvinculacao, 
    AnexoDesvinculacao,
    fk_name="desvinculacao",
    fields="__all__", 
    extra=0,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)

