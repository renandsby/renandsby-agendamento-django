from django import forms
from .models import Solicitacao, AnexoSolicitacao
from core.forms.widgets import CustomAttachmentInput
from core.forms.mixins import (
    PreencheProcessoPorAdolescenteMixin, 
    LabelProcessoSemNomeMixin
)

class SolicitacaoCentralForm( 
    PreencheProcessoPorAdolescenteMixin,
    LabelProcessoSemNomeMixin,
    forms.ModelForm
):  
    def __init__(self, *args, **kwargs):
        adolescentes = kwargs.pop('adolescentes', None)
        super().__init__(*args, **kwargs)
        if adolescentes is not None:
            self.fields['adolescente'].queryset = adolescentes


    class Meta:
        model = Solicitacao
        exclude = ('unidade',)
        widgets = {
            'mensagem_alteracao': forms.widgets.TextInput(
                attrs = { 'placeholder' : 'Descreva as alterações desejadas' }
            )
        }

class SolicitacaoUnidadeForm( 
    PreencheProcessoPorAdolescenteMixin,
    LabelProcessoSemNomeMixin,
    forms.ModelForm
):  
    def __init__(self, *args, **kwargs):
        adolescentes = kwargs.pop('adolescentes', None)
        super().__init__(*args, **kwargs)
        if adolescentes is not None:
            self.fields['adolescente'].queryset = adolescentes

    class Meta:
        model = Solicitacao
        fields = ('adolescente', 'processo', 'acao_solicitada', 'observacoes',)


AnexoSolicitacaoFormSet = forms.inlineformset_factory(
    Solicitacao, 
    AnexoSolicitacao,
    fk_name="solicitacao", 
    fields="__all__", 
    extra=1, 
    can_delete=True,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)
