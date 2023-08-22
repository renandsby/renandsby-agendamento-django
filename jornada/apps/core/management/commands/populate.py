import subprocess
import glob
from pathlib import Path
from django.core.management.base import BaseCommand

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Command(BaseCommand):
    help = 'Atualiza Vincula Adolescentes Randomicos a Unidades'

    def add_arguments(self, parser):
        parser.add_argument('--folder', '-f', type=str, help="Unidades que irão receber as vinculacoes.")

    def handle(self, *args, **options):
        folder = options['folder'] if options['folder'] else "./fixtures/"
        folder_path = Path(folder)
        if folder_path.is_dir():
            filelist = glob.glob(f"{folder_path}/*.json")
            for file in sorted(filelist):
                print(f"Installing fixure {file}")
                if subprocess.run(
                        ['django-admin', 'loaddata', file]).returncode == 0:
                    print(bcolors.OKGREEN+'Success loading fixture!\n'+bcolors.ENDC)
                else:
                    print(bcolors.FAIL+'Error loading fixtures from file: ' + file + "\n"+bcolors.ENDC)
        else:
            print('No fixtures found!') 


