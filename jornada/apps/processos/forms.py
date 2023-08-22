from django import forms
from .models import Processo, AnexoProcesso
from core.forms.widgets import CustomAttachmentInput
class ProcessoForm(forms.ModelForm):
    class Meta:
        model = Processo
        exclude = ("ativo", "adolescente")
        labels = {
                "data_apreensao": "Data Apreensão",
                "observacoes": "Observações",
                }



AnexoProcessoFormSet = forms.inlineformset_factory(
    Processo,
    AnexoProcesso,
    fk_name="processo",
    fields="__all__",
    extra=1,
    can_delete=True,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)
