import names
import random
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand




class Command(BaseCommand):
    ...
    # @staticmethod
    # def _random_birth_date(min_age:int, max_age:int):
    #     end = datetime.now() - timedelta(days=min_age*365)
    #     start = datetime.now() - timedelta(days=max_age*365)
    #     delta = end - start
    #     int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    #     random_second = random.randrange(int_delta)
    #     return start + timedelta(seconds=random_second)
    
    # @classmethod
    # def _gera_adolescente_aleatorio(cls):
    #     return Adolescente.objects.create(
    #         nome = names.get_full_name().upper(),

    #         data_nascimento = cls._random_birth_date(16,20)
    #     )

    
    # help = 'Vincula Adolescentes Randomicos a Unidades'
