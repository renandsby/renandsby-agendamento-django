from django.core.management.base import BaseCommand
from servidores.models import Servidor
from unidades.models import Unidade

class Command(BaseCommand):
    help = 'Atualiza unidade de servidores a partir do código de lotação'

    def add_arguments(self, parser):
        parser.add_argument('--matriculas', '-matriculas', '-mat', type=str, help="Matriculas dos servidores para ter a unidade atualizada")
        parser.add_argument('--force', nargs="?", type=bool, default=False, help="atualiza unidade inclusive de quem já tem unidade")

    def handle(self, *args, **options):
        force = options['force'] == None or options['force'] == True
        matriculas = options['matriculas'].split(',') if options['matriculas'] else None
        
        servidores = Servidor.objects.filter(codigo_lotacao__isnull=False)
        
        if matriculas:
            servidores = servidores.filter(matricula__in = matriculas)
            
        if not force:
            servidores = servidores.filter(unidade__isnull=True)
        
        for servidor in servidores:
            if servidor.codigo_lotacao is not None:
                match servidor.codigo_lotacao:
                   

                    case s if s.startswith("33200302"): 
                        unidade = Unidade.objects.get(sigla="UIPSS")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("33200303"): 
                        unidade = Unidade.objects.get(sigla="UIP")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("33200304"): 
                        unidade = Unidade.objects.get(sigla="UNIRE")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("33200305"): 
                        unidade = Unidade.objects.get(sigla="UISS")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("33200306"): 
                        unidade = Unidade.objects.get(sigla="UNISS")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("33200307"): 
                        unidade = Unidade.objects.get(sigla="UIBRA")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("33200308"): 
                        unidade = Unidade.objects.get(sigla="UISM")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("33200309"): 
                        unidade = Unidade.objects.get(sigla="UIFG")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040101"): 
                        unidade = Unidade.objects.get(sigla="SEMI GUA")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040102"): 
                        unidade = Unidade.objects.get(sigla="SEMI GAMA II")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040103"): 
                        unidade = Unidade.objects.get(sigla="SEMI GAM")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040104"): 
                        unidade = Unidade.objects.get(sigla="SEMI METRO")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040105"): 
                        unidade = Unidade.objects.get(sigla="SEMI TAG I")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040106"): 
                        unidade = Unidade.objects.get(sigla="SEMI TAG II")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040201"): 
                        unidade = Unidade.objects.get(sigla="GEAMA PLANO PILOTO")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040202"): 
                        unidade = Unidade.objects.get(sigla="GEAMA BRAZLÂNDIA")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040203"): 
                        unidade = Unidade.objects.get(sigla="GEAMA CEILÂNDIA NORTE")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040204"): 
                        unidade = Unidade.objects.get(sigla="GEAMA CEILÂNDIA SUL")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040205"): 
                        unidade = Unidade.objects.get(sigla="GEAMA GAMA")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040206"): 
                        unidade = Unidade.objects.get(sigla="GEAMA GUARÁ")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040207"): 
                        unidade = Unidade.objects.get(sigla="GEAMA NÚCLEO BANDEIRANTE")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040208"): 
                        unidade = Unidade.objects.get(sigla="GEAMA PARANOÁ")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040209"): 
                        unidade = Unidade.objects.get(sigla="GEAMA PLANALTINA")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040210"): 
                        unidade = Unidade.objects.get(sigla="GEAMA RECANTO")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040211"): 
                        unidade = Unidade.objects.get(sigla="GEAMA SAMAMBAIA")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040212"): 
                        unidade = Unidade.objects.get(sigla="GEAMA SANTA MARIA")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040213"): 
                        unidade = Unidade.objects.get(sigla="GEAMA SÃO SEBASTIAO")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040214"): 
                        unidade = Unidade.objects.get(sigla="GEAMA SOBRADINHO")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")

                    case s if s.startswith("3320040215"): 
                        unidade = Unidade.objects.get(sigla="GEAMA TAGUATINGA")
                        if unidade:
                            servidor.unidade = unidade
                            servidor.save()
                        print(f"{servidor.nome=} -> {unidade.sigla}")