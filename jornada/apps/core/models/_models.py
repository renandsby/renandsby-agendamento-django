import uuid as uuid_lib
from django.db import models

from .mixins import (
    ValidateOnSaveMixin,
    RegistraMudancasMixin,
)
from simple_history.models import HistoricalRecords


class RegistraCriacaoModificacaoModel(models.Model):
    '''
        Salva os dados de criação e modificação automaticamente.
        Herdando deste model, e adicionando o Middleware AuthoringMiddleware
        esses dados serão sempre armazenados.
    '''
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable= False)
    criado_por = models.ForeignKey('custom_auth.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_criados', editable= False)
    modificado_em = models.DateTimeField(auto_now=True, null=True, blank=True, editable= False)
    modificado_por = models.ForeignKey('custom_auth.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_modificados', editable= False)
    history = HistoricalRecords(inherit=True)

    class Meta: 
        abstract = True


class BaseModel(
    RegistraMudancasMixin,
    ValidateOnSaveMixin,
    RegistraCriacaoModificacaoModel
):   
    uuid = models.UUIDField(
        unique=True, 
        default=uuid_lib.uuid4, 
        editable=False
    )
    class Meta:
        abstract = True


class VinculaPassagemAdolescente(models.Model):   
    entrada_vinculada = models.ForeignKey(
        'unidades.EntradaAdolescente', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True, 
        related_name="%(class)ss_vinculados",
        editable=False
    )
    
    def clean(self) -> None:
        if self.adding:
            if hasattr(self, 'adolescente'):
                entrada_atual = self.adolescente.entrada_em_unidade_atual
                if entrada_atual is not None:
                    self.entrada_vinculada = entrada_atual
        return super().clean()

    class Meta:
        abstract = True