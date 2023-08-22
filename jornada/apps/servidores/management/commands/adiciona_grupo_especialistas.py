from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from servidores.models import Servidor
from dominios.models import Cargo


class Command(BaseCommand):
    help = 'Identifica especialistas e adiciona grupo correspondente'

    def handle(self, *args, **options):
        
        print("\n Buscando Especialistas...\n")
        
        especialistas = Servidor.objects.filter(cargo__id__in=Cargo.objects.filter(descricao__startswith="ESOCIO").values_list('id', flat=True))
        grupo_especialista = Group.objects.get(name='Especialista')
        
        for especialista in especialistas:
            especialista.user.groups.add(grupo_especialista)    
            print(f"{especialista.nome} => {grupo_especialista.name}")

            