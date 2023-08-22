import csv
from datetime import datetime
from servidores.models import Servidor
from custom_auth.models import CustomUser
from dominios.models import Cargo
from adolescentes.models import Adolescente
from dominios.models import Genero, Cor
from unidades.models import Unidade, EntradaAdolescente
# SCRIPT DE CARGA CSV


# COMO UTILIZAR ?
# 1 - colocar o CSV dentro da pasta scripts
# 2 - Altera o script abaixo adequando para o seu csv
# 3 - docker-compose exec -T django django-admin shell < ../scripts/carga_csv.py

# with open('/app/scripts/EFETIVO 04-07.csv', newline='\n', mode="r", encoding='utf-8-sig') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=";")
#     for row in reader:
#         print(row)


# CARREGANDO SERVIDORES E CARGOS
with open('/app/scripts/SERVIDORES28-07.csv', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:

        try:
            servidor = Servidor.objects.get(matricula__icontains=row['MATRICULA'])
            servidor.codigo_lotacao = row['LOTACAO']
            servidor.descricao_lotacao = row['DESCRICAO LOTACAO']

            if row['CARGO']:
                cargo = Cargo.objects.filter(codigo=row['CARGO'])
                if cargo.exists():
                    servidor.cargo = cargo.first()
                else: 
                    print('CARGO NÃO ENCONTRADO!', row['CARGO'], row['DENOMINACAO'])
                
            servidor.codigo_funcao = row['CODIGO FUNCAO']
            servidor.denominacao_funcao = row['DENOMINACAO FUNCAO']
            servidor.save()
        except Servidor.DoesNotExist:
            print('NÃO ENCONTRADO! ->', row['NOME'], row['MATRICULA'])
            
        

# with open('/app/scripts/CARGOS.csv', newline='\n') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:    
#         servidor = Servidor.objects.filter(matricula=row['MATRICULA']).first()
#         if servidor is not None:
#             servidor.codigo_funcao = row['CODIGO FUNCAO']
#             servidor.denominacao_funcao = row['DENOMINACAO FUNCAO']
#             servidor.save()
        

# with open('/app/scripts/SERVIDORES.csv', newline='\n') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:    
#         servidor = Servidor.objects.filter(matricula=row['MATRICULA']).first()
#         if servidor is not None:
#             cargo = Cargo.objects.filter(codigo=row['CARGO']).first()
#             if cargo:
#                 print(f"{servidor} -> {cargo}")
#                 servidor.cargo = cargo
#                 servidor.save()


## CRIA ADOLESCENTES NO BANCO CASO JA NAO EXISTA (CHECA PELO SIPIA)    
# with open('/app/scripts/EFETIVO 04-07.csv', newline='\n', mode="r", encoding='utf-8-sig') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=";")
#     for row in reader:
#         if row['SIPIA'] != '':
#             if not Adolescente.objects.filter(sipia=row['SIPIA']).exists():                
#                 try:
#                     genero = Genero.objects.get(descricao__iexact=row['GÊNERO'])
#                 except Genero.DoesNotExist:
#                     genero = Genero.objects.get(descricao__iexact='Não Declarado')
                
#                 try:
#                     cor = Cor.objects.get(descricao__iexact=row['RAÇA/COR'])
#                 except Cor.DoesNotExist:
#                     cor = Cor.objects.get(descricao__iexact='Não Declarado')
                    
                
#                 ad = Adolescente(
#                     nome = row['NOME'],
#                     sipia = row['SIPIA'],
#                     data_nascimento = datetime.strptime(row['DATA DE NASCIMENTO'] ,'%d/%m/%y'),
#                     genero=genero, 
#                     cor=cor, 
#                 )
#                 try:
#                     ad.save()
#                 except Exception as e:
#                     print(ad, "Não salvo", e)
        
# with open('/app/scripts/EFETIVO 04-07.csv', newline='\n', mode="r", encoding='utf-8-sig') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=";")
#     for row in reader:
#         try:
#             adol = Adolescente.objects.get(sipia=row['SIPIA'])
#             uni = Unidade.objects.get(sigla=row['UNIDADE'])
            
#             EntradaAdolescente.objects.create(
#                 adolescente = adol,
#                 unidade = uni,
#                 status = EntradaAdolescente.Status.ENTRADA_PENDENTE,
#                 observacoes_entrada = "Preencha a data real de entrada do adolescente na unidade.",
#                 data_entrada = datetime(minute=00, hour=00, second=59, year=2023, month=7, day=4)
#             )
            
#         except Exception as e:
#             print(row, e)
