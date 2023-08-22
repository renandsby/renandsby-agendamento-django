from adolescentes.models import Adolescente
import random

# SCRIPT QUE MISTURA OS SOBRENOMES DE TODOS OS ADOLESCENTES DA BASE
# SERVE PARA ANONIMIZAR OS NOMES DE FORMA A PRESERVAR A PRIVACIDADE DOS SOCIOEDUCANDOS

# ATENÇÃO!!! NÃO É POSSÍVEL DESFAZER A MISTURA DOS NOMES DEPOIS DE REALIZADA

# COMO UTILIZAR ?
# 3 - docker-compose exec -T django django-admin shell < ../scripts/shuffle_surnames.py

todos = Adolescente.objects.all()
id_nome = list(todos.values_list('id', 'nome'))

novos_nomes = []
so_sobrenome = []
for id,nome in id_nome:
    novos_nomes.append([id,nome.split(" ")[0]])
    so_sobrenome.append(" ".join(nome.split(" ")[1:]))

random.shuffle(so_sobrenome)

for idx,novo_nome in enumerate(novos_nomes):
    novo_nome[1] += " "+so_sobrenome[idx]

for adol in novos_nomes:
    adolescente = Adolescente.objects.get(id=adol[0])
    adolescente.nome = adol[1]
    adolescente.save()
    