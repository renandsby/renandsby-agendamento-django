def somatorio(unidades):
    somatorio = 0
    com_vagas = [
        {
            'vagas': unidade.resumo_vagas
        } 
            for unidade in unidades
        ]

    for unidade in com_vagas:
        for value in unidade['vagas'].values():
            somatorio += value['ocupadas'] 

    
    return somatorio

def somatorio_internacao(unidades):
    total = {
        'total_estrita': 0,
        'total_sancao': 0,
        'total_provisoria': 0,
        'somatorio': 0
    }
    total_estrita = 0
    total_sancao = 0
    total_provisoria = 0

    com_vagas = [
        {
            'vagas': unidade.resumo_vagas
        } 
            for unidade in unidades
        ]

    for unidade in com_vagas:
        for value in unidade['vagas'].keys():
            if (value == 'Internação Estrita'):
                total_estrita += unidade['vagas'][value]['ocupadas'] 

            if (value == 'Internação Sanção'):
                total_sancao += unidade['vagas'][value]['ocupadas'] 

            if (value == 'Internação Provisória'):
                total_provisoria += unidade['vagas'][value]['ocupadas'] 

    total['total_estrita'] = total_estrita
    total['total_sancao'] = total_sancao
    total['total_provisoria'] = total_provisoria
    total['somatorio'] = total_provisoria + total_sancao + total_estrita

    return total

def adiciona_vagas(unidades):
    somatorio = 0
    com_vagas = [
        {
            'uuid': unidade.uuid,
            'sigla': unidade.sigla,
            'tipo_unidade':unidade.tipo_unidade,
            'vagas': unidade.resumo_vagas,
            'somatorio' : 0
        } 
            for unidade in unidades
        ]

    for unidade in com_vagas:
        total = {
            'total': 0,
            'ocupadas': 0,
            'disponiveis': 0
        }
        for value in unidade['vagas'].values():
            somatorio += value['ocupadas'] 
            total['total'] += value['total']
            total['ocupadas'] += value['ocupadas'] 
            total['disponiveis'] += value['disponiveis']

            adiciona_porcentagem(value)
            adiciona_progress_bg_class(value)
    
        unidade['vagas']['Total'] = total
        adiciona_porcentagem(unidade['vagas']['Total'])
        adiciona_progress_bg_class(unidade['vagas']['Total'])

    unidade['somatorio'] = somatorio
    
    return com_vagas


def adiciona_porcentagem(item):
    if item['total'] > 0:
        item['porcentagem'] = (item['ocupadas']/item['total']) * 100
        item['porcentagem'] = item['porcentagem'] 
    else: 
        item['porcentagem'] = 0


def adiciona_progress_bg_class(item):
    if item['total'] > 0:
        if item['porcentagem'] > 70:
            item['progress_bg_class'] = 'bg-warning'
        else: 
            item['progress_bg_class'] = 'bg-info'
            
        if item['porcentagem'] > 90:
            item['progress_bg_class'] = 'bg-danger'
    else:
        item['progress_bg_class'] = 'bg-info'
    
    if item['ocupadas'] == 0:
        item['progress_bg_class'] = 'bg-secondary'
    
    if item['disponiveis'] == 0 and item['ocupadas'] > 0:
        item['progress_bg_class'] = 'bg-danger'