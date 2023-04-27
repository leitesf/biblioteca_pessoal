from django.core.management.base import BaseCommand
from tqdm import tqdm

from games.importador import ImportadorSteam, ImportadorSteamFront
from games.models import Loja, Jogo, Plataforma
from main.models import *


class Command(BaseCommand):
    help = "Resgata jogos do Steam"

    def handle(self, *args, **options):
        configuracao = ConfiguracaoSistema.objects.first()
        usuario_principal = configuracao.usuario_principal
        steam_api_key = configuracao.steam_api_key
        steam = Loja.objects.get_or_create(nome='Steam')[0]
        pc = Plataforma.objects.get_or_create(nome='PC')[0]
        if steam_api_key and usuario_principal and usuario_principal.steam_user:
            importador_steam = ImportadorSteam(steam_api_key, usuario_principal.steam_user)
            jogos_adicionados, adicionados_ao_steam, adicionados_ao_pc = importador_steam.importar_jogos_do_usuario(steam, pc)
        else:
            jogos_adicionados, adicionados_ao_steam, adicionados_ao_pc = [], [], []
            print("Verifique se o usuário principal possui steam user configurado e se a steam key está configurada.")

        importador_steam_front = ImportadorSteamFront()
        steam_ids_adicionadas, jogos_nao_encontrados_no_steam = importador_steam_front.buscar_steam_id_de_jogos_sem_steam_id()
        capas_adicionadas = []
        genero_adicionado = []
        print("Atualizando capas e gêneros dos jogos do steam")
        for jogo in tqdm(Jogo.objects.filter(steam_id__isnull=False, nao_existe_no_steam=False)):
            if not jogo.capa:
                importador_steam_front.atualizar_capa_de_jogo(jogo)
                capas_adicionadas.append(jogo)
            if not jogo.genero:
                try:
                    importador_steam_front.atualizar_genero_de_jogo(jogo)
                    genero_adicionado.append(jogo)
                except:
                    pass
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
        for jogo in genero_adicionado:
            print('Gênero adicionado: {}'.format(jogo.titulo))


