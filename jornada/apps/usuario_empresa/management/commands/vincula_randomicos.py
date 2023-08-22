import names
import random
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from unidades.models import Unidade



class Command(BaseCommand):
    
    @staticmethod
    def _random_birth_date(min_age:int, max_age:int):
        end = datetime.now() - timedelta(days=min_age*365)
        start = datetime.now() - timedelta(days=max_age*365)
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)
    
    @classmethod
    def _gera_adolescente_aleatorio(cls):
        return Adolescente.objects.create(
            nome = names.get_full_name().upper(),

            data_nascimento = cls._random_birth_date(16,20)
        )

    
    help = 'Vincula Adolescentes Randomicos a Unidades'

    def add_arguments(self, parser):
        parser.add_argument('--unidades', '-unidades', type=str, help="Unidades que irão receber as vinculacoes.")
        parser.add_argument('--qtd', '-qtd', type=str, help="Quantidade de vinculações por unidade.")
        parser.add_argument('--lotado', type=bool, default=False, help="Deixar lotado.")
        parser.add_argument('--verbose', '-verbose', type=bool, default=False, help="Verboso.")

    def handle(self, *args, **options):

        un_choices = [i.upper() for i in options['unidades'].split(',')] if options['unidades'] else None
        quantidade = int(options['qtd']) if options['qtd'] else 1
        lotado = options['lotado']
        verbose = options['verbose']
        
        unidades = Unidade.objects.all()
        if un_choices:
            unidades = unidades.filter(sigla__in=un_choices)
        
        for unidade in unidades:
            for i in range(quantidade):
                adolescente = self._gera_adolescente_aleatorio()
         
                tipos_vaga = list(unidade.vagas_disponiveis.keys())
              
                modulo = unidade.modulos.order_by('?').first() if lotado and unidade.modulos.exists() else None
                quarto = modulo.quartos.order_by('?').first() if modulo is not None and modulo.quartos is not None else None
                
  
                if verbose:
                    print(unidade)
                
            
            
            