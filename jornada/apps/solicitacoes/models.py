from django.db import models

from core.validators import valida, validate_file_size
from core.models import BaseModel
from core.models.utils import generate_uuid4_filename

from solicitacoes.logic import (
    logica_solicitacao
)

class Solicitacao(BaseModel):
    class Status(models.IntegerChoices):
        AGUARDANDO_VALIDACAO = 1, 'Aguardando Validação'
        VALIDADO = 2, 'Validado'
        EM_ANALISE = 3, 'Em Análise'
        REALIZADO = 4, 'Realizado'
        NEGADO = 5, 'Negado'
        
    data_solicitacao = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Data de Solicitação")
    nome_adolescente = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nome do Adolescente")
    nome_mae = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nome da Mãe")
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimetno")
    numero_processo = models.CharField(max_length=100, null=True, blank=True, verbose_name="Número do Processo")
    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")
    
    medida = models.ForeignKey('dominios.TipoMedida', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Medida")
    acao_solicitada = models.ForeignKey('dominios.AcaoSolicitacaoMovimentacao', on_delete=models.SET_NULL, null=True, verbose_name="Ação Solicitada")
    
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.AGUARDANDO_VALIDACAO, blank=True)
    
    alteracao_solicitada = models.BooleanField(default=False, verbose_name="Alteração Solicitada")
    mensagem_alteracao = models.CharField(max_length=256, null=True, blank=True, default="", verbose_name="Mensagem para Alteração")
    
    adolescente = models.ForeignKey('adolescentes.Adolescente', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Adolescente")
    processo = models.ForeignKey('processos.Processo', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Processo")
    unidade = models.ForeignKey('unidades.Unidade', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Unidade")

    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'
        ordering = ('-criado_em', )
        
        permissions = (
            ("ver", "Ver Solicitações."),
            ("editar", "Editar Solicitações."),
            ("incluir", "Incluir Solicitações."),
            ("excluir", "Excluir Solicitações."),
            ("ver_da_unidade", "Ver Solicitações da sua unidade."),
        )

    def __str__(self):
        return f"Solicitação de " + str(self.acao_solicitada.descricao) + " de " +\
            str(self.adolescente.nome if self.adolescente is not None else self.nome_adolescente)
            
    @property
    def validada(self):
        return self.adolescente is not None and not self.alteracao_solicitada
    
    def clean(self, *args, **kwargs):
        logica_solicitacao(self)
        super().clean(*args, **kwargs)

    
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def negar(self, *args, **kwargs):
        self.status = self.Status.NEGADO
        self.save()


class AnexoSolicitacao(BaseModel):
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    solicitacao = models.ForeignKey('solicitacoes.Solicitacao', related_name="anexos", on_delete=models.SET_NULL, blank=True, null=True)
    tipo_anexo = models.ForeignKey('dominios.TipoAnexoSolicitacaoMovimentacao', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Anexo")
    descricao = models.CharField(max_length=100, null=True, blank=True, verbose_name="Descrição")
