from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from servidores.models import Servidor
from unidades.models import Unidade
from dominios.models import Cargo

LOTACOES_GESTOR_GERAL = [
    "332000000000", # SUBSIS
    "332003000000", # COORINT
    "332004000000", # COORSEMA
    "332004010000", # DISEMI,
    "332004020000", # DIMA   
]


PREFIXO_INTERNACAO = "332003"
PREFIXO_SEMILIBERDADE = "33200401"
PREFIXO_MEIO_ABERTO = "33200402"


DESCRICOES_LOTACAO_GESEG = ["GERENCIA DE SEGURANCA", "NUCLEO DE DISCIPLINA"]
DESCRICOES_LOTACAO_GESP = ["GERENCIA SOCIOPSICOPEDAGOGICA", "NUCLEO PEDAGOGICO", "NUCLEO PSICOSSOCIAL"]
DESCRICOES_LOTACAO_GEAD = ["GERENCIA ADMINISTRATIVA", "NUCLEO DE DOCUMENTACAO"]


CARGOS_ADMINISTRATIVOS = Cargo.objects.filter(descricao__in = ["TECNICO SOCIOEDUCATIVO", "TSOCIO - AG. ADMINISTRATIVO"])
CARGOS_AGENTES_SOCIOEDUCATIVOS = Cargo.objects.filter(descricao__in = ["AGENTE SOCIOEDUCATIVO", "TSOCIO - AGENTE SOCIAL", "AUXILIAR SOCIOEDUCATIVO"])
CARGOS_ESPECIALISTAS = Cargo.objects.filter(descricao__startswith="ESOCIO")


class Command(BaseCommand):
    help = 'Atualiza unidade de servidores a partir do código de lotação'

    def add_arguments(self, parser):
        parser.add_argument('--matriculas', '-matriculas', '-mat', type=str, help="Matriculas dos servidores para ter a unidade atualizada")
        parser.add_argument('--clean', nargs="?", type=bool, default=False, help="Remove grupos anteriores")

    def handle(self, *args, **options):
        matriculas = options['matriculas'].split(',') if options['matriculas'] else None
        clean = options['clean'] == None or options['clean'] == True
        
        print("\n Preenchendo grupos...\n")
        
        servidores = Servidor.objects.all()
        
            
        if matriculas:
            servidores = servidores.filter(matricula__in = matriculas)
        
        for servidor in servidores:
            if clean:
                servidor.user.groups.clear()
        
            if servidor.codigo_lotacao in LOTACOES_GESTOR_GERAL:
                group = Group.objects.get(name='Gestor Geral')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
                
            
     
            if (
                servidor.codigo_lotacao is not None and  
                servidor.codigo_lotacao.startswith("33200301")
            ):
                group = Group.objects.get(name='Atendimento Inicial')
                servidor.user.groups.add(group)
                print(f"{servidor.nome=} => {group.name}")
                    
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_INTERNACAO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.denominacao_funcao is not None and
                servidor.denominacao_funcao.upper() in [ "DIRETOR" , "VICE-DIRETOR" ]
            ):
                group = Group.objects.get(name='Direção Internação')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_INTERNACAO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.descricao_lotacao is not None and
                servidor.descricao_lotacao.upper() in ["GERENCIA DE SEGURANCA", "NUCLEO DE DISCIPLINA"]
            ):
                group = Group.objects.get(name='Servidor GESEG Internação')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_INTERNACAO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.descricao_lotacao is not None and
                servidor.descricao_lotacao.upper() in DESCRICOES_LOTACAO_GESEG and
                servidor.denominacao_funcao is not None
            ):
                group = Group.objects.get(name='Gestor GESEG Internação')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_INTERNACAO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.descricao_lotacao is not None and
                servidor.descricao_lotacao.upper() in DESCRICOES_LOTACAO_GESP
            ):
                group = Group.objects.get(name='Servidor GESP Internação')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_INTERNACAO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.descricao_lotacao is not None and
                servidor.descricao_lotacao.upper() in DESCRICOES_LOTACAO_GESP and
                servidor.denominacao_funcao is not None
            ):
                group = Group.objects.get(name='Gestor GESP Internação')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_INTERNACAO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.descricao_lotacao is not None and
                servidor.descricao_lotacao.upper() in DESCRICOES_LOTACAO_GEAD
            ):
                group = Group.objects.get(name='Servidor GEAD Internação')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_INTERNACAO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.descricao_lotacao is not None and
                servidor.descricao_lotacao.upper() in DESCRICOES_LOTACAO_GEAD and
                servidor.denominacao_funcao is not None
            ):
                group = Group.objects.get(name='Gestor GEAD Internação')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_SEMILIBERDADE) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.cargo in CARGOS_ADMINISTRATIVOS
            ):
                group = Group.objects.get(name='Administrativo Semiliberdade')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_SEMILIBERDADE) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.cargo in (CARGOS_AGENTES_SOCIOEDUCATIVOS | CARGOS_ESPECIALISTAS)
            ):
                group = Group.objects.get(name='Servidor Semiliberdade')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
                
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_SEMILIBERDADE) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.denominacao_funcao is not None
            ):
                group = Group.objects.get(name='Gestor Semiliberdade')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_MEIO_ABERTO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.cargo in CARGOS_ADMINISTRATIVOS
            ):
                group = Group.objects.get(name='Administrativo Meio Aberto')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_MEIO_ABERTO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.cargo in (CARGOS_AGENTES_SOCIOEDUCATIVOS | CARGOS_ESPECIALISTAS)
            ):
                group = Group.objects.get(name='Servidor Meio Aberto')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
                
            if (
                servidor.codigo_lotacao is not None and 
                servidor.codigo_lotacao.startswith(PREFIXO_MEIO_ABERTO) and
                servidor.codigo_lotacao not in LOTACOES_GESTOR_GERAL and
                servidor.denominacao_funcao is not None
            ):
                group = Group.objects.get(name='Gestor Meio Aberto')
                servidor.user.groups.add(group)
                print(f"{servidor.nome} => {group.name}")
            