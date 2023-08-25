from django import forms
from .models import RedeEmpresas, Endereco, Vagas
from usuario_empresa.models import UsuarioEmpresa
from core.forms.mixins import (
    UfCidadeBairroMixin
)

       
class RedeEmpresasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
           
    
    class Meta:
        model = RedeEmpresas
        fields = "__all__"


        
class EnderecoForm(UfCidadeBairroMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
           
    class Meta:
        model = Endereco
        exclude = ("redeEmpresas",)
    
# class VagasForm(UfCidadeBairroMixin, forms.ModelForm):

#     class Meta:
#         model = Vagas
#         exclude = ("endereco",)
#         widgets = {
#             'descricao': forms.TextInput(
#                 attrs = {
#                     'placeholder': 'Ex: Quantidade de vagas, numero de sala , ambiente'
#                 }
#             ),
#         }

        