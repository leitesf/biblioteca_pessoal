import csv

import steamfront
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from games.importador import ImportadorSteamFront
from games.models import Loja, Jogo, Plataforma


class Command(BaseCommand):
    help = "Resgata jogos de um arquivo jogos_para_importar.csv"

    def handle(self, *args, **options):
        client = steamfront.Client()
        jogos_adicionados = []
        adicionados_a_nova_loja = []
        adicionados_ao_pc = []
        jogos_nao_encontrados_no_steam = []
        importador_steam_front = ImportadorSteamFront()
        with transaction.atomic():
            with open('jogos_para_importar.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=';')
                for row in tqdm(csv_reader):
                    loja = Loja.objects.get_or_create(nome=row['loja'])[0]
                    plataforma = Plataforma.objects.get_or_create(nome=row['plataforma'])[0]
                    steam_id = importador_steam_front.buscar_steam_id(row['titulo'])
                    if not steam_id:
                        jogos_nao_encontrados_no_steam.append(row['titulo'])
                    if Jogo.objects.filter(titulo=row['titulo'], tipo='Digital').exists():
                        jogo = Jogo.objects.get(titulo=row['titulo'], tipo='Digital')
                        if loja not in jogo.lojas.all():
                            jogo.lojas.add(loja)
                            adicionados_a_nova_loja.append(jogo)
                        if plataforma not in jogo.plataformas.all():
                            jogo.plataformas.add(plataforma)
                            adicionados_ao_pc.append(jogo)
                    elif steam_id and Jogo.objects.filter(steam_id=steam_id).exists():
                        jogo = Jogo.objects.get(steam_id=steam_id)
                        if loja not in jogo.lojas.all():
                            jogo.lojas.add(loja)
                            adicionados_a_nova_loja.append(jogo)
                        if plataforma not in jogo.plataformas.all():
                            jogo.plataformas.add(plataforma)
                            adicionados_ao_pc.append(jogo)
                    else:
                        jogo = Jogo()
                        jogo.titulo = row['titulo']
                        jogo.steam_id = steam_id
                        jogo.save()
                        jogo.lojas.add(loja)
                        jogo.plataformas.add(plataforma)
                        jogo.save()
                        jogos_adicionados.append(jogo)

        for jogo in jogos_adicionados:
            print('Jogo adicionado: {}'.format(jogo.titulo))
        for jogo in adicionados_a_nova_loja:
            print('Jogo adicionado a nova loja: {}'.format(jogo.titulo))
        for jogo in adicionados_ao_pc:
            print('Jogo adicionado ao PC: {}'.format(jogo.titulo))
        for jogo in jogos_nao_encontrados_no_steam:
            print('Jogos não encontrados no steam: {}'.format(jogo))
