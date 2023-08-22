from typing import Any, Dict, Tuple
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import BaseModel
from core.validators import (
    processo_do_adolescente,
    preencheu
)

from alteracoes_vinculo.logic import logica_desvinculacao, logica_vinculacao

class BaseAlteracoesVinculo(BaseModel):
    class Status(models.IntegerChoices):
        PENDENTE = 1, 'Pendente'
        REALIZADA = 2, 'Realizada'
        CANCELADO = 3, 'Cancelado'
        
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, 
        default=Status.PENDENTE, 
        blank=True, 
        editable=False
    )
    
    adolescente = models.ForeignKey(
        'adolescentes.Adolescente',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=False, 
        related_name="%(class)s"
    )
    
    processo = models.ForeignKey(
        'processos.Processo', 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="%(class)s"
    )

    
    observacoes = models.TextField(
        null=True, 
        blank=True, 
        verbose_name="Observações"
    )
    
    def cancelar(self):
        self.status = self.Status.CANCELADO
        self.save()
    
    def clean(self, *args, **kwargs):    
        processo_do_adolescente(self)
        super().clean(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.status == self.Status.REALIZADA:
            raise ValidationError(f'Não é possível deletar {self.__class__.__name__} com este status')
        return super().delete(*args, **kwargs)
    
    class Meta:
        app_label = "alteracoes_vinculo"
        abstract = True

class BaseVinculacao(BaseAlteracoesVinculo):
    unidade_destino = models.ForeignKey(
        'unidades.Unidade', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Unidade de Destino",
        related_name="%(class)s_como_destino"
    )
    
    tipo_vaga = models.ForeignKey(
        'dominios.TipoVagaUnidade', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Tipo de Vaga"
    )
    
    data_entrada = models.DateField(
        blank=True, 
        null=True
    )
    
    tipo_entrada = models.ForeignKey(
        'dominios.TipoEntradaUnidade', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        verbose_name="Tipo de Entrada"
    )
    
    observacoes_entrada = models.TextField(
        null=True, 
        blank=True, 
        verbose_name="Observações Unidade de Entrada"
    )
    
    entrada_criada = models.OneToOneField(
        'unidades.EntradaAdolescente', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="%(class)s_de_entrada",
        editable=False,
        error_messages={'unique': "Duplicidade."}
    )
    
    def realizar_vinculacao(self):
        from unidades.models import EntradaAdolescente        
        
        # validacoes
        preencheu(self, 'unidade_destino')
        preencheu(self, 'tipo_vaga')
        preencheu(self, 'data_entrada')
        preencheu(self, 'tipo_entrada')
        
        try:
            self.entrada_criada = EntradaAdolescente.objects.create(
                adolescente = self.adolescente,
                processo = self.processo,
                unidade = self.unidade_destino,
                tipo_vaga = self.tipo_vaga,
                tipo_entrada = self.tipo_entrada,
                data_prevista_entrada = self.data_entrada,
                observacoes_entrada = self.observacoes_entrada,
                status =  EntradaAdolescente.Status.ENTRADA_PENDENTE
            )
            
        except Exception as e:
            if self.entrada_criada is not None:
                self.entrada_criada.delete()
                self.entrada_criada = None
                
            self.status = self.Status.PENDENTE
            self.save()
            raise e
            
        else:    
            
            self.status = self.Status.REALIZADA
            self.save()
        
            if self.entrada_criada is not None:        
                for anexo in self.anexos.all():
                    self.entrada_criada.anexos.create(anexo=anexo.anexo, descricao=anexo.descricao)
            

    def desfazer_vinculacao(self):
        from unidades.models import EntradaAdolescente
        
        if self.entrada_criada is not None:
            if self.entrada_criada.status == EntradaAdolescente.Status.ENTRADA_PENDENTE:
                self.entrada_criada.delete()
                self.entrada_criada = None    
        
        self.status = self.Status.PENDENTE
        self.save()
    
    def clean(self, *args, **kwargs):
        logica_vinculacao(self)
        return super().clean(*args, **kwargs)
    
    
    class Meta:
        app_label = "alteracoes_vinculo"
        abstract = True



class BaseDesvinculacao(BaseAlteracoesVinculo):
    unidade_origem = models.ForeignKey(
        'unidades.Unidade', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Unidade de Origem",
        related_name="%(class)s_como_origem"
    )
    
    # Dados para refletir na unidade de origem
    data_saida = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Data de Saída"
    )
    
    tipo_saida = models.ForeignKey(
        'dominios.TipoSaidaUnidade', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        verbose_name="Tipo de Saída"
    )
    
    observacoes_saida = models.TextField(
        null=True, 
        blank=True, 
        verbose_name="Observações Unidade Saída"
    )
    
    entrada_antiga = models.OneToOneField(
        'unidades.EntradaAdolescente', 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="%(class)s_de_saida",
        editable=False,
        error_messages={'unique': "Duplicidade."}
    )
    status_original_entrada_antiga = models.PositiveSmallIntegerField(
        blank=True, 
        null=True,
        editable=False
    )
    
    def realizar_desvinculacao(self):
        from unidades.models import EntradaAdolescente
        from solicitacoes.models import Solicitacao
        

        if self.entrada_antiga is not None:
            preencheu(self, 'data_saida')
            preencheu(self, 'tipo_saida')
            try:    
                status_anterior = self.entrada_antiga.status
                
                if self.entrada_antiga.status == EntradaAdolescente.Status.ENTRADA_PENDENTE:
                    self.entrada_antiga.data_entrada = self.data_saida
                
                
                if self.entrada_antiga.unidade.tipo_unidade.descricao == 'Meio Aberto' or \
                 self.entrada_antiga.status == EntradaAdolescente.Status.ENTRADA_PENDENTE:     
                    self.entrada_antiga.data_saida = self.data_saida
                    self.entrada_antiga.status = EntradaAdolescente.Status.SAIDA_REALIZADA
                    
                else:
                    self.entrada_antiga.data_prevista_saida = self.data_saida
                    self.entrada_antiga.status = EntradaAdolescente.Status.SAIDA_PENDENTE
                
                self.entrada_antiga.tipo_saida = self.tipo_saida
                self.entrada_antiga.observacoes_saida = self.observacoes_saida
                
                self.entrada_antiga.save()

                if self.adolescente.entradas_ativas.exists():
                    qs = self.adolescente.entradas_ativas.exclude(pk=self.entrada_antiga.pk)
                    if qs.exists():
                        qs.update(status = EntradaAdolescente.Status.SAIDA_REALIZADA)
                
            except Exception as e:
                self.entrada_antiga.status = status_anterior
                self.entrada_antiga.save()
                self.status = self.Status.PENDENTE
                self.save()
                raise e
            
            else:
                self.status = self.Status.REALIZADA
                self.save()
            
            for anexo in self.anexos.all():
                self.entrada_antiga.anexos.create(anexo=anexo.anexo, descricao=anexo.descricao)
            
        
        return self.entrada_antiga
    
    def desfazer_desvinculacao(self):
        if self.entrada_antiga is not None:        
            self.entrada_antiga.status = self.status_original_entrada_antiga
            self.entrada_antiga.save()

        self.status = self.Status.PENDENTE
        self.save()
    
    def clean(self, *args, **kwargs):
        logica_desvinculacao(self)
        return super().clean(*args, **kwargs)
        
    class Meta:
        app_label = "alteracoes_vinculo"
        abstract = True
    