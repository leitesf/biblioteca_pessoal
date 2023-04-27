import requests
import steamfront
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import transaction
from tqdm import tqdm

from games.models import Jogo
from games.utils import get_genero_equivalente


class ImportadorSteam:
    def __init__(self, steam_api_key, steam_user):
        self.steam_api_key = steam_api_key
        self.steam_user = steam_user

    def importar_jogos_do_usuario(self, steam, pc):
        jogos_adicionados = []
        adicionados_ao_steam = []
        adicionados_ao_pc = []
        print("Importando jogos do usuário principal")
        dados = requests.get(
            "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/" +
            "?key={}&steamid={}&include_appinfo=true&format=json".format(
                self.steam_api_key,
                self.steam_user
            )
        ).json()
        with transaction.atomic():
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
        return jogos_adicionados, adicionados_ao_steam, adicionados_ao_pc


class ImportadorSteamFront:
    cliente = steamfront.Client()

    def buscar_steam_id_de_jogos_sem_steam_id(self):
        print("Buscando jogos sem steam_id no steam")
        steam_ids_adicionadas = []
        jogos_nao_encontrados_no_steam = []
        for jogo in tqdm(Jogo.objects.filter(steam_id__isnull=True)):
            busca = self.buscar_steam_id(jogo.titulo)
            if busca:
                jogo.steam_id = busca
                steam_ids_adicionadas.append(jogo)
            else:
                jogos_nao_encontrados_no_steam.append(jogo)
        return steam_ids_adicionadas, jogos_nao_encontrados_no_steam

    def atualizar_capa_de_jogo(self, jogo):
        capa = requests.get(
            "https://steamcdn-a.akamaihd.net/steam/apps/{}/library_600x900.jpg".format(jogo.steam_id)
        )
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(capa.content)
        img_temp.flush()
        jogo.capa.save('capa-{}.jpg'.format(jogo.id), File(img_temp), save=True)

    def atualizar_genero_de_jogo(self, jogo):
        busca = self.cliente.getApp(appid=jogo.steam_id)
        if 'genres' in busca.raw:
            jogo.genero = get_genero_equivalente(busca.genres[0])
            jogo.save()

    def buscar_steam_id(self, titulo):
        try:
            return self.cliente.getApp(name=titulo).appid
        except:
            return None
