from django import forms

from .models import AnexoEducacao, AtendimentoEducacao
from core.forms.mixins import UfCidadeBairroMixin
from core.forms.widgets import CustomAttachmentInput

class EducacaoForm(UfCidadeBairroMixin, forms.ModelForm):
    class Meta:
        model = AtendimentoEducacao
        exclude = ("adolescente",)
        labels = {
            "situacao_escolar": "Situação Escolar",
            "observacoes": "Observações",
            "i_educar": "i-educar",
        }




AnexoEducacaoFormSet = forms.inlineformset_factory(
    AtendimentoEducacao,
    AnexoEducacao,
    fields="__all__",
    extra=1,
    can_delete=True,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)
