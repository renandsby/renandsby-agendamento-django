from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from core.forms.widgets import CustomPictureInput, CustomAttachmentInput
from core.forms.mixins import UfCidadeBairroMixin
from .models import (
    Adolescente, 
    Foto, 
    Observacao, 
    Relatorio, 
    Endereco, 
    DocumentoAnexo, 
    AnexoEndereco,
)


class AdolescenteCreateForm(forms.ModelForm):

    def clean(self) -> Dict[str, Any]:
        cleaned_data =  super().clean()
        if 'nome' in cleaned_data\
            and 'data_nascimento' in cleaned_data:
                nome = cleaned_data['nome']
                data_nascimento = cleaned_data['data_nascimento']
                mesmo_nascimento = Adolescente.objects.filter(data_nascimento=data_nascimento)
                if mesmo_nascimento.exists():
                    from unidecode import unidecode
                    from difflib import SequenceMatcher
                    transform_string = lambda s: unidecode(s).lower().replace(" ", "")                   
                    
                    
                    nome = transform_string(nome)
                    
                    for adol in mesmo_nascimento:
                        s = SequenceMatcher(None, transform_string(adol.nome), nome)
                        if s.ratio() > .9:
                            raise ValidationError(f"Duplicidade! Adolescente muito parecido com: {adol.nome} nascido em {adol.data_nascimento.strftime('%d/%m/%y')} e Id Jornada {adol.id_jornada}")
                    
            
        return cleaned_data
    
    class Meta:
        model = Adolescente
        fields = '__all__'


class EnderecoForm(UfCidadeBairroMixin, forms.ModelForm):
   
    class Meta:
        model = Endereco
        exclude = ("adolescente",)
        widgets = {
            'descricao': forms.TextInput(
                attrs = {
                    'placeholder': 'Ex: Endereço da mãe'
                }
            ),
        }



class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        exclude = ("adolescente",)
        widgets = {
            'anexo': CustomAttachmentInput(),
        }


FotoAdolescenteFormSet = forms.inlineformset_factory(
    Adolescente, 
    Foto, 
    fk_name="adolescente", 
    fields="__all__", 
    extra=1,
    can_delete=True,
    can_delete_extra=True,
    widgets= {
        'foto': CustomPictureInput()
    }
)

DocumentoAnexoFormSet = forms.inlineformset_factory(
    Adolescente,
    DocumentoAnexo, 
    fk_name="adolescente", 
    fields="__all__", 
    extra=1, 
    max_num=1,
    can_delete=True, 
    widgets = {
        'anexo': CustomAttachmentInput(),
    } 
)



ObservacoesFormSet = forms.inlineformset_factory(
    Adolescente, 
    Observacao, 
    fk_name="adolescente", 
    fields="__all__", 
    extra=1, 
    max_num=1,
    can_delete=True,
    widgets = {
        'observacao': forms.Textarea(attrs={'placeholder': 'Ex: Como anda o comportamento do adolescente?'}),
    }  
)


ObservacaoAdolescenteFormSet = forms.inlineformset_factory(
    Adolescente, 
    Observacao, 
    fk_name="adolescente", 
    fields="__all__", 
    extra=1, 
    max_num=1,
    can_delete=True,
    widgets = {
        'observacao': forms.TextInput(attrs={'placeholder': 'Ex: Como anda o comportamento do adolescente'}),
    }  
)

AnexoEnderecoFormSet = forms.inlineformset_factory(
    Endereco,
    AnexoEndereco,
    fk_name="endereco",
    fields="__all__",
    extra=1,
    can_delete=True,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)

