from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from core.forms.widgets import CustomPictureInput, CustomAttachmentInput
from core.forms.mixins import UfCidadeBairroMixin
from .models import (
    Adolescente, 
    Foto, 
    Observacao, 
    Telefone,
    Relatorio, 
    Endereco, 
    Familiar, 
    DocumentoAnexo, 
    AnexoFamiliar, 
    AnexoEndereco,
    AnexoTelefone
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

class FamiliarForm(forms.ModelForm):
    class Meta:
        model = Familiar
        exclude = ("adolescente",)
        widgets = {
            'observacoes' : forms.widgets.Textarea(attrs={'rows':3})
        }


class TelefoneForm(forms.ModelForm):
    class Meta:
        model = Telefone
        exclude = ("adolescente",)


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


FamiliarAdolescenteFormSet = forms.inlineformset_factory(
    Adolescente,
    Familiar, 
    fk_name="adolescente", 
    fields="__all__", 
    extra=1, 
    max_num=1,
    can_delete=True, 
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

TelefoneAdolescenteFormSet = forms.inlineformset_factory(
    Adolescente, 
    Telefone, 
    fk_name="adolescente", 
    fields="__all__", 
    extra=1, 
    max_num=1,
    can_delete=True,
    widgets = {
        'descricao': forms.TextInput(attrs={'placeholder': 'Ex: Telefone Da Mãe'}),
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

AnexoFamiliarFormSet = forms.inlineformset_factory(
    Familiar,
    AnexoFamiliar,
    fk_name="familiar",
    fields="__all__",
    extra=1,
    can_delete=True,
    widgets = {
        'anexo': CustomAttachmentInput(),
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
AnexoTelefoneFormSet = forms.inlineformset_factory(
    Telefone,
    AnexoTelefone,
    fk_name="telefone",
    fields="__all__",
    extra=1,
    can_delete=True,
    widgets = {
        'anexo': CustomAttachmentInput(),
    }
)
