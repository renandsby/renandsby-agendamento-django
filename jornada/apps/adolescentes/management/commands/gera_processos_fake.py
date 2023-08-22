from django.core.management.base import BaseCommand
from adolescentes.models import Adolescente
from processos.models import Processo
from dominios.models import TipoProcesso
from random import randint

class Command(BaseCommand):
    help = 'Gera processos fake para adolescentes'

    def add_arguments(self, parser):
        parser.add_argument('--sipia', '-sipia', type=str, help="SIPIA dos adolescentes para terem os processos gerados")

    def handle(self, *args, **options):
        sipia = options['sipia'].split(',') if options['sipia'] else None
        
        adolescentes = Adolescente.objects.all()
        
        if sipia:
            adolescentes = adolescentes.filter(sipia__in = sipia)
        
        for adolescente in adolescentes:
            p = Processo.objects.create(
                adolescente = adolescente,
                tipo_processo = TipoProcesso.objects.get(id=1),
                numero = str(randint(10000000000000,99999999999999))
            )
            print(f"{adolescente.nome} -> {p.numero}")
            