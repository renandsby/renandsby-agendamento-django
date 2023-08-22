from core.validators import (
    raise_validation_error,
    preencheu, 
    adolescente_esta_lotado_em_alguma_unidade, 
    adolescente_nao_tem_saida_pendente, 
    adolescente_nao_tem_entrada_pendente
)
from django.core.exceptions import ValidationError


def origem_e_destino_diferentes(obj):
    if obj.unidade_destino == obj.adolescente.unidade_atual:
        raise ValidationError(
            f'O adolescente já está lotado na unidade {obj.adolescente.unidade_atual}')







def pode_cancelar(obj):
    if not obj.status == obj.__class__.Status.PENDENTE:
        raise ValidationError(
            f'Não foi possível cancelar a {obj.__class__.__name__}. Só é possível cancelar se estiver pendente!')


def pode_vincular(vinculacao):
    preencheu(vinculacao, 'unidade_destino')
    preencheu(vinculacao, 'tipo_vaga')
    adolescente_nao_tem_entrada_pendente(vinculacao)


def pode_transferir(transferencia):
    preencheu(transferencia,'unidade_destino')
    preencheu(transferencia,'tipo_vaga')
    adolescente_nao_tem_entrada_pendente(transferencia)
    adolescente_nao_tem_saida_pendente(transferencia)
    adolescente_esta_lotado_em_alguma_unidade(transferencia)
    origem_e_destino_diferentes(transferencia)


def pode_desvincular(desvinculacao):
    adolescente_esta_lotado_em_alguma_unidade(desvinculacao)
    adolescente_nao_tem_saida_pendente(desvinculacao)


def nao_pode_estar_pendente(obj):
    if obj.status == obj.__class__.Status.PENDENTE:
        raise ValidationError(
            f'Status da {obj.__class__.__name__} não pode ser Pendente.')

def pode_deletar_vinculacao(vinculacao):
    if vinculacao.entrada_criada is not None:
        if vinculacao.entrada_criada.status > 1:
            raise ValidationError(f"Checkin na unidade {vinculacao.entrada_criada.unidade.sigla} já foi realizado") 

def pode_desfazer_vinculacao(vinculacao):
    nao_pode_estar_pendente(vinculacao)
    if vinculacao.entrada_criada is not None:
        if vinculacao.entrada_criada.status > 1:
            raise ValidationError(f"Checkin na unidade {vinculacao.entrada_criada.unidade.sigla} já foi realizado") 


def pode_deletar_transferencia(transferencia):
    if transferencia.entrada_antiga is not None:
        if transferencia.entrada_antiga.status == 4:
            raise ValidationError(f"Checkout na unidade {transferencia.entrada_antiga.unidade.sigla}  de origem já foi realizado") 

    if transferencia.entrada_criada is not None:
        if transferencia.entrada_criada.status > 1:
            raise ValidationError(f"Checkin na unidade {transferencia.entrada_criada.unidade.sigla} já foi realizado") 

def pode_desfazer_transferencia(transferencia):
    nao_pode_estar_pendente(transferencia)
    if transferencia.entrada_antiga is not None:
        if transferencia.entrada_antiga.status == 4:
            raise ValidationError(f"Checkout na unidade {transferencia.entrada_antiga.unidade.sigla}  de origem já foi realizado") 

    if transferencia.entrada_criada is not None:
        if transferencia.entrada_criada.status > 1:
            raise ValidationError(f"Checkin na unidade {transferencia.entrada_criada.unidade.sigla} já foi realizado") 


def pode_deletar_desvinculacao(desvinculacao):
    if desvinculacao.entrada_antiga is not None:
        if desvinculacao.entrada_antiga.status == 4:
            raise ValidationError(f"Checkout na unidade {desvinculacao.entrada_antiga.unidade.sigla}  já foi realizado") 

def pode_desfazer_desvinculacao(desvinculacao):
    nao_pode_estar_pendente(desvinculacao)
    if desvinculacao.entrada_antiga is not None:
        if desvinculacao.entrada_antiga.status == 4:
            raise ValidationError(f"Checkout na unidade {desvinculacao.entrada_antiga.unidade.sigla}  já foi realizado") 