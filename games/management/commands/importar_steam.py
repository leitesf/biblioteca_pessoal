from datetime import datetime

import steamfront
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from games.models import Loja, Jogo, Plataforma
from main.models import *


class Command(BaseCommand):
    help = "Resgata jogos do Steam"

    def handle(self, *args, **options):
        configuracao = ConfiguracaoSistema.objects.first()
        usuario_principal = configuracao.usuario_principal
        steam_api_key = configuracao.steam_api_key
        if steam_api_key and usuario_principal and usuario_principal.steam_user:
            with transaction.atomic():
                steam = Loja.objects.get_or_create(nome='Steam')[0]
                pc = Plataforma.objects.get_or_create(nome='PC')[0]

                dados = requests.get(
                    "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&include_appinfo=true&format=json".format(
                        steam_api_key,
                        usuario_principal.steam_user
                    )
                ).json()
                print("Importando jogos do usuário principal")
                jogos_adicionados = []
                adicionados_ao_steam = []
                adicionados_ao_pc = []
                # import ipdb; ipdb.set_trace()
                for item in tqdm(dados['response']['games']):
                    if not Jogo.objects.filter(titulo=item['name'], tipo='Digital').exists() and \
                            not Jogo.objects.filter(steam_id=item['appid']).exists():
                        jogo = Jogo()
                        jogo.titulo = item['name']
                        jogo.steam_id = item['appid']
                        jogo.save()
                        jogo.lojas.add(steam)
                        jogo.plataformas.add(pc)
                        jogo.save()
                        jogos_adicionados.append(jogo)
                    elif Jogo.objects.filter(steam_id=item['appid']).exists():
                        pass
                    else:
                        jogo = Jogo.objects.get(titulo=item['name'], tipo='Digital')
                        if steam not in jogo.lojas.all():
                            jogo.lojas.add(steam)
                            adicionados_ao_steam.append(jogo)
                        if pc not in jogo.plataformas.all():
                            jogo.plataformas.add(pc)
                            adicionados_ao_pc.append(jogo)
                        jogo.steam_id = item['appid']
                        jogo.save()
        else:
            print("Verifique se o usuário principal possui steam user configurado e se a steam key está configurada.")
        print("Atualizando capas dos jogos do steam")
        steam_ids_adicionadas = []
        client = steamfront.Client()
        jogos_nao_encontrados_no_steam = []
        for jogo in tqdm(Jogo.objects.filter(steam_id__isnull=True)):
            try:
                busca = client.getApp(name=jogo.titulo)
                jogo.steam_id = busca.appid
                jogo.save()
                steam_ids_adicionadas.append(jogo)
            except:
                jogos_nao_encontrados_no_steam.append(jogo)
        capas_adicionadas = []
        for jogo in tqdm(Jogo.objects.filter(steam_id__isnull=False, capa='')):
            capa = requests.get(
                "https://steamcdn-a.akamaihd.net/steam/apps/{}/library_600x900.jpg".format(jogo.steam_id)
            )
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(capa.content)
            img_temp.flush()
            jogo.capa.save('capa-{}.jpg'.format(jogo.id), File(img_temp), save=True)
            capas_adicionadas.append(jogo)
        for jogo in jogos_adicionados:
            print('Jogo adicionado: {}'.format(jogo.titulo))
        for jogo in adicionados_ao_steam:
            print('Jogo adicionado ao Steam: {}'.format(jogo.titulo))
        for jogo in adicionados_ao_pc:
            print('Jogo adicionado ao PC: {}'.format(jogo.titulo))
        for jogo in steam_ids_adicionadas:
            print('Steam ids adicionadas: {}'.format(jogo.titulo))
        for jogo in jogos_nao_encontrados_no_steam:
            print('Jogos não encontrados no steam: {}'.format(jogo.titulo))
        for jogo in capas_adicionadas:
            print('Capa adicionada: {}'.format(jogo.titulo))


