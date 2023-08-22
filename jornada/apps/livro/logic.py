from django.core.exceptions import ValidationError
from unidades.models import Modulo, Unidade


def verifica_data_abertura(livro):
    if livro.outros_livros.filter(data_abertura__date=livro.data_abertura.date()).exists():
        raise ValidationError({'data_abertura' : f"Já existe um livro na data especificada! {livro.data_abertura.date().strftime('%d/%m/%Y')}"})
    
    if livro.outros_livros.filter(data_abertura__gte=livro.data_abertura).exists():
        raise ValidationError({'data_abertura' : f"Data deve ser posterior a outros livros existentes."})
    


def copia_informacoes_de_campos_abertos(livro):
    if livro.anterior:
        if not livro.patrimonio:
            livro.patrimonio = livro.anterior.patrimonio
        if not livro.instalacoes:
            livro.instalacoes = livro.anterior.instalacoes
        if not livro.avisos:
            livro.avisos = livro.anterior.avisos

def acompanhamentos_livro_anterior(livro):
    if livro.anterior:
        if livro.anterior.acompanhamentos.exists():
            max_date_acompanhamentos_anterior = livro.anterior.acompanhamentos.latest('data_hora').data_hora
            if livro.data_abertura < max_date_acompanhamentos_anterior:
                raise ValidationError({'data_abertura' : "Livro anterior tem acompanhamentos posteriores a esta data"})
        

def logica_criacao(livro):
    if livro.adding:
        verifica_data_abertura(livro)
        # acompanhamentos_livro_anterior(livro)
        copia_informacoes_de_campos_abertos(livro)

def logica_livro(livro):
    if livro.de_modulo:
        livro.unidade = livro.modulo.unidade
    if livro.servidor_passagem_anterior.id == livro.servidor_recebimento.id:
        raise ValidationError({'servidor_recebimento' : "Servidores de Passagem/Recebimento devem ser diferentes"})
        