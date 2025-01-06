from datetime import datetime

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from games.models import Jogo
from main.models import *


class Command(BaseCommand):
    help = "Converte um arquivo livros.json baixado do skoob em livros cadastrados no sistema"

    def handle(self, *args, **options):
        with transaction.atomic():
            ports = requests.get(
                'https://raw.githubusercontent.com/PortsMaster/PortMaster-Info/main/ports.json'
            ).json()['ports']
            print("Importando jogos do Portmaster")
            ports_detectados=[]
            ports_a_verificar=[]
            for port in tqdm(ports.keys()):
                titulo = ports[port]["attr"]["title"]
                if "trimui-smart-pro:ALL" in ports[port]["attr"]["avail"] and Jogo.objects.filter(titulo=titulo).exists():
                    import ipdb; ipdb.set_trace()
                    Jogo.objects.filter(titulo=titulo).update(possui_port=True)
                    ports_detectados.append(titulo)
                elif "trimui-smart-pro:ALL" in ports[port]["attr"]["avail"] and Jogo.objects.filter(titulo__icontains=titulo).exists():
                    ports_a_verificar.append(titulo)
                    
            for port in ports_detectados:
                print('Port detectado: {}'.format(port))
                    
            for port in ports_a_verificar:
                print('Port a verificar: {}'.format(port))
