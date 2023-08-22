from datetime import datetime
from django.test import TestCase
from django.core.management import call_command
from unidades.models import Unidade, Quarto, Modulo
from django.core.exceptions import ValidationError
import datetime 

class UnidadesTestCase(TestCase):
    fixtures = [
        'fixtures/base/1-dominios.json', 
        'fixtures/base/4-base_unidades.json',
    ]

    @classmethod
    def setUpTestData(cls):
        ''' Isso aqui roda uma vez só antes de todos os testes '''
        cls.UNIRE = Unidade.objects.get(sigla='UNIRE')
        cls.UIBRA = Unidade.objects.get(sigla='UIBRA')
        cls.GERSEMIMET = Unidade.objects.get(sigla='GERSEMIMET')
        cls.GEAMANB = Unidade.objects.get(sigla='GEAMANB')
        
       


    def setUp(self):
        ''' Isso aqui roda antes de cada teste '''
        ...


    
    
        
